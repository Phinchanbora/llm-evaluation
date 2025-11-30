# 🚀 Quick Start Guide

## Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/NahuelGiudizi/llm-evaluation.git
cd llm-evaluation

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -e .

# 4. Verificar instalación
python -m pytest tests/ -v
```

## Prerequisitos

**Ollama debe estar corriendo:**
```bash
# Instalar Ollama: https://ollama.ai
ollama serve  # Iniciar servidor

# Descargar modelos
ollama pull llama3.2:1b
ollama pull mistral:7b
```

## 🎯 Casos de Uso

### 1. Evaluación Básica (Demo Rápido)

```bash
python examples/demo.py
```

**Output:**
- `evaluation_report.md` - Reporte completo
- Métricas en consola

### 2. Evaluación Personalizada

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.providers import GenerationConfig

# Configurar
config = GenerationConfig(
    temperature=0.7,
    max_tokens=500,
    timeout_seconds=60,
    retry_attempts=5
)

provider = OllamaProvider(model="mistral:7b", config=config)
evaluator = ModelEvaluator(provider=provider)

# Evaluar
results = evaluator.evaluate_all()

print(f"Overall Score: {results.overall_score:.2f}")
print(f"Accuracy: {results.accuracy:.1%}")
print(f"Response Time: {results.avg_response_time:.2f}s")
```

### 3. Comparar Múltiples Modelos

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider

models = ["llama3.2:1b", "mistral:7b", "phi3:3.8b"]
results = {}

for model_name in models:
    print(f"\n📊 Evaluating {model_name}...")
    provider = OllamaProvider(model=model_name)
    evaluator = ModelEvaluator(provider=provider)
    results[model_name] = evaluator.evaluate_all()

# Comparar
for name, result in results.items():
    print(f"{name}: {result.overall_score:.2f}/1.00")
```

### 4. Solo Benchmarks

```python
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers.ollama_provider import OllamaProvider

provider = OllamaProvider(model="llama3.2:1b")
runner = BenchmarkRunner(provider=provider)

# Individual
mmlu = runner.run_mmlu_sample()
print(f"MMLU Accuracy: {mmlu['mmlu_accuracy']:.1%}")

# Todos
all_benchmarks = runner.run_all_benchmarks()
print(f"Aggregate: {all_benchmarks['aggregate_benchmark_score']:.1%}")
```

### 5. Solo Visualizaciones

```python
from llm_evaluator.visualizations import quick_comparison

results = {
    "llama3.2:1b": {
        "mmlu": 0.65,
        "accuracy": 0.75,
        "coherence": 0.82,
        "speed": 0.90
    },
    "mistral:7b": {
        "mmlu": 0.78,
        "accuracy": 0.85,
        "coherence": 0.88,
        "speed": 0.70
    }
}

quick_comparison(results, output_dir="visualizations")
```

**Genera 7 tipos de gráficos:**
- Bar charts (estáticos)
- Interactive plotly (HTML)
- Radar charts
- Heatmaps
- Trend analysis
- Box plots
- Dashboards

### 6. Evaluación Personalizada

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider

provider = OllamaProvider(model="llama3.2:1b")
evaluator = ModelEvaluator(provider=provider)

# Test set personalizado
custom_tests = [
    {"prompt": "¿Cuál es la capital de Argentina?", "expected": "Buenos Aires"},
    {"prompt": "¿Cuánto es 15 * 8?", "expected": "120"},
    {"prompt": "¿Quién escribió Don Quijote?", "expected": "Cervantes"}
]

metrics = evaluator.evaluate_quality(test_set=custom_tests)
print(f"Custom Accuracy: {metrics['accuracy']:.1%}")
```

## ⚙️ Configuración

### Opción 1: Variables de Entorno

```bash
# .env file
LLM_EVAL_DEFAULT_MODEL=mistral:7b
LLM_EVAL_DEFAULT_TEMPERATURE=0.8
LLM_EVAL_DEFAULT_TIMEOUT=60
LLM_EVAL_LOG_LEVEL=DEBUG
LLM_EVAL_OUTPUT_DIR=my_outputs

OLLAMA_BASE_URL=http://localhost:11434
BENCHMARK_USE_DEMO_BENCHMARKS=true
```

