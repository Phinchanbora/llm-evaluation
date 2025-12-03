# 🎬 Guion para Video Demo de 30 Segundos

**LLM Evaluation Framework - Demo Rápido**

---

## 📝 Objetivo

Mostrar el flujo completo desde instalación hasta visualización de resultados en el dashboard.

---

## 🎥 Estructura del Video (30 segundos)

### **ESCENA 1: Instalación (0-5 segundos)**

**Visual:**

```bash
pip install llm-benchmark-toolkit
```

**Narración/Texto en pantalla:**
> "Install in one command"

**Elementos visuales:**

- Terminal con comando
- Check verde cuando termine la instalación

---

### **ESCENA 2: Quick Evaluation (5-12 segundos)**

**Visual:**

```bash
llm-eval quick
```

**Narración/Texto en pantalla:**
> "Evaluate any model in seconds"

**Elementos visuales:**

- Terminal mostrando:
  - Autodetección: "✓ Found Ollama: llama3.2"
  - Progress bar: "Running MMLU... 5/5 ✓"
  - Progress bar: "Running TruthfulQA... 5/5 ✓"
  - Resultados rápidos:

    ```
    MMLU: 68.5%
    TruthfulQA: 52.3%
    Overall: 60.4%
    ```

---

### **ESCENA 3: Dashboard Web (12-22 segundos)**

**Visual:**

```bash
llm-eval dashboard
```

**Narración/Texto en pantalla:**
> "Visualize results in real-time"

**Elementos visuales:**

- Browser abriendo en <http://localhost:8765>
- Dashboard mostrando:
  1. **Vista de runs** (2 segundos)
     - Lista de evaluaciones pasadas
     - Click en una run
  
  2. **Comparación de modelos** (3 segundos)
     - Gráfico de barras comparando gpt-4o-mini vs claude-3-5-sonnet vs llama3.2
     - Radar chart con múltiples métricas
  
  3. **Viewer de escenarios** (3 segundos)
     - Scroll por preguntas/respuestas individuales
     - Highlight de respuesta correcta vs incorrecta

---

### **ESCENA 4: Multi-Provider Support (22-28 segundos)**

**Visual:**

```bash
llm-eval compare gpt-4o-mini claude-3-5-sonnet llama3.2
```

**Narración/Texto en pantalla:**
> "Compare any model: OpenAI, Anthropic, Ollama, DeepSeek..."

**Elementos visuales:**

- Terminal con progress bars paralelos
- 3 modelos evaluándose al mismo tiempo
- Tabla final comparativa

---

### **ESCENA 5: Cierre + CTA (28-30 segundos)**

**Visual:**

- Logo del framework
- GitHub repo URL

**Narración/Texto en pantalla:**
> "LLM Evaluation Framework"
> "github.com/NahuelGiudizi/llm-evaluation"
> "⭐ Star on GitHub"

---

## 🎨 Estilo Visual

### Colores

- Background: Dark terminal (negro/gris oscuro)
- Text: Verde neón para success, azul para info, rojo para errores
- UI Dashboard: Tema moderno con gradientes sutiles

### Transiciones

- Fade entre escenas (0.2s)
- Zoom in para highlights importantes
- Cursor animado en terminal

### Música

- Background instrumental suave (opcional)
- Sound effects para success checks

---

## 📊 Métricas a Mostrar

### Quick Eval

- MMLU: 68.5%
- TruthfulQA: 52.3%
- HellaSwag: 78.2%

### Compare

| Model | MMLU | TruthfulQA | Avg |
|-------|------|------------|-----|
| gpt-4o-mini | 82.1% | 59.3% | 70.7% |
| claude-3-5-sonnet | 88.7% | 62.1% | 75.4% |
| llama3.2 | 68.5% | 52.3% | 60.4% |

---

## 🎯 Mensajes Clave

1. **Simple**: "One command to install, one command to evaluate"
2. **Multi-Provider**: "Support for 10+ LLM providers"
3. **Academic-Grade**: "10 benchmarks, 50,000+ questions"
4. **Visual**: "Beautiful dashboard for real-time insights"
5. **Local-First**: "Run everything locally with Ollama"

---

## 💡 Tips de Grabación

1. **Terminal**: Usar Asciinema o Terminalizer para grabar terminal con tipeo automático
2. **Dashboard**: Usar screen recorder (OBS Studio) con cursor animado
3. **Edición**: DaVinci Resolve o Premiere Pro
4. **Texto**: Usar subtítulos grandes y legibles
5. **Velocidad**: 1.2x speed para terminal (hace que parezca más fluido)
6. **Resolución**: 1920x1080, 60fps

---

## 📦 Assets Necesarios

- [ ] Logo del framework (PNG transparente)
- [ ] Screenshots del dashboard
- [ ] Terminal recordings
- [ ] Música de fondo (royalty-free)
- [ ] Thumbnails para YouTube/Reddit

---

## 🚀 Donde Publicar

1. **YouTube**: Video completo de 30s
2. **X (Twitter)**: Video + thread explicativo
3. **Reddit**: r/MachineLearning, r/LocalLLaMA
4. **LinkedIn**: Post profesional
5. **GitHub README**: Embed del video
6. **HuggingFace Spaces**: Demo interactivo

---

## ✅ Checklist Pre-Publicación

- [ ] Video grabado y editado
- [ ] Subtítulos agregados
- [ ] Thumbnail atractivo creado
- [ ] Descripción preparada
- [ ] Links verificados
- [ ] Tags optimizados (SEO)
- [ ] Post en redes sociales redactado

---

**Duración total: 30 segundos**  
**Objetivo: Mostrar valor en < 30s y generar estrellas en GitHub**
