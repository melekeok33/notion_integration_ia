import time
import os
import threading  
from http.server import SimpleHTTPRequestHandler, HTTPServer 
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

#función para engañar al servidor y tener algo mínimo corriendo en el puerto de mi pc
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"🌍 Servidor fantasma activo en el puerto {port} para engañar a Render...")
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()
# ==========================================
load_dotenv()
from notion_client_con import notion_client
from calendar_client_con import CalendarIntegration

class main_orchestrator():
    def __init__(self):

        # 1. Inicializamos Notion
        self.notion = notion_client()
        
        # 2. Inicializamos el Calendario pasándole el Gemini de Notion
        self.calendar = CalendarIntegration(self.notion.a)
        
        # 3. Le pasamos el calendario a Notion para que pueda usarlo en el futuro
        self.notion.calendar = self.calendar

    def start_monitoring(self):
        print("WATCH ASSISTANT ACTIVATED")
        print("Press Ctrl + C to shutdown the assistant.\n")
        
        while True:
            try:
                # Ejecuta el bucle de escaneo normal
                self.notion.read_pages()
                
                # Espera 10 segundos
                time.sleep(10)
                
            except Exception as e:
                print(f" An error occurred in the main loop: {e}")
                time.sleep(15)

if __name__ == "__main__":
    # Encendemos el orquestador
    orchestrator = main_orchestrator()
    
    # Arrancamos el bucle infinito de monitoreo
    orchestrator.start_monitoring()