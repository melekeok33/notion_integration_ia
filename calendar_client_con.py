import json
import requests
from datetime import datetime
import os

class CalendarIntegration:
    def __init__(self, gemini_client_instance):
        self.gemini = gemini_client_instance
        notion_token = os.getenv("NOTION_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def analyze_and_schedule(self, text_from_notion: str) -> str:
        print("Analizando texto para el calendario...")
        
        DATABASE_ID = "374dc3e3dfb580b7add0e7ab2b86c3d1" 
        url = "https://api.notion.com/v1/pages"
        
        # 1. Prompt para Gemini (Mantenemos la extracción limpia)
        prompt = f"""
        Actúa como un asistente de calendario estricto y preciso. Analiza el texto del usuario y extrae la información para crear un evento.
        
        Debes responder ÚNICAMENTE con un objeto JSON válido (sin código markdown ni texto extra).
        Si el texto NO contiene una petición de agendar, responde con: {{"action": "none"}}
        
        La fecha y hora actual de referencia es: {datetime.now().strftime("%Y-%m-%d %H:%M")} (Año-Mes-Día Hora:Minuto).
        PRESTA MUCHA ATENCIÓN A LA HORA ESPECIFICADA (ej: "a las 3:00 pm", "a las 15:00"). Si el usuario menciona una hora, colócala exactamente en el start_datetime.
        
        Clasifica el evento en una de estas etiquetas en el campo "tag": "Trabajo", "Personal", "Estudios", o "Otros".
        
        El formato de respuesta JSON obligatorio si hay un evento es:
        {{
            "action": "create_event",
            "title": "Título claro del evento",
            "start_datetime": "Formato AAAAMMDDTHHMM (ej: 20260603T1500)",
            "duration": "Formato [número]h[número]m",
            "tag": "Trabajo, Personal, Estudios, o Otros",
            "description": "Detalles extra"
        }}

        Texto del usuario a analizar:
        "{text_from_notion}"
        """

        try:
            response_text = self.gemini.function(prompt)
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            data = json.loads(response_text)
            if data.get("action") == "none":
                return "No se detectó ninguna orden para el calendario."

            print("¡DATOS DETECTADOS PARA EL CALENDARIO!")
            print(json.dumps(data, indent=4, ensure_ascii=False))

            # =========================================================
            # PROCESAMIENTO DE FECHA Y HORA (MÉTODO SEGURO)
            # =========================================================
            raw_date = data["start_datetime"]
            # Formato ISO limpio que Notion acepta perfectamente
            # Cambia el :00 del final por -05:00
            formatted_date = f"{raw_date[0:4]}-{raw_date[4:6]}-{raw_date[6:8]}T{raw_date[9:11]}:{raw_date[11:13]}:00-06:00"

            COLUMNA_TITULO = "Nombre"
            COLUMNA_FECHA = "Fecha"
            COLUMNA_ETIQUETA = "Etiquetas"

            properties = {}
            properties[COLUMNA_TITULO] = {"title": [{"text": {"content": data["title"]}}]}
            
            # Enviamos solo los datos nativos de tiempo que no rompen la API
            properties[COLUMNA_FECHA] = {
                "date": {
                    "start": formatted_date
                }
            }
            
            properties[COLUMNA_ETIQUETA] = {
                "multi_select": [{"name": data.get("tag", "Otros")}]
            }

            payload = {
                "parent": { "database_id": DATABASE_ID },
                "properties": properties
            }

            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code == 200:
                return f"✅ ¡Evento agendado!: '{data['title']}' fijado correctamente a las {raw_date[9:11]}:{raw_date[11:13]}."
            else:
                print(f"❌ Error detallado de la API de Notion: {response.text}")
                return f"❌ Error al guardar el evento (Status: {response.status_code})."

        except json.JSONDecodeError:
            return "Error: Formato JSON no válido devuelto por la IA."
        except Exception as e:
            return f"Error al procesar el calendario: {e}"