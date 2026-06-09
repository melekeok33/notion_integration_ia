# 🤖 Notion × Gemini — Watch Assistant

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Gemini-2.5%20Flash-8E75FF?style=flat-square&logo=google-gemini&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/Notion-API-000000?style=flat-square&logo=notion&logoColor=white" alt="Notion">
  <img src="https://img.shields.io/badge/Status-●%20Active-3ECF8E?style=flat-square" alt="Status">
</p>

> Escribe **`@gemini.resumir`** (o cualquier otro comando) en cualquier parte de tu página de Notion. El asistente en segundo plano lo detectará al instante, procesará el contexto con la IA de Gemini, inyectará la respuesta de forma fragmentada debajo y mutará la etiqueta a `@solved` para evitar ejecuciones infinitas.

---

## 🛠️ Comandos Disponibles

Escribe cualquiera de las siguientes etiquetas al inicio de un bloque en Notion. El texto que coloques después de la etiqueta se enviará automáticamente como el contexto de la solicitud para la Inteligencia Artificial.

| Comando / Etiqueta | Descripción del Procesamiento |
| :--- | :--- |
| **`@gemini.resumir`** | Condensa el bloque completo en puntos clave concisos y estructurados. |
| **`@gemini.mejorar`** | Reescribe el contenido con mejor ortografía y redacción sin alterar la idea original. |
| **`@gemini.formalizar`** | Convierte notas informales o borradores rápidos a un lenguaje corporativo/profesional. |
| **`@gemini.expandir`** | Desarrolla una idea o concepto corto aportando mayor detalle, ejemplos y profundidad. |
| **`@gemini.tareas`** | Analiza analíticamente el texto y extrae una lista de tareas (`To-Do List`) accionables. |
| **`@gemini.preguntas`** | Genera 5 preguntas de estudio o autoevaluación basadas estrictamente en el contenido. |
| **`@gemini.estructura`** | Reorganiza el bloque completo de texto en un esquema (`Outline`) jerárquico y limpio. |
| **`@gemini.definir`** | Detecta el término técnico principal del bloque y lo explica claramente según su contexto. |
| **`@gemini.calcular`** | Detecta, procesa y resuelve expresiones, ecuaciones o problemas matemáticos. |
| **`@gemini.explicar`** | Analiza un bloque de código detectado dentro de Notion y lo detalla paso a paso. |
| **`@gemini.traducir.en`** | Traduce de forma precisa todo el contenido de texto seleccionado al idioma inglés. |
| **`@gemini.cal`** | Procesa texto en lenguaje natural y agenda un evento en tu base de datos de calendario. |

---

## 🚀 Instalación y Despliegue en 4 Pasos

### 1. Clonar el repositorio
```bash
git clone [https://github.com/melekeok33/notion_integration_ia](https://github.com/melekeok33/notion_integration_ia)
cd notion_integration_ia


notion-gemini-assistant/
├── main.py                # Orquestador principal y bucle continuo (polling loop)
├── notion_client_con.py   # Conexión, lectura recursiva de páginas y escritura de bloques
├── gemini_client_con.py   # Cliente dedicado y prompts base de Gemini 2.5 Flash
├── calendar_client_con.py  # Módulo para la integración con base de datos de calendario
├── .env                   # Archivo de tokens privados (¡Asegúrate de no subirlo a GitHub!)
└── requirements.txt       # Archivo con todas las dependencias del ecosistema Python