### Opción 2: Código

```python
from llm_evaluator.config import get_evaluator_config

config = get_evaluator_config()
config.default_temperature = 0.9
config.log_level = "DEBUG"
```

### Opción 3: Constructor

```python
from llm_evaluator.providers import GenerationConfig

config = GenerationConfig(
    temperature=0.9,
    max_tokens=1000,
    timeout_seconds=120,
    retry_attempts=5
)
```

## 🧪 Testing

```bash
# Todos los tests
python -m pytest tests/ -v

# Tests específicos
python -m pytest tests/test_evaluator.py -v
python -m pytest tests/test_benchmarks.py -v

# Con coverage
pip install pytest-cov
python -m pytest tests/ --cov=src/llm_evaluator --cov-report=html

# Ver coverage
open htmlcov/index.html  # o Start htmlcov/index.html en Windows
```

## 📊 Benchmarks: Demo vs Real

**Importante:** Los benchmarks actuales son DEMO (3-2 preguntas).

**Para producción, integrar datasets reales:**

```python
# Instalar
pip install datasets

from datasets import load_dataset

# MMLU - 14,042 preguntas
mmlu = load_dataset('cais/mmlu', 'all')

# TruthfulQA - 817 preguntas
truthfulqa = load_dataset('truthful_qa', 'generation')

# HellaSwag - 10,042 scenarios
hellaswag = load_dataset('Rowan/hellaswag')
```

## 🐛 Troubleshooting

### Ollama no responde
```bash
# Verificar que esté corriendo
ollama list

# Reiniciar
# Windows: reiniciar servicio
# Linux/Mac: ollama serve
```

### Modelo no encontrado
```bash
# Descargar modelo
ollama pull llama3.2:1b

# Verificar descarga
ollama list
```

### Tests fallan
```bash
# Verificar instalación
pip install -e .

# Reinstalar dependencias
pip install -r requirements.txt
```

### Import errors
```python
# Asegurar que estás en el directorio correcto
import sys
sys.path.insert(0, 'src')
```

## 📈 Performance Tips

1. **Modelos pequeños primero**: `llama3.2:1b` es rápido para testing
2. **Reducir samples**: `evaluate_performance(num_samples=5)` para dev
3. **Cache resultados**: Guardar reports para no re-evaluar
4. **Usar GPU**: Ollama detecta automáticamente
5. **Batch prompts**: El provider usa `generate_batch()` cuando posible

## 🎨 Visualizaciones Avanzadas

```python
from llm_evaluator.visualizations import EvaluationVisualizer

viz = EvaluationVisualizer(style="dark", figsize=(12, 8))

# Comparación estática
viz.create_benchmark_comparison(results, output="comparison.png")

# Interactivo
viz.create_benchmark_comparison(results, output="comparison.html", interactive=True)

# Dashboard completo
viz.create_dashboard(results, output="dashboard.html")

# Radar chart
viz.create_radar_chart(results, output="radar.png")

# Heatmap
viz.create_model_heatmap(results, output="heatmap.png")
```

## 🔍 Debugging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# O en config
from llm_evaluator.config import get_evaluator_config
config = get_evaluator_config()
config.log_level = "DEBUG"
config.log_file = "debug.log"
```

## 📝 Próximos Pasos

1. **Explorar ejemplos**: Ver `demo.py` y `demo_visualizations.py`
2. **Leer tests**: `tests/` muestra todos los casos de uso
3. **Revisar docs**: README.md tiene más detalles
4. **Integrar tu caso de uso**: Crear provider personalizado si necesario
5. **Contribuir**: Issues y PRs bienvenidos

## 🚨 Limitaciones Conocidas

Ver `LIMITATIONS.md` para lista completa de:
- Benchmarks demo (no producción)
- Performance con modelos grandes
- Dependencia de Ollama
- Coverage gaps
