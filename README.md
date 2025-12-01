# LLM Evaluation Suite

[![PyPI version](https://badge.fury.io/py/llm-benchmark-toolkit.svg)](https://pypi.org/project/llm-benchmark-toolkit/)
[![Tests](https://github.com/NahuelGiudizi/llm-evaluation/workflows/Tests/badge.svg)](https://github.com/NahuelGiudizi/llm-evaluation/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Benchmark LLMs with real datasets** (24,901 questions from MMLU, TruthfulQA, HellaSwag)

## ⚡ 30-Second Start

```bash
pip install llm-benchmark-toolkit
llm-eval quick llama3.2:1b
```

**Output:**
```
📊 Results for llama3.2:1b:
==================================================
MMLU:       42.3%
TruthfulQA: 38.7%
HellaSwag:  51.2%
==================================================
```

## 🎯 Features

- ✅ **Real benchmarks**: 14,042 MMLU + 817 TruthfulQA + 10,042 HellaSwag
- ✅ **Multi-provider**: Ollama, OpenAI, Anthropic, HuggingFace
- ✅ **CLI tool**: `llm-eval quick`, `run`, `compare`, `benchmark`
- ✅ **10x caching**: Intelligent caching for repeated evaluations
- ✅ **Progress bars**: Real-time progress with ETA

## 📊 CLI Commands

```bash
# Quick benchmark (100 questions, ~5 min)
llm-eval quick llama3.2:1b

# Full evaluation
llm-eval run --model llama3.2:1b

# Compare models
llm-eval compare --models llama3.2:1b,mistral:7b

# Specific benchmarks
llm-eval benchmark --model llama3.2:1b --benchmarks mmlu,truthfulqa

# List providers
llm-eval providers
```

## 🐍 Python API

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider

# Initialize
provider = OllamaProvider(model="llama3.2:1b")
evaluator = ModelEvaluator(provider=provider)

# Run evaluation
results = evaluator.evaluate_all()
print(f"Overall Score: {results.overall_score:.1%}")

# Generate report
evaluator.generate_report(results, output="report.md")
```

## 🔬 Benchmarks

```python
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers.ollama_provider import OllamaProvider

provider = OllamaProvider(model="llama3.2:1b")

# Quick sample (100 questions, ~5 min) - DEFAULT
runner = BenchmarkRunner(provider)
results = runner.run_mmlu_sample()

# Demo mode (3 questions, instant)
runner = BenchmarkRunner(provider, use_full_datasets=False)
results = runner.run_mmlu_sample()

# Full dataset (14,042 questions, ~2 hours)
runner = BenchmarkRunner(provider, sample_size=None)
results = runner.run_mmlu_sample()
```

## 🔐 Providers

```bash
# Ollama (local, free)
pip install llm-benchmark-toolkit

# OpenAI
pip install llm-benchmark-toolkit[openai]

# Anthropic
pip install llm-benchmark-toolkit[anthropic]

# All providers
pip install llm-benchmark-toolkit[all-providers]
```

```python
# OpenAI
from llm_evaluator.providers.openai_provider import OpenAIProvider
provider = OpenAIProvider(model="gpt-3.5-turbo")  # Uses OPENAI_API_KEY

# Anthropic
from llm_evaluator.providers.anthropic_provider import AnthropicProvider
provider = AnthropicProvider(model="claude-3-haiku-20240307")
```

## 📖 Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Full Benchmarks](docs/FULL_BENCHMARKS.md)
- [Testing Guide](docs/TESTING_GUIDE.md)
- [Blog Post](https://dev.to/nahuelgiudizi/building-an-honest-llm-evaluation-framework-from-fake-metrics-to-real-benchmarks-2b90)

## 🔗 Requirements

- Python 3.11+
- [Ollama](https://ollama.com/download) (for local models)
- Models: `ollama pull llama3.2:1b`

## 📝 License

MIT

---

**Author:** Nahuel | **Date:** November 2025
