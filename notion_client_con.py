import requests
import os
from gemini_client_con import gemini_client

class notion_client():
    def __init__(self):
        # Token principal desde variables de entorno
        self.token = os.getenv("NOTION_TOKEN")

        # Encabezados para acceso a Notion API (Versión Estable)
        self.headings = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        self.search_url = "https://api.notion.com/v1/search"
        self.page_id = None
        self.last_time_edited = None
        
        # Inicializamos el cliente de calendario como None (se inyectará desde main.py)
        self.calendar = None 
        self.a = gemini_client()

        # Envío de petición de prueba a Notion
        self.response = requests.post(self.search_url, headers=self.headings)
        
        if self.response.status_code == 200:
            print("NOTION CONNECTED")
        else:
            print(f"SERVER ERROR: {self.response.status_code}:")

    def read_pages(self): # Método principal: busca páginas modificadas
        try:
            json_files = { 
                "filter": {
                    "value": "page",
                    "property": "object"
                },
                "sort": {
                    "direction": "descending",
                    "timestamp": "last_edited_time"
                },
                "page_size": 1
            }

            response_files = requests.post(self.search_url, headers=self.headings, json=json_files) 
            if response_files.status_code == 200:
                files = response_files.json() 
                pages = files['results']

                if not pages:
                    return
                
                page = pages[0]
                page_id = page.get('id')
                last_time = page.get('last_edited_time')

                # Si no hay cambios reales, evitamos procesar de más
                if (self.page_id == page_id) and (self.last_time_edited == last_time):
                    print("No changes")
                    return

                self.page_id = page_id
                self.last_time_edited = last_time

                # Encontrar el título de la página activa
                for pg in pages:
                    properties = pg.get('properties', {})
                    name = "Sin titulo"

                    for prop_name, prop_data in properties.items():
                        if prop_data['type'] == 'title':
                            title = prop_data['title']
                            if title:
                                name = title[0]['text']['content']
                                # Ejecutar el escáner de bloques de contenido
                                parsed_data = self.notion_content(page_id)
                                break
                    

                    if parsed_data["mode"] == "chat":
                        sub_mode = parsed_data["sub_mode"]
                        parrafo = parsed_data["text_to_send"]
                        
                        print(f"TRIGGER DETECTADO -> Página: {name} | Modo: {sub_mode.upper()}") 

                        if sub_mode == "calendar":
                            if hasattr(self, 'calendar') and self.calendar is not None:
                                # Modo Calendario activo
                                text = self.calendar.analyze_and_schedule(parrafo)
                            else:
                                text = "Error: La extensión de calendario no está enlazada correctamente."
                        
                        elif sub_mode == "info":
                            # Modo Información General activo (Gemini puro)
                            text = self.a.function(parrafo)
                        
                        else:
                            # Resguardo por si acaso
                            print("⏳ Comando no reconocido de forma explícita. Ignorando...")
                            return

                        print(text)
                        
                        # Escribimos el resultado en Notion y apagamos el trigger cambiando a @solved
                        if self.write_notion(page_id, text):
                            self.mute_trigger_keyword(parsed_data["trigger_block"], sub_mode)
                    
                    else:
                        # Si no hay palabras clave válidas, duerme plácidamente
                        print(f" Página: {name} | ID: {page_id} -> No active triggers. Sleeping.")
            else:
                raise Exception(response_files.text)

        except Exception as e:
            print(f"SERVER ERROR en read_pages: {e}")

    def _fetch_blocks_recursive(self, block_id: str, level: int = 0) -> list:
        url = f"https://api.notion.com/v1/blocks/{block_id}/children"
        response = requests.get(url, headers=self.headings)
        if response.status_code != 200:
            return []
            
        blocks = response.json().get('results', [])
        flat_list = []
        
        for block in blocks:
            type_block = block.get('type')
            id_block = block.get('id')
            has_children = block.get('has_children', False)
            
            bloque_data = block.get(type_block, {})
            rich_text = bloque_data.get('rich_text', [])
            plain_text = "".join([t.get('plain_text', '') for t in rich_text])
            
            if not plain_text and type_block != "divider":
                continue
                
            flat_list.append({
                "id": id_block,
                "type": type_block,
                "plain_text": plain_text,
                "level": level,
                "block_data": bloque_data
            })
            
            if has_children:
                flat_list.extend(self._fetch_blocks_recursive(id_block, level + 1))
                
        return flat_list

    def notion_content(self, page_id: str) -> dict: 
        blocks = self._fetch_blocks_recursive(page_id)
        
        all_text = []
        chat_instructions = []
        chat_mode = False
        sub_mode = None
        trigger_block = None

        for b in blocks:
            indentation = "  " * b["level"]
            type_block = b["type"]
            plain_text = b["plain_text"]
            
            # Formatear la estructura visual de los elementos
            line = plain_text
            if type_block in ["bulleted_list_item", "numbered_list_item"]:
                line = f"{indentation}- {plain_text}"
            elif type_block == "to_do":
                state = "[x]" if b["block_data"].get('checked') else "[ ]"
                line = f"{indentation}{state} {plain_text}"
            elif type_block in ["heading_1", "heading_2", "heading_3"]:
                prefix = "#" if type_block == "heading_1" else "##" if type_block == "heading_2" else "###"
                line = f"{prefix} {plain_text}"
            elif type_block == "quote":
                line = f"{indentation}> {plain_text}"
            elif type_block == "callout":
                icon = b["block_data"].get('icon', {}).get('emoji', '💡')
                line = f"{indentation}{icon} {plain_text}"
            elif type_block == "code":
                lenguaje = b["block_data"].get('language', '')
                line = f"{indentation}```{lenguaje}\n{plain_text}\n{indentation}```"
            elif type_block == "divider":
                line = "---"

            all_text.append(line)
            
            #Análisis estricto de palabras clave
            if "@gemini" in plain_text and "@solved" not in plain_text and not chat_mode:
                if "@gemini.cal" in plain_text:
                    sub_mode = "calendar"
                    keyword_usada = "@gemini.cal"
                elif "@gemini.info" in plain_text:
                    sub_mode = "info"
                    keyword_usada = "@gemini.info"
                else:
                    sub_mode = None  # Ignora si ponen cosas como @gemini a secas o flashcards futuras

                if sub_mode:
                    chat_mode = True
                    trigger_block = b
                    # Limpiamos el comando del texto final para no confundir a la IA
                    immediate_order = plain_text.split(keyword_usada, 1)[1].strip()
                    if immediate_order:
                        chat_instructions.append(immediate_order)
                    continue
                
            # Si el modo chat se encendió, recopila todo lo que esté debajo del trigger
            if chat_mode:
                chat_instructions.append(line)
                
        if chat_mode:
            return {
                "mode": "chat",
                "sub_mode": sub_mode,
                "text_to_send": "\n".join(chat_instructions),
                "trigger_block": trigger_block
            }
        else:
            return {
                "mode": "summary",
                "sub_mode": None,
                "text_to_send": "\n".join(all_text),
                "trigger_block": None
            }

    def write_notion(self, id: str, text: str):
        url = f"https://api.notion.com/v1/blocks/{id}/children"
        chunk_list = [
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{ "text": { "content": "Gemini:" } }]
                }
            }
        ]

        # Notion limita los bloques a un máximo de 2000 caracteres
        end = 2000
        for i in range(0, len(text), end):
            slice_text = text[i:i+end]
            pgraph = {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{ "text": { "content": slice_text } }]
                }
            }
            chunk_list.append(pgraph)

        payload = {"children": chunk_list}
        respuesta = requests.patch(url, headers=self.headings, json=payload)
        
        if respuesta.status_code == 200:
            return True
        else:
            print(f"WRITE ERROR: {respuesta.status_code}")
            print(respuesta.text)
            return False

    def mute_trigger_keyword(self, block: dict, sub_mode: str):
        """Reemplaza la palabra clave específica por @solved para apagar el trigger"""
        url = f"https://api.notion.com/v1/blocks/{block['id']}"
        
        # Identificamos qué palabra clave exacta debemos apagar
        target_word = f"@gemini.{sub_mode}"
        muted_text = block["plain_text"].replace(target_word, f"@solved.{sub_mode}")
        
        payload = {
            block["type"]: {
                "rich_text": [{ "text": { "content": muted_text } }]
            }
        }
        requests.patch(url, headers=self.headings, json=payload)

# Bloque de ejecución local seguro
if __name__ == "__main__":
    a = notion_client()
    a.read_pages()