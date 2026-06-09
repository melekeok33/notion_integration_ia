
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Notion × Gemini — README</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:        #0c0c0f;
    --surface:   #13131a;
    --border:    #1f1f2e;
    --gem:       #7c6ff7;   /* Gemini violet */
    --notion:    #e8e4ff;   /* soft lavender white */
    --accent:    #3ecf8e;   /* mint green — trigger pulse */
    --muted:     #5a5a72;
    --text:      #dcdcf0;
    --mono:      'IBM Plex Mono', monospace;
    --sans:      'Inter', sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    line-height: 1.7;
    padding: 0 1.5rem 6rem;
    max-width: 860px;
    margin: 0 auto;
  }

  /* ── HERO ── */
  .hero {
    padding: 5rem 0 3.5rem;
    border-bottom: 1px solid var(--border);
  }

  .badge-row {
    display: flex;
    gap: .5rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
  }

  .badge {
    font-family: var(--mono);
    font-size: .68rem;
    padding: .25rem .7rem;
    border-radius: 3px;
    letter-spacing: .06em;
    text-transform: uppercase;
  }

  .badge-python  { background: #2b2b3d; color: #7c9bff; border: 1px solid #3a3a5c; }
  .badge-gemini  { background: #1e1830; color: var(--gem); border: 1px solid #3d3060; }
  .badge-notion  { background: #1a1a2a; color: var(--notion); border: 1px solid #2e2e45; }
  .badge-status  { background: #0d2318; color: var(--accent); border: 1px solid #1a4030; }

  .hero-title {
    font-size: clamp(2.4rem, 6vw, 3.8rem);
    font-weight: 700;
    letter-spacing: -.03em;
    line-height: 1.1;
    color: #fff;
  }

  .hero-title span { color: var(--gem); }

  .hero-sub {
    margin-top: 1.2rem;
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 560px;
    font-weight: 300;
  }

  .hero-sub strong { color: var(--text); font-weight: 500; }

  /* ── FLOW DIAGRAM ── */
  .flow {
    margin: 3.5rem 0;
    display: flex;
    align-items: center;
    gap: .75rem;
    flex-wrap: wrap;
  }

  .flow-node {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: .6rem 1.1rem;
    font-family: var(--mono);
    font-size: .8rem;
    color: var(--text);
  }

  .flow-node.highlight { border-color: var(--gem); color: var(--gem); }
  .flow-node.trigger   { border-color: var(--accent); color: var(--accent); }

  .flow-arrow {
    color: var(--muted);
    font-size: 1.1rem;
    font-family: var(--mono);
  }

  /* ── SECTIONS ── */
  section { margin-top: 4rem; }

  .section-label {
    font-family: var(--mono);
    font-size: .7rem;
    color: var(--muted);
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: .6rem;
    border-bottom: 1px solid var(--border);
  }

  h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 1rem;
  }

  p { color: var(--muted); margin-bottom: .8rem; }
  p strong { color: var(--text); }

  /* ── COMMANDS GRID ── */
  .commands-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: .75rem;
    margin-top: 1.5rem;
  }

  .cmd-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: .9rem 1rem;
    transition: border-color .15s;
  }

  .cmd-card:hover { border-color: var(--gem); }

  .cmd-tag {
    font-family: var(--mono);
    font-size: .78rem;
    color: var(--gem);
    margin-bottom: .35rem;
  }

  .cmd-desc {
    font-size: .8rem;
    color: var(--muted);
    line-height: 1.5;
    margin: 0;
  }

  /* ── CODE BLOCK ── */
  .code-block {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
    font-family: var(--mono);
    font-size: .82rem;
    color: #a8b8d8;
    overflow-x: auto;
    margin-top: 1.2rem;
    line-height: 1.7;
  }

  .code-block .comment { color: var(--muted); }
  .code-block .key     { color: var(--gem); }
  .code-block .val     { color: var(--accent); }
  .code-block .str     { color: #f0a070; }

  /* ── SETUP STEPS ── */
  .steps { margin-top: 1.5rem; display: flex; flex-direction: column; gap: .75rem; }

  .step {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  .step-num {
    font-family: var(--mono);
    font-size: .72rem;
    color: var(--gem);
    background: #1e1830;
    border: 1px solid #3d3060;
    border-radius: 4px;
    padding: .2rem .55rem;
    flex-shrink: 0;
    margin-top: .1rem;
  }

  .step-text { font-size: .9rem; color: var(--muted); }
  .step-text strong { color: var(--text); }
  .step-text code {
    font-family: var(--mono);
    background: var(--surface);
    border: 1px solid var(--border);
    padding: .1rem .4rem;
    border-radius: 3px;
    font-size: .8rem;
    color: var(--accent);
  }

  /* ── FILE TREE ── */
  .file-tree {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    font-family: var(--mono);
    font-size: .82rem;
    line-height: 2;
    margin-top: 1.2rem;
  }

  .ft-dir  { color: var(--notion); }
  .ft-file { color: var(--muted); }
  .ft-note { color: var(--gem); }

  /* ── FOOTER ── */
  footer {
    margin-top: 5rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    font-family: var(--mono);
    font-size: .75rem;
    color: var(--muted);
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: .5rem;
  }

  footer span { color: var(--gem); }
</style>
</head>
<body>

<!-- ── HERO ── -->
<div class="hero">
  <div class="badge-row">
    <span class="badge badge-python">Python 3.10+</span>
    <span class="badge badge-gemini">Gemini 2.5 Flash</span>
    <span class="badge badge-notion">Notion API</span>
    <span class="badge badge-status">● Active</span>
  </div>

  <h1 class="hero-title">Notion <span>×</span> Gemini<br>Watch Assistant</h1>

  <p class="hero-sub">
    Escribe <strong>@gemini.resumir</strong> en cualquier página de Notion.<br>
    El asistente lo detecta, consulta Gemini y escribe la respuesta — solo.
  </p>
</div>

<!-- ── FLOW ── -->
<div class="flow">
  <div class="flow-node">Notion Page</div>
  <div class="flow-arrow">→</div>
  <div class="flow-node trigger">@gemini.comando</div>
  <div class="flow-arrow">→</div>
  <div class="flow-node">Polling Loop</div>
  <div class="flow-arrow">→</div>
  <div class="flow-node highlight">Gemini 2.5</div>
  <div class="flow-arrow">→</div>
  <div class="flow-node">Notion Block</div>
  <div class="flow-arrow">→</div>
  <div class="flow-node">@solved</div>
</div>

<!-- ── COMANDOS ── -->
<section>
  <div class="section-label">Comandos disponibles</div>
  <h2>Etiquetas que reconoce el asistente</h2>
  <p>Escribe la etiqueta en cualquier bloque de Notion. El texto que viene después se envía como contexto.</p>

  <div class="commands-grid">
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.resumir</div>
      <p class="cmd-desc">Condensa el bloque en puntos clave concisos.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.mejorar</div>
      <p class="cmd-desc">Reescribe con mejor redacción sin cambiar la idea.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.formalizar</div>
      <p class="cmd-desc">Convierte notas informales a lenguaje profesional.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.expandir</div>
      <p class="cmd-desc">Desarrolla una idea corta con más detalle.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.tareas</div>
      <p class="cmd-desc">Extrae tareas accionables del texto.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.preguntas</div>
      <p class="cmd-desc">Genera 5 preguntas de estudio desde el contenido.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.estructura</div>
      <p class="cmd-desc">Reorganiza el texto como outline jerárquico.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.definir</div>
      <p class="cmd-desc">Explica el término técnico principal en contexto.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.calcular</div>
      <p class="cmd-desc">Detecta y resuelve expresiones matemáticas.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.explicar</div>
      <p class="cmd-desc">Explica un bloque de código paso a paso.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.traducir.en</div>
      <p class="cmd-desc">Traduce el texto al inglés.</p>
    </div>
    <div class="cmd-card">
      <div class="cmd-tag">@gemini.cal</div>
      <p class="cmd-desc">Agenda un evento directamente en tu base de datos de Notion.</p>
    </div>
  </div>
</section>

<!-- ── SETUP ── -->
<section>
  <div class="section-label">Instalación</div>
  <h2>Corre en 4 pasos</h2>

  <div class="steps">
    <div class="step">
      <div class="step-num">01</div>
      <div class="step-text"><strong>Clona el repositorio</strong><br>
        <code>git clone https://github.com/tu-usuario/notion-gemini-assistant</code>
      </div>
    </div>
    <div class="step">
      <div class="step-num">02</div>
      <div class="step-text"><strong>Instala dependencias</strong><br>
        <code>pip install -r requirements.txt</code>
      </div>
    </div>
    <div class="step">
      <div class="step-num">03</div>
      <div class="step-text"><strong>Configura las variables de entorno</strong><br>
        Crea un archivo <code>.env</code> con <code>NOTION_TOKEN</code> y <code>api_key</code> de Gemini.
      </div>
    </div>
    <div class="step">
      <div class="step-num">04</div>
      <div class="step-text"><strong>Inicia el asistente</strong><br>
        <code>python main.py</code> — el loop empieza a monitorear tus páginas.
      </div>
    </div>
  </div>
</section>

<!-- ── .ENV ── -->
<section>
  <div class="section-label">Configuración</div>
  <h2>Variables de entorno</h2>
  <div class="code-block">
<span class="comment"># .env</span>
<span class="key">NOTION_TOKEN</span>=<span class="str">secret_xxxxxxxxxxxxxxxxxxxx</span>
<span class="key">api_key</span>=<span class="str">AIzaSy_xxxxxxxxxxxxxxxxxxxx</span>
  </div>
</section>

<!-- ── ESTRUCTURA ── -->
<section>
  <div class="section-label">Arquitectura</div>
  <h2>Estructura del proyecto</h2>
  <div class="file-tree">
<span class="ft-dir">notion-gemini-assistant/</span>
├── <span class="ft-file">main.py</span>               <span class="ft-note"># Orquestador principal y polling loop</span>
├── <span class="ft-file">notion_client_con.py</span>  <span class="ft-note"># Lectura de páginas y escritura de bloques</span>
├── <span class="ft-file">gemini_client_con.py</span>  <span class="ft-note"># Cliente de Gemini 2.5 Flash</span>
├── <span class="ft-file">calendar_client_con.py</span> <span class="ft-note"># Integración con base de datos calendario</span>
├── <span class="ft-file">.env</span>                  <span class="ft-note"># Tokens (no subir al repo)</span>
└── <span class="ft-file">requirements.txt</span>
  </div>
</section>

<!-- ── FOOTER ── -->
<footer>
  <div>Built with <span>Python</span> · <span>Gemini 2.5 Flash</span> · <span>Notion API</span></div>
  <div>MIT License</div>
</footer>

</body>
</html>
