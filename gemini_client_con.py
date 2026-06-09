from google import genai as ai #google ai library
import os
from dotenv import load_dotenv

class gemini_client():
    def __init__ (self):

        #load .env file
        load_dotenv()

        #get the api key
        self.api_key = os.getenv("api_key")

        #initialice the client 
        self.client = ai.Client(api_key=self.api_key)
        

    def function (self, text):

        # System instructions combined into a single valid string payload
        self.prompt = (
            "Eres un asistente de productividad. Dame una respuesta clara al siguiente requerimiento de mi Notion, "
            "manten la respuesta breve."
            "CRÍTICO: Devuelve la respuesta en TEXTO PLANO PURO."
            "Usa saltos de línea normales y espaciado para estructurar los párrafos de forma limpia."
            f"Contenido Extraído de Notion:\n{text}"
        )

        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=self.prompt
        )
        
        return response.text

