# 🎨 Guion para GIF Animado del README

**LLM Evaluation Framework - Demo Visual**

---

## 📝 Objetivo

Crear un GIF de 10-15 segundos que muestre el flujo completo de evaluación y visualización en el dashboard, optimizado para el README de GitHub.

---

## 🎬 Estructura del GIF (Loop continuo)

### **FRAME 1: Instalación (2 segundos)**

**Terminal:**

```bash
$ pip install llm-benchmark-toolkit
✓ Successfully installed llm-benchmark-toolkit-0.6.0
python -m llm_evaluator.dashboard
```

**Elementos:**

- Prompt con cursor parpadeante
- Comando aparece con efecto de tipeo
- Check verde al finalizar

---

### **FRAME 2: Quick Evaluation (3 segundos)**

**Terminal:**

```bash
$ llm-eval quick

🔍 Detecting available models...
✓ Found: Ollama (llama3.2)

📊 Running quick evaluation...
MMLU       [████████████████████] 5/5   ✓
TruthfulQA [████████████████████] 5/5   ✓
HellaSwag  [████████████████████] 5/5   ✓

📈 Results:
┌──────────────┬────────┐
│ Benchmark    │ Score  │
├──────────────┼────────┤
│ MMLU         │ 68.5%  │
│ TruthfulQA   │ 52.3%  │
│ HellaSwag    │ 78.2%  │
├──────────────┼────────┤
│ Overall      │ 66.3%  │
└──────────────┴────────┘
```

**Animación:**

- Progress bars llenan de izquierda a derecha
- Checks aparecen uno por uno
- Tabla se dibuja línea por línea

---

### **FRAME 3: Transición al Dashboard (1 segundo)**

**Terminal:**

```bash
$ llm-eval dashboard

🚀 Starting dashboard...
✓ Backend running on http://localhost:8765
✓ Frontend ready
🌐 Opening browser...
```

**Animación:**

- Fade out del terminal
- Fade in del browser

---

### **FRAME 4: Dashboard - Lista de Runs (2 segundos)**

**Browser:**

```
╔════════════════════════════════════════════════════════╗
║ 🚀 LLM Evaluation Dashboard                            ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  📊 Recent Evaluations                                 ║
║  ┌──────────────────────────────────────────────────┐ ║
║  │ ○ llama3.2      MMLU, TruthfulQA    Dec 3, 2025 │ ║
║  │ ○ gpt-4o-mini   MMLU, GSM8K         Dec 2, 2025 │ ║
║  │ ○ claude-3.5    Full Benchmark      Dec 1, 2025 │ ║
║  └──────────────────────────────────────────────────┘ ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

**Animación:**

- Cursor hover sobre primera run
- Click y highlight

---

### **FRAME 5: Dashboard - Comparación de Modelos (3 segundos)**

**Browser:**

```
╔════════════════════════════════════════════════════════╗
║ 📊 Model Comparison                                    ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  MMLU Scores                                           ║
║  █████████████████ gpt-4o-mini      82.1%             ║
║  ██████████████████████ claude-3.5  88.7%             ║
║  █████████████ llama3.2             68.5%             ║
║                                                        ║
║  TruthfulQA Scores                                     ║
║  ██████████████ gpt-4o-mini         59.3%             ║
║  ███████████████ claude-3.5         62.1%             ║
║  ████████████ llama3.2              52.3%             ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

**Animación:**

- Barras crecen de izquierda a derecha
- Porcentajes aparecen con counter effect
- Highlight del modelo ganador

---

### **FRAME 6: Dashboard - Viewer de Escenarios (2 segundos)**

**Browser:**

```
╔════════════════════════════════════════════════════════╗
║ 🔍 Scenarios Viewer                                    ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  Question:                                             ║
║  "What is the capital of France?"                      ║
║                                                        ║
║  Response: "Paris"                        ✓ Correct   ║
║                                                        ║
║  ────────────────────────────────────────────────────  ║
║                                                        ║
║  Question:                                             ║
║  "Is the sky blue because of ocean reflection?"        ║
║                                                        ║
║  Response: "Yes, the sky appears blue because..."      ║
║                                           ✗ Incorrect  ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

**Animación:**

- Scroll suave por las preguntas
- Checkmarks y X aparecen con fade
- Highlight de respuesta correcta (verde) e incorrecta (rojo)

---

### **FRAME 7: Logo + CTA (2 segundos)**

**Visual:**

```
╔════════════════════════════════════════════════════════╗
║                                                        ║
║             🚀 LLM Evaluation Framework                ║
║                                                        ║
║         10+ Providers | 10 Benchmarks | 50K+ Tests    ║
║                                                        ║
║      github.com/NahuelGiudizi/llm-evaluation          ║
║                                                        ║
║                    ⭐ Star on GitHub                   ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

**Animación:**

- Fade in del texto
- Star icon con pulso animado
- Loop back al Frame 1

---

## 🎨 Especificaciones Técnicas

### Dimensiones

- **Ancho**: 1000px (optimal para GitHub)
- **Alto**: 600px
- **Ratio**: 5:3

### Formato

