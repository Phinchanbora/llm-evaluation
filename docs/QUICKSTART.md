# 🚀 Quick Start Guide

> Get running with LLM Benchmark Toolkit in 5 minutes.

**Navigation:** [← README](../README.md) | [Providers](PROVIDERS.md) | [API Reference](API.md) | [Academic Usage](ACADEMIC_USAGE.md)

---

## Installation

### From PyPI (Recommended)

```bash
pip install llm-benchmark-toolkit
```

### With Optional Dependencies

```bash
# OpenAI support
pip install llm-benchmark-toolkit[openai]

# Anthropic support
pip install llm-benchmark-toolkit[anthropic]

# All providers
pip install llm-benchmark-toolkit[all]
```

### From Source (Development)

```bash
git clone https://github.com/NahuelGiudizi/llm-evaluation.git
cd llm-evaluation
pip install -e ".[dev]"
```

---

## Quick Commands

### 1. Auto-Detect Provider

```bash
# Set your API key
export OPENAI_API_KEY="sk-..."

# Run quick evaluation (20 questions, ~2 min)
llm-eval quick
```

The CLI auto-detects providers from environment:

- `OPENAI_API_KEY` → OpenAI
- `ANTHROPIC_API_KEY` → Anthropic  
- `DEEPSEEK_API_KEY` → DeepSeek
- Ollama running locally → Ollama

### 2. Specify Model

```bash
# Ollama (local)
llm-eval quick --model llama3.2:1b

# OpenAI
llm-eval quick --model gpt-4o-mini

# With sample size
llm-eval quick --model gpt-4o-mini --sample-size 50
```

### 3. Compare Models

```bash
llm-eval compare --models llama3.2:1b,mistral:7b,phi3
```

### 4. Full Evaluation

```bash
llm-eval run --model llama3.2:1b --output results.json
```

### 5. Academic Evaluation

```bash
llm-eval academic --model llama3.2:1b \
  --sample-size 500 \
  --output-latex results.tex \
  --output-bibtex citations.bib
```

---

## Python API

### Basic Evaluation

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers import OllamaProvider

# Create provider
provider = OllamaProvider(model="llama3.2:1b")

# Create evaluator
evaluator = ModelEvaluator(provider=provider)

# Run evaluation
results = evaluator.evaluate_all()

# Print results
print(f"Overall Score: {results.overall_score:.1%}")
print(f"Accuracy: {results.accuracy:.1%}")
print(f"Avg Response Time: {results.avg_response_time:.2f}s")
```

### With Caching (10x Faster)

```python
from llm_evaluator.providers import CachedProvider, OllamaProvider

# Wrap provider with cache
base = OllamaProvider(model="llama3.2:1b")
provider = CachedProvider(base)

evaluator = ModelEvaluator(provider=provider)
results = evaluator.evaluate_all()

# Check cache stats
stats = provider.get_cache_stats()
print(f"Cache hit rate: {stats['hit_rate_percent']:.1f}%")
```

### Custom Configuration

```python
from llm_evaluator.providers import GenerationConfig, OllamaProvider

config = GenerationConfig(
    temperature=0.3,      # Lower = more deterministic
    max_tokens=256,       # Limit response length
    timeout_seconds=60,   # Request timeout
    retry_attempts=5      # Retries on failure
)

provider = OllamaProvider(model="llama3.2:1b", config=config)
```

### Compare Multiple Models

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers import OllamaProvider

models = ["llama3.2:1b", "mistral:7b", "phi3:3.8b"]
results = {}

for model_name in models:
    print(f"📊 Evaluating {model_name}...")
    provider = OllamaProvider(model=model_name)
    evaluator = ModelEvaluator(provider=provider)
    results[model_name] = evaluator.evaluate_all()

# Compare
for name, result in results.items():
    print(f"{name}: {result.overall_score:.1%}")
```

### Direct Benchmark Access

