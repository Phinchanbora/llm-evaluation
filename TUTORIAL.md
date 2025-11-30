# 🚀 Tutorial Rápido - LLM Evaluation

## ¿Qué es este proyecto?

Un framework para **evaluar modelos de lenguaje** con benchmarks **reales** (24,901 preguntas) y generar **gráficos comparativos**.

---

## 📋 Paso a Paso - Tu Primera Evaluación

### 1️⃣ Activar el entorno virtual

```powershell
cd "c:\Users\nahue\Desktop\Python Projects\llm-evaluation"
.\venv\Scripts\activate
```

### 2️⃣ Verificar que Ollama está corriendo

Abre otra terminal y ejecuta:
```powershell
ollama list
```

Deberías ver tus modelos (llama3.2:1b, mistral, etc.)

### 3️⃣ Ejecutar tu primera evaluación (30 segundos)

```powershell
python examples/demo.py
```

**Esto evalúa tu modelo con 8 preguntas de prueba** (modo demo, súper rápido).

**SALIDA:**
```
MMLU: 62.5%
TruthfulQA: 75.0%
HellaSwag: 50.0%
Overall Score: 62.5%
```

---

## 📊 Ver Gráficos - 3 Formas

### Opción 1: Demo de Visualizaciones (RECOMENDADO para empezar)

```powershell
python examples/demo_visualizations.py
```

**Esto genera 7 gráficos en `outputs/visualizations/`:**
- `benchmark_comparison.png` - Comparación de benchmarks (barras)
- `benchmark_interactive.html` - **ABRIR ESTE** en el navegador (interactivo)
- `quality_radar.html` - Radar chart de calidad
- `performance_heatmap.png` - Mapa de calor
- `score_distribution.html` - Distribución de scores
- `performance_trends.html` - Tendencias de performance
- `dashboard.html` - **DASHBOARD COMPLETO** con todos los gráficos

**ABRE:** `outputs/visualizations/dashboard.html` en tu navegador 🎉

---

### Opción 2: Comparar 2+ Modelos Reales (con evaluación real)

```powershell
python examples/compare_models.py
```

**Esto evalúa 2 modelos de Ollama** (llama3.2:1b vs mistral:7b) y genera gráficos en `outputs/comparisons/`.

**Tiempo:** ~2 minutos (usa 8 preguntas demo por modelo).

---

### Opción 3: CLI Tool (más flexible)

```powershell
# Evaluar 1 modelo
llm-eval run --model llama3.2:1b

# Comparar 2 modelos
llm-eval compare --models llama3.2:1b,mistral:7b

# Benchmark específico (MMLU con 100 preguntas)
llm-eval benchmark --model llama3.2:1b --benchmark mmlu --sample-size 100
```

---

## 🎯 Workflow Recomendado

### Para entender el proyecto (10 minutos):

1. **Ver datos simulados** (sin evaluación real):
   ```powershell
   python examples/demo_visualizations.py
   ```
   📂 Abre: `outputs/visualizations/dashboard.html`

2. **Comparar modelos reales** (evaluación real):
   ```powershell
   python examples/compare_models.py
   ```
   📂 Abre: `outputs/comparisons/comparison_dashboard.html`

---

## 📁 Estructura del Proyecto

```
llm-evaluation/
├── src/llm_evaluator/
│   ├── evaluator.py          # Motor principal de evaluación
│   ├── benchmarks.py          # MMLU, TruthfulQA, HellaSwag
│   ├── visualizations.py      # Generador de gráficos
│   ├── providers/
│   │   ├── ollama_provider.py      # Ollama (local)
│   │   ├── openai_provider.py      # GPT-3.5/4
│   │   ├── anthropic_provider.py   # Claude
│   │   ├── huggingface_provider.py # HuggingFace
│   │   └── cached_provider.py      # Cache (10x speedup)
│   └── cli.py                 # Comando llm-eval
│
├── examples/
│   ├── demo.py                      # ← EMPIEZA AQUÍ (30s)
│   ├── demo_visualizations.py       # ← VER GRÁFICOS (datos simulados)
│   ├── compare_models.py            # ← COMPARAR MODELOS REALES
│   ├── demo_full_benchmarks.py      # Full benchmarks (8 horas)
│   └── demo_vs_real.py              # Demo vs Real comparison
│
├── outputs/                   # ← AQUÍ SE GUARDAN LOS GRÁFICOS
│   ├── visualizations/        # Gráficos de demo
│   └── comparisons/           # Comparaciones reales
│
└── tests/                     # 58 tests (87% coverage)
```

---

## 🔧 Configuración de Providers

### Ollama (Local) - Ya funciona ✅
No necesitas configurar nada, usa tu Ollama local.

### OpenAI (GPT-4) - Opcional
```powershell
# Crea .env en la raíz del proyecto
echo "OPENAI_API_KEY=tu-api-key-aqui" > .env

# Instala dependencias
pip install -e ".[openai]"

# Usa en Python
from llm_evaluator.providers.openai_provider import OpenAIProvider
provider = OpenAIProvider(model="gpt-3.5-turbo")
```

### Anthropic (Claude) - Opcional
```powershell
echo "ANTHROPIC_API_KEY=tu-api-key-aqui" > .env
pip install -e ".[anthropic]"
```