- **Tipo**: GIF animado
- **FPS**: 15 frames por segundo
- **Duración**: 15 segundos (loop infinito)
- **Tamaño**: < 5MB (GitHub limit: 10MB)

### Colores

```css
--terminal-bg: #1e1e1e
--terminal-text: #00ff00
--success: #00ff00
--error: #ff4444
--info: #3b82f6
--highlight: #fbbf24
--ui-bg: #ffffff
--ui-border: #e5e7eb
--ui-accent: #3b82f6
```

### Fuentes

- **Terminal**: Fira Code, Monospace
- **Dashboard**: Inter, Sans-serif
- **Tamaño**: 14-16px para legibilidad

---

## 🛠️ Herramientas para Crear el GIF

### Opción 1: Terminalizer + ScreenToGif

1. **Terminal**: Grabar con Terminalizer

   ```bash
   npm install -g terminalizer
   terminalizer record demo
   terminalizer render demo
   ```

2. **Dashboard**: Grabar con OBS o ScreenToGif
   - Configurar 1000x600 canvas
   - Grabar interacción con dashboard

3. **Combinar**: Usar GIMP o Photoshop para unir frames

### Opción 2: Asciinema + agg

1. **Grabar terminal**:

   ```bash
   asciinema rec demo.cast
   ```

2. **Convertir a GIF**:

   ```bash
   agg demo.cast demo.gif
   ```

### Opción 3: Playwright + gifski (Automatizado)

```javascript
// playwright-to-gif.js
const { chromium } = require('playwright');
const { exec } = require('child_process');

async function createGif() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 600 } });
  
  // Navigate to dashboard
  await page.goto('http://localhost:8765');
  
  // Record frames
  for (let i = 0; i < 100; i++) {
    await page.screenshot({ path: `frame-${i}.png` });
    await page.waitForTimeout(100);
  }
  
  await browser.close();
  
  // Convert to GIF
  exec('gifski -o demo.gif frame-*.png --fps 10');
}
```

---

## 📐 Layout del GIF

```
┌─────────────────────────────────────────────┐
│ [Terminal o Dashboard ocupan todo]         │
│                                             │
│                                             │
│                                             │
│                                             │
│                                             │
│                                             │
│ [Pequeño logo/badge en esquina superior]   │
└─────────────────────────────────────────────┘
```

---

## 🎯 Elementos Clave a Mostrar

1. ✅ **Instalación simple**: Un comando
2. ✅ **Autodetección**: Sin config manual
3. ✅ **Progress visual**: Barras animadas
4. ✅ **Resultados claros**: Tabla con scores
5. ✅ **Dashboard moderno**: UI limpia y profesional
6. ✅ **Comparación**: Múltiples modelos side-by-side
7. ✅ **Detalle**: Preguntas/respuestas individuales
8. ✅ **Multi-provider**: Logos de OpenAI, Anthropic, Ollama

---

## 📝 Texto Alternativo (Alt Text)

Para accesibilidad en GitHub:

```markdown
![LLM Evaluation Framework Demo](demo.gif)

*Quick evaluation demo: Install with pip, run `llm-eval quick`, 
visualize results in the dashboard. Support for 10+ LLM providers.*
```

---

## 🚀 Optimización

### Reducir tamaño del GIF

```bash
# Usar gifsicle para comprimir
gifsicle -O3 --colors 256 demo.gif -o demo-optimized.gif

# O usar gifski (mejor calidad)
gifski --fps 15 --quality 90 --width 1000 frames/*.png -o demo.gif
```

### Prioridades

1. **Legibilidad** > Tamaño
2. **Smooth animation** > FPS alto
3. **Key moments** > Todo el flujo

---

## ✅ Checklist de Creación

- [ ] Grabar terminal con comandos
- [ ] Grabar dashboard con interacciones
- [ ] Editar timing (cada frame visible 2-3s)
- [ ] Agregar transiciones suaves
- [ ] Verificar legibilidad del texto
- [ ] Optimizar tamaño (< 5MB)
- [ ] Test en diferentes tamaños de pantalla
- [ ] Agregar al README en sección destacada
- [ ] Subir a GitHub
- [ ] Compartir en redes sociales

---

## 💡 Variantes del GIF

### GIF Corto (5 segundos)

- Solo terminal con quick eval
- Para Twitter/X donde GIFs cortos funcionan mejor

### GIF Largo (20 segundos)

- Flujo completo con compare y dashboard
- Para README principal y documentación

### GIF Vertical (para móvil)

- 600x1000px
- Optimizado para Instagram/Stories

---

## 🎬 Dónde Incluir el GIF

1. **README.md**: Primera sección después del título
2. **docs/QUICKSTART.md**: Inicio del tutorial
3. **PyPI page**: En la descripción larga
4. **X (Twitter)**: Tweet de lanzamiento
5. **Reddit**: Post en r/MachineLearning
6. **LinkedIn**: Post profesional
7. **Dev.to**: Blog post

---

**Duración: 15 segundos (loop)**  
**Objetivo: Mostrar valor y wow factor en el primer scroll del README**