```python
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers import OllamaProvider

provider = OllamaProvider(model="llama3.2:1b")
runner = BenchmarkRunner(
    provider=provider,
    use_full_datasets=True,  # Use HuggingFace datasets
    sample_size=100          # Questions per benchmark
)

# Run all benchmarks
results = runner.run_all_benchmarks()
print(f"MMLU: {results['mmlu']['mmlu_accuracy']:.1%}")
print(f"TruthfulQA: {results['truthfulqa']['truthfulness_score']:.1%}")
print(f"HellaSwag: {results['hellaswag']['hellaswag_accuracy']:.1%}")

# Or run individual benchmarks
mmlu = runner.run_mmlu_sample()
```

---

## Provider Setup

### Ollama (Local)

```bash
# Install Ollama: https://ollama.ai
ollama serve

# Download models
ollama pull llama3.2:1b
ollama pull mistral:7b
```

```python
from llm_evaluator.providers import OllamaProvider

provider = OllamaProvider(model="llama3.2:1b")
```

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

```python
from llm_evaluator.providers import OpenAIProvider

provider = OpenAIProvider(model="gpt-4o-mini")
# Or with explicit key:
provider = OpenAIProvider(model="gpt-4o", api_key="sk-...")
```

### Anthropic

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

```python
from llm_evaluator.providers import AnthropicProvider

provider = AnthropicProvider(model="claude-3-5-sonnet-20241022")
```

### DeepSeek

```bash
export DEEPSEEK_API_KEY="sk-..."
```

```python
from llm_evaluator.providers import DeepSeekProvider

provider = DeepSeekProvider(model="deepseek-chat")
```

---

## Output Examples

### Console Output

```
🚀 LLM QUICK EVALUATION
==================================================
✅ Provider: ollama
✅ Model: llama3.2:1b
✅ Sample size: 20

⏳ Starting evaluation...

📊 Running benchmarks...
📚 MMLU Progress: 100%|████████████| 20/20 [00:25<00:00]
🎯 TruthfulQA Progress: 100%|██████| 20/20 [00:22<00:00]
🧠 HellaSwag Progress: 100%|███████| 20/20 [00:18<00:00]

==================================================
📊 RESULTS
==================================================
  🎯 MMLU:       65.0%
  🎯 TruthfulQA: 55.0%
  🎯 HellaSwag:  72.5%

  📈 Overall:    64.2%

  💾 Cache: 0% hit rate
==================================================
✨ Evaluation complete!
```

### JSON Output

```json
{
  "model_name": "llama3.2:1b",
  "mmlu": {
    "accuracy": 0.65,
    "confidence_interval_95": [0.62, 0.68],
    "n_samples": 100
  },
  "truthfulqa": {
    "accuracy": 0.55,
    "confidence_interval_95": [0.51, 0.59],
    "n_samples": 100
  },
  "hellaswag": {
    "accuracy": 0.725,
    "confidence_interval_95": [0.69, 0.76],
    "n_samples": 100
  },
  "average_accuracy": 0.642
}
```

---

## Benchmark Modes

| Mode | Questions | Time | Use Case |
|------|-----------|------|----------|
| **Demo** | 8 | ~30s | Quick testing |
| **Sample** | 100-500 | 5-30min | Development |
| **Full** | 24,901 | 2-8h | Publication |

```python
# Demo mode (default)
runner = BenchmarkRunner(provider)

# Sample mode
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=100)

# Full mode
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=None)
```

---

## Next Steps

- 🔌 [Providers Guide](PROVIDERS.md) - All provider configurations
- 📘 [API Reference](API.md) - Complete function/class documentation
- 🎓 [Academic Usage](ACADEMIC_USAGE.md) - Publication-quality evaluations
- 🔬 [Full Benchmarks](FULL_BENCHMARKS.md) - Benchmark dataset details

---

**Navigation:** [← README](../README.md) | [Providers](PROVIDERS.md) | [API Reference](API.md) | [Academic Usage](ACADEMIC_USAGE.md)