### HuggingFace - Opcional
```powershell
echo "HUGGINGFACE_API_KEY=tu-api-key-aqui" > .env
pip install -e ".[huggingface]"
```

---

## 🎨 Tipos de Gráficos Disponibles

1. **Benchmark Comparison** (barras) - Compara MMLU, TruthfulQA, HellaSwag
2. **Radar Chart** (polígono) - Accuracy, Coherence, Consistency
3. **Heatmap** (mapa de calor) - Performance de múltiples modelos
4. **Score Distribution** (boxplot) - Distribución de scores
5. **Performance Trends** (líneas) - Evolución temporal
6. **Dashboard** (todo junto) - Vista completa interactiva

---

## 💡 Ejemplos de Código

### Ejemplo 1: Evaluación básica con gráficos

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.visualizations import EvaluationVisualizer

# Evaluar modelo
provider = OllamaProvider(model="llama3.2:1b")
evaluator = ModelEvaluator(provider=provider)
results = evaluator.evaluate_all()

# Generar gráficos
viz = EvaluationVisualizer()
results_dict = {
    "llama3.2:1b": {
        "mmlu": results.quality_metrics.get("mmlu_score", 0),
        "truthful_qa": results.quality_metrics.get("truthful_qa_score", 0),
        "hellaswag": results.quality_metrics.get("hellaswag_score", 0),
    }
}

viz.plot_benchmark_comparison(
    results_dict,
    output_path="my_benchmark.html",
    interactive=True
)

print(f"✅ Gráfico guardado: my_benchmark.html")
```

### Ejemplo 2: Comparar 3 modelos

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.visualizations import quick_comparison

models = ["llama3.2:1b", "mistral:7b", "phi3:3.8b"]
results = {}

for model in models:
    provider = OllamaProvider(model=model)
    evaluator = ModelEvaluator(provider=provider)
    results[model] = evaluator.evaluate_all()

# Genera dashboard completo
quick_comparison(results, output_dir="my_comparison")
print(f"✅ Dashboard: my_comparison/comparison_dashboard.html")
```

### Ejemplo 3: Usar caching (10x más rápido)

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.providers.cached_provider import CachedProvider

# Wrap el provider con cache
base_provider = OllamaProvider(model="llama3.2:1b")
cached_provider = CachedProvider(base_provider, ttl=3600)  # 1 hora

evaluator = ModelEvaluator(provider=cached_provider)

# Primera evaluación: lenta (llama al modelo)
results1 = evaluator.evaluate_all()  # ~60 segundos

# Segunda evaluación: rápida (usa cache)
results2 = evaluator.evaluate_all()  # ~6 segundos (10x más rápido)

# Ver estadísticas de cache
stats = cached_provider.get_cache_stats()
print(f"Cache hits: {stats['hits']}, Misses: {stats['misses']}")
print(f"Hit rate: {stats['hit_rate_percent']:.1f}%")
```

---

## 🐛 Troubleshooting

### "No module named 'ollama'"
```powershell
pip install ollama
```

### "Connection refused" al evaluar
Verifica que Ollama está corriendo:
```powershell
ollama serve
```

### "Model not found"
Descarga el modelo:
```powershell
ollama pull llama3.2:1b
```

### No veo los gráficos
Los gráficos se guardan en `outputs/`. Busca archivos `.html` y `.png`:
```powershell
Get-ChildItem -Path outputs -Recurse -Include *.html,*.png
```

---

## 📚 Modos de Evaluación

| Modo | Preguntas | Tiempo | Uso |
|------|-----------|--------|-----|
| **Demo** | 8 | 30s | Testing rápido |
| **Sample** | 100-500 | 5min | Evaluación media |
| **Full** | 24,901 | 8hrs | Paper científico |

```python
# Demo mode (default)
evaluator = ModelEvaluator(provider=provider)
results = evaluator.evaluate_all()  # 8 preguntas

# Sample mode
from llm_evaluator.benchmarks import BenchmarkRunner
runner = BenchmarkRunner(provider=provider, mode="full", sample_size=100)
results = runner.run_all_benchmarks()  # 100 preguntas

# Full mode (cuidado, 8 horas)
runner = BenchmarkRunner(provider=provider, mode="full")
results = runner.run_all_benchmarks()  # 24,901 preguntas
```

---

## 🎯 Próximos Pasos

1. ✅ **Ejecuta `python examples/demo_visualizations.py`**
2. ✅ **Abre `outputs/visualizations/dashboard.html`**
3. 🔄 **Ejecuta `python examples/compare_models.py`** (evaluación real)
4. 📊 **Abre `outputs/comparisons/comparison_dashboard.html`**
5. 🚀 **Usa el CLI**: `llm-eval run --model tu-modelo`

---

## 📞 Ayuda

- **Docs completas**: `docs/QUICKSTART.md`
- **Tests**: `pytest tests/ -v`
- **GitHub**: https://github.com/NahuelGiudizi/llm-evaluation

---

## 🎉 Resumen Visual

```
TU WORKFLOW:
1. python examples/demo_visualizations.py     → Ver gráficos simulados
2. Abrir: outputs/visualizations/dashboard.html → 🎨 Dashboard interactivo
3. python examples/compare_models.py          → Evaluar modelos reales
4. Abrir: outputs/comparisons/comparison_dashboard.html → 📊 Comparación real
```

**¡Disfruta evaluando tus LLMs! 🚀**
