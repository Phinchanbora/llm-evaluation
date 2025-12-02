# 🚀 LLM Benchmark Toolkit

<p align="center">
  <img src="https://img.shields.io/pypi/v/llm-benchmark-toolkit?style=for-the-badge&color=blue" alt="PyPI">
  <img src="https://img.shields.io/pypi/dm/llm-benchmark-toolkit?style=for-the-badge&color=green" alt="Downloads">
  <img src="https://img.shields.io/github/stars/NahuelGiudizi/llm-evaluation?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/badge/python-3.11+-blue?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
</p>

<p align="center">
  <b>Benchmark LLMs with real datasets: 24,901 questions from MMLU, TruthfulQA & HellaSwag</b>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-providers">Providers</a> •
  <a href="#-academic-use">Academic</a> •
  <a href="#-docs">Docs</a>
</p>

---

## ⚡ Quick Start

```bash
pip install llm-benchmark-toolkit

# Auto-detect your provider and run evaluation
llm-eval quick
```

**That's it!** The tool auto-detects your LLM provider from environment variables:
- `OPENAI_API_KEY` → Uses GPT-4o-mini
- `ANTHROPIC_API_KEY` → Uses Claude 3.5 Sonnet
- `DEEPSEEK_API_KEY` → Uses DeepSeek-V3
- Ollama running → Uses Llama 3.2

```
🚀 LLM QUICK EVALUATION
==================================================
✅ Provider: openai (gpt-4o-mini)
✅ Sample size: 20

📊 RESULTS
==================================================
  🎯 MMLU:       78.5%
  🎯 TruthfulQA: 71.2%
  🎯 HellaSwag:  82.4%
  
  📈 Overall:    77.4%
==================================================
✨ Evaluation complete!
```

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 📊 **Real Benchmarks** | 14,042 MMLU + 817 TruthfulQA + 10,042 HellaSwag questions |
| 🔌 **5 Providers** | Ollama, OpenAI, Anthropic, DeepSeek, HuggingFace |
| ⚡ **Zero Config** | Auto-detects provider from environment variables |
| 💾 **10x Caching** | Intelligent caching for repeated evaluations |
| 📈 **Academic Rigor** | 95% CI, McNemar tests, baseline comparisons |
| 📄 **Paper Exports** | LaTeX tables, BibTeX citations, reproducibility manifests |
| 🎨 **Beautiful CLI** | Progress bars, colored output, detailed reports |

## 📦 Installation

```bash
# Basic installation
pip install llm-benchmark-toolkit

# With specific provider support
pip install llm-benchmark-toolkit[openai]       # OpenAI GPT models
pip install llm-benchmark-toolkit[anthropic]    # Claude models
pip install llm-benchmark-toolkit[all]          # All providers
```

## 🔌 Providers

### Check Available Providers
```bash
llm-eval providers
```

```
🔌 Available Providers:

✅ Auto-detected: openai (gpt-4o-mini)

  ✅ ollama          - Local LLMs (llama3.2, mistral, etc.)
  ✅ openai          - GPT-3.5, GPT-4, GPT-4o (pip install openai)
  ❌ anthropic       - Claude 3/3.5 (pip install anthropic)
  ✅ deepseek        - DeepSeek-V3, DeepSeek-R1 (pip install openai)
  ❌ huggingface     - Inference API (pip install huggingface-hub)

📋 Environment Variables:
  ✅ OPENAI_API_KEY       sk-abc1...
  ❌ ANTHROPIC_API_KEY    Not set
  ❌ DEEPSEEK_API_KEY     Not set
  ❌ HF_TOKEN             Not set
```

### Provider Examples

```bash
# Ollama (local)
ollama serve  # Start Ollama
llm-eval quick --model llama3.2:1b

# OpenAI
export OPENAI_API_KEY="sk-..."
llm-eval quick --model gpt-4o-mini

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
llm-eval run --model claude-3-5-sonnet-20241022 --provider anthropic

# DeepSeek (super affordable!)
export DEEPSEEK_API_KEY="sk-..."
llm-eval quick --model deepseek-chat
```

## 🖥️ CLI Commands

