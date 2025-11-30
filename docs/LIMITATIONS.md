# ⚠️ Limitations & Known Issues

## Perspectiva CTO: Análisis Honesto

Este documento presenta las **limitaciones reales** del proyecto desde una perspectiva enterprise.

---

# ⚠️ Limitations & Known Issues

## Perspectiva CTO: Análisis Honesto

Este documento presenta las **limitaciones reales** del proyecto desde una perspectiva enterprise.

---

## ✅ RESUELTO: Benchmarks Demo → Production-Ready

### ~~1. Benchmarks Demo (NOT Production-Ready)~~ ✅ FIXED

**Estado:** ✅ **RESUELTO** - Implementación completa disponible

**Solución Implementada:**

- ✅ MMLU: **14,042 preguntas reales** desde HuggingFace
- ✅ TruthfulQA: **817 preguntas reales** desde HuggingFace
- ✅ HellaSwag: **10,042 escenarios reales** desde HuggingFace

**Ahora Válido Para:**

- ✅ Investigación académica
- ✅ Comparaciones serias entre modelos
- ✅ Publicación en papers
- ✅ Benchmarking enterprise

**Uso:**

```python
from llm_evaluator.benchmarks import BenchmarkRunner

# Modo demo (rápido, desarrollo)
runner = BenchmarkRunner(provider)

# Modo sampling (recomendado, 5-10 min)
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=100)

# Modo full (producción, 2-8 horas)
runner = BenchmarkRunner(provider, use_full_datasets=True)

results = runner.run_all_benchmarks()
```

**Documentación:** Ver `FULL_BENCHMARKS.md` y `CHANGELOG_BENCHMARKS.md`

**Fecha de Resolución:** Noviembre 29, 2025

---

## 🔴 Limitaciones Críticas (Bloqueantes para Producción)

### 1. Solo Ollama Provider Implementado

**Problema:**

- OpenAI provider: **NO IMPLEMENTADO**
- Anthropic provider: **NO IMPLEMENTADO**
- HuggingFace provider: **NO IMPLEMENTADO**

**Impacto:**

- Limitado a modelos locales Ollama
- No puede comparar GPT-4, Claude, etc.
- Promesas de "multi-provider" son arquitectura, no realidad

**Solución:**

```python
# Implementar providers faltantes
class OpenAIProvider(LLMProvider):
    def generate(self, prompt, config):
        # API call a OpenAI
        pass
```

**Esfuerzo:** 1-2 días por provider

**Status:** 🏗️ Arquitectura lista, implementations faltantes

---

### 2. Performance con Modelos Grandes (>7B)

**Problema:**

- Modelos 33B+: **muy lentos** sin GPU
- Timeouts frecuentes
- Memoria insuficiente en máquinas normales

**Datos Reales:**

```
llama3.2:1b  → 0.5s por prompt  ✅
mistral:7b   → 2-3s por prompt  ⚠️
deepseek:33b → 15-30s por prompt ❌
```

**Impacto:**

- Evaluaciones de modelos grandes toman **horas**
- No escalable para CI/CD
- Necesita hardware especializado

**Solución:**

- Configurar timeouts adecuados
- Usar GPU (CUDA/Metal)
- Batch processing (parcialmente implementado)
- Considerar vLLM para inference rápido

**Status:** ⚠️ Limitación inherente de LLMs locales

---

### 3. Coverage Gaps

**Tests Coverage:**

- Core modules: 95%+
- Visualizations: **70%** (matplotlib difícil de testear)
- End-to-end: **0%** (no integration tests)

**Problema:**

```python
# Sin tests:
- Ollama connection failures
- Network timeouts reales
- Concurrent evaluations
- Large model memory issues
```

**Impacto:**

- Bugs en edge cases
- No confidence en refactors grandes
- CI/CD incompleto

**Solución:**

```bash
# Agregar integration tests
pytest tests/integration/ --slow
```

**Esfuerzo:** 3-5 días

**Status:** 🔴 Gap significativo

---

## 🟡 Limitaciones Importantes (No Bloqueantes)

### 5. Métricas de Calidad Simplificadas

**Problema:**

```python
# Actual: substring matching
if "Paris" in response.lower():
    correct += 1

# Debería: semantic similarity
similarity = sentence_transformers.util.cos_sim(expected, response)
```

**Impacto:**

- False positives/negatives
- No captura respuestas equivalentes
- Ejemplo: "París" vs "Paris" → falla

**Solución:**

```python
pip install sentence-transformers
# Usar embeddings para similarity
```

**Esfuerzo:** 1-2 días

---

### 6. No Database / No Histórico

**Problema:**

- Resultados solo en archivos `.md`
- No tracking de evolución temporal
- No comparación histórica
- No analytics

**Impacto:**

```python
# Quiero ver:
"¿El modelo mejoró desde la semana pasada?"
"¿Qué configuración funciona mejor?"

# Actual:
Comparar 50 archivos .md manualmente 😭
```

**Solución:**

```python
# Agregar SQLite/PostgreSQL
from sqlalchemy import create_engine
results.save_to_db()

# O timeseries DB
influxdb.write(results)
```

**Esfuerzo:** 3-4 días

---

### 7. Hallucination Detection Básico

**Problema:**