```bash
# Quick benchmark (20 questions, ~2 min)
llm-eval quick

# Full evaluation with report
llm-eval run --model llama3.2:1b

# Compare multiple models
llm-eval compare --models llama3.2:1b,mistral:7b,phi3

# Run specific benchmarks
llm-eval benchmark --model gpt-4o --provider openai --benchmarks mmlu

# Academic evaluation with exports
llm-eval academic --model llama3.2:1b \
  --sample-size 500 \
  --output-latex results.tex \
  --output-bibtex citations.bib
```

## 🐍 Python API

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers import OllamaProvider, OpenAIProvider

# Option 1: Local with Ollama
provider = OllamaProvider(model="llama3.2:1b")

# Option 2: OpenAI
provider = OpenAIProvider(model="gpt-4o-mini")

# Run evaluation
evaluator = ModelEvaluator(provider=provider)
results = evaluator.evaluate_all()

print(f"Overall Score: {results.overall_score:.1%}")
print(f"MMLU: {results.mmlu_accuracy:.1%}")
print(f"TruthfulQA: {results.truthfulqa_score:.1%}")
```

## 🎓 Academic Use

For publication-quality evaluations with statistical rigor:

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.export import export_to_latex, generate_bibtex

# Run academic evaluation
provider = OllamaProvider(model="llama3.2:1b")
evaluator = ModelEvaluator(provider=provider)

results = evaluator.evaluate_all_academic(
    sample_size=500,
    compare_baselines=True
)

# Results with 95% confidence intervals
print(f"MMLU: {results.mmlu_accuracy:.1%}")
print(f"95% CI: [{results.mmlu_ci[0]:.1%}, {results.mmlu_ci[1]:.1%}]")

# Compare to published baselines (GPT-4, Claude, Llama)
for baseline, comparison in results.baseline_comparison.items():
    print(f"vs {baseline}: {comparison['difference']:+.1%}")

# Export for papers
latex = export_to_latex(results_dict, "My Model")
bibtex = generate_bibtex()
```

See [Academic Usage Guide](docs/ACADEMIC_USAGE.md) for full documentation.

## 🔬 Benchmarks Included

| Benchmark | Questions | Description |
|-----------|-----------|-------------|
| **MMLU** | 14,042 | Massive Multitask Language Understanding - 57 subjects |
| **TruthfulQA** | 817 | Measures truthfulness and avoiding misinformation |
| **HellaSwag** | 10,042 | Common-sense reasoning and sentence completion |

## 💾 Caching

Caching is **enabled by default** and speeds up repeated evaluations by 10x:

```python
from llm_evaluator.providers import CachedProvider, OllamaProvider

# Automatic caching
provider = OllamaProvider(model="llama3.2:1b")
cached = CachedProvider(provider)

# Check cache stats
stats = cached.get_cache_stats()
print(f"Hit rate: {stats['hit_rate_percent']:.1f}%")
```

Cache is stored in `~/.cache/llm-eval/` and persists between sessions.

## 🏆 Model Comparison

Compare your model against published baselines:

```python
results = evaluator.evaluate_all_academic(sample_size=500)

# Built-in baselines
# - GPT-4: 86.4% MMLU
# - Claude 3 Opus: 86.8% MMLU  
# - Llama 3 70B: 79.5% MMLU
# - Mistral 7B: 62.5% MMLU

for baseline, comparison in results.baseline_comparison.items():
    print(f"vs {baseline}: {comparison['difference']:+.1%}")
```

## 📊 Output Formats

```bash
# JSON (default)
llm-eval run --model llama3.2:1b --output results.json

# Markdown report
llm-eval run --model llama3.2:1b --output report.md

# LaTeX tables (for papers)
llm-eval academic --model llama3.2:1b --output-latex table.tex

# BibTeX citations
llm-eval academic --model llama3.2:1b --output-bibtex refs.bib
```

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/NahuelGiudizi/llm-evaluation.git
cd llm-evaluation
pip install -e ".[dev]"
pytest tests/
```

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## ⭐ Star History

If this project helped you, please star it! ⭐

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/NahuelGiudizi">Nahuel Giudizi</a>
</p>