```python
# Actual: keyword matching
uncertainty_markers = ["don't know", "not sure"]
if any(marker in response):
    no_hallucination = True

# Débil para:
- Hallucinations sutiles
- Confabulación creativa
- Facts incorrectos con alta confianza
```

**Impacto:**

- Hallucination rate **no confiable**
- Falsos negativos frecuentes

**Solución:**

- Integrar fact-checking APIs
- RAG con knowledge base
- Modelo especializado para validación

**Esfuerzo:** 1 semana+

---

### 8. Configuración Pydantic No Usada en Código

**Problema:**

```python
# Implementado:
class EvaluatorConfig(BaseSettings):
    default_temperature: float = 0.7

# Pero código NO lo usa:
evaluator = ModelEvaluator()  # Ignora config
```

**Impacto:**

- Config file es decorativo
- ENV vars no tienen efecto
- Necesita wiring manual

**Solución:**

```python
# En evaluator.py
from llm_evaluator.config import get_evaluator_config
config = get_evaluator_config()
self.temperature = config.default_temperature
```

**Esfuerzo:** 2-3 horas

**Status:** 🟡 Quick win

---

## 🟢 Limitaciones Menores (Nice to Have)

### 9. No Streaming Responses

**Problema:**

- Evaluaciones largas: sin feedback
- Usuario ve "..." por minutos
- No progress bars

**Solución:**

```python
from tqdm import tqdm
for prompt in tqdm(prompts):
    evaluate(prompt)
```

**Esfuerzo:** 1 hora

---

### 10. No CLI Tool

**Problema:**

```bash
# No existe:
llm-eval compare llama3.2:1b mistral:7b

# Tiene que escribir Python
```

**Solución:**

```python
# Agregar click/typer
import click

@click.command()
@click.argument('models', nargs=-1)
def compare(models):
    # ...
```

**Esfuerzo:** 1 día

---

### 11. Dependencias Pesadas

**Problema:**

```
matplotlib, seaborn, plotly, pandas, numpy, scipy
→ 500MB+ de dependencias
```

**Impacto:**

- Docker images grandes
- Install time lento
- Overkill para uso básico

**Solución:**

```toml
[tool.poetry.extras]
viz = ["matplotlib", "plotly", "seaborn"]
ml = ["scikit-learn", "scipy"]
```

**Esfuerzo:** 2 horas

---

### 12. No Async/Paralelo

**Problema:**

```python
# Sequential:
for model in models:
    evaluate(model)  # 10 min cada uno → 50 min total

# Podría ser:
asyncio.gather(*[evaluate(m) for m in models])  # → 10 min total
```

**Impacto:**

- Comparaciones multi-modelo lentas
- No aprovecha cores

**Solución:**

```python
async def evaluate_async(provider):
    # ...

await asyncio.gather(*evaluations)
```

**Esfuerzo:** 2-3 días

---

## 📊 Scorecard Realista

| Aspecto              | Score | Comentario                    |
| -------------------- | ----- | ----------------------------- |
| **Arquitectura**     | 9/10  | Clean, SOLID, testable        |
| **Type Safety**      | 9/10  | Sin Any types, strict         |
| **Tests**            | 7/10  | 40/40 unit, 0 integration     |
| **Documentation**    | 8/10  | README bueno, falta ADRs      |
| **Benchmarks**       | 3/10  | Solo demos, no reales         |
| **Performance**      | 6/10  | Ok para 1-7B, malo para 33B+  |
| **Features**         | 7/10  | Core sólido, faltan providers |
| **Production Ready** | 5/10  | ⚠️ No para research serio     |

**Overall: 6.75/10** - Excelente base, necesita features adicionales para enterprise

---

## 🎯 Roadmap Sugerido (CTO View)

### Sprint 1 (Alta Prioridad) - 1 semana

1. ✅ Integrar datasets reales (MMLU, TruthfulQA, HellaSwag)
2. ✅ Wire config con código actual
3. ✅ Agregar progress bars

### Sprint 2 (Media Prioridad) - 1 semana

4. ✅ OpenAI provider implementation
5. ✅ Integration tests suite
6. ✅ Semantic similarity para accuracy

### Sprint 3 (Baja Prioridad) - 1 semana

7. ✅ Database para resultados
8. ✅ CLI tool
9. ✅ Async/parallel evaluation

### Post-MVP

- Anthropic provider
- Hallucination detection avanzado
- Web dashboard
- CI/CD pipeline completo

---

## 💡 Recomendaciones para Uso Actual

**✅ Úsalo para:**

- Prototipar comparaciones de modelos
- Learning/teaching LLM evaluation
- Demostrar arquitectura Clean
- Portfolio técnico

**❌ NO usar para:**

- Research papers (benchmarks demo)
- Production model selection crítica
- Publicaciones académicas
- Marketing sin disclaimers

**⚠️ Usar con disclaimers:**

- "Benchmarks demo, no producción"
- "Arquitectura enterprise-ready, features WIP"
- "Necesita integración con datasets reales"

---

## 🤝 Transparencia = Confianza

Este documento existe porque:

1. **Honestidad técnica** es esencial
2. **No sorprender** a futuros usuarios/colaboradores
3. **Roadmap claro** para llegar a 10/10
4. **Portfolio profesional** = código + análisis crítico

**En resumen:** Excelente arquitectura, necesita completar features para ser production-ready.

---

_Last updated: 2025-11-29_
_Maintainer: @NahuelGiudizi_
