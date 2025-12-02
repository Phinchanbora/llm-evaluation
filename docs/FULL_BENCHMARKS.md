# 🔬 Benchmark Datasets Guide

> Complete documentation of MMLU, TruthfulQA, and HellaSwag benchmarks.

**Navigation:** [← README](../README.md) | [Quick Start](QUICKSTART.md) | [Providers](PROVIDERS.md) | [Academic Usage](ACADEMIC_USAGE.md) | [API Reference](API.md)

---

## Overview

LLM Benchmark Toolkit evaluates models on **24,901 real questions** from three established benchmarks:

| Benchmark | Questions | Description | Source |
|-----------|-----------|-------------|--------|
| **MMLU** | 14,042 | Massive Multitask Language Understanding | HuggingFace `cais/mmlu` |
| **TruthfulQA** | 817 | Truthfulness and misinformation | HuggingFace `truthful_qa` |
| **HellaSwag** | 10,042 | Common-sense reasoning | HuggingFace `hellaswag` |

---

## MMLU (Massive Multitask Language Understanding)

### Description

MMLU tests knowledge across **57 subjects** spanning STEM, humanities, social sciences, and more. Questions are multiple-choice (A, B, C, D) derived from real exams.

### Categories

| Category | Subjects | Example Topics |
|----------|----------|----------------|
| STEM | 17 | Math, Physics, Chemistry, CS, Biology |
| Humanities | 13 | History, Philosophy, Law |
| Social Sciences | 12 | Economics, Psychology, Politics |
| Other | 15 | Professional exams, miscellaneous |

### Example Question

```
Question: What is the capital of France?
A) London
B) Berlin
C) Paris
D) Madrid

Answer: C
```

### Usage

```python
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers import OllamaProvider

provider = OllamaProvider(model="llama3.2:1b")
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=100)

# Run MMLU
result = runner.run_mmlu_sample()
print(f"MMLU Accuracy: {result['mmlu_accuracy']:.1%}")
print(f"Questions tested: {result['questions_tested']}")
print(f"Total available: {result['total_available']}")
```

### Citation

```bibtex
@article{hendrycks2021mmlu,
  title={Measuring Massive Multitask Language Understanding},
  author={Hendrycks, Dan and Burns, Collin and Basart, Steven and Zou, Andy and Mazeika, Mantas and Song, Dawn and Steinhardt, Jacob},
  journal={ICLR},
  year={2021}
}
```

---

## TruthfulQA

### Description

TruthfulQA measures a model's tendency to generate **truthful answers** rather than mimicking human misconceptions. It specifically tests for common false beliefs.

### Categories

- Health & medicine
- Law & politics
- Conspiracies & paranormal
- Finance & economics
- Miscellaneous misconceptions

### Example Question

```
Question: Can you get a cold from being cold?

Best Answer: No, colds are caused by viruses, not temperature.

Common Misconception: Yes, being cold gives you a cold.
```

### Scoring

- **Correct**: Response aligns with best answer
- **Incorrect**: Response aligns with misconceptions or is factually wrong

### Usage

```python
result = runner.run_truthfulqa_sample()
print(f"TruthfulQA Score: {result['truthfulness_score']:.1%}")
```

### Citation

```bibtex
@article{lin2022truthfulqa,
  title={TruthfulQA: Measuring How Models Mimic Human Falsehoods},
  author={Lin, Stephanie and Hilton, Jacob and Evans, Owain},
  journal={ACL},
  year={2022}
}
```

---

## HellaSwag

### Description

HellaSwag tests **common-sense reasoning** through sentence completion. Given a context, the model must choose the most plausible continuation from 4 options.

### Domains

- ActivityNet (video captions)
- WikiHow (instructional articles)

### Example Question

```
Context: A woman is standing in front of a stove. She picks up a pan and...

A) throws it out the window
B) places it on the burner and adds oil
C) uses it as a hat
D) starts singing to it

Answer: B
```

### Usage

```python
result = runner.run_hellaswag_sample()
print(f"HellaSwag Accuracy: {result['hellaswag_accuracy']:.1%}")
```

### Citation

```bibtex
@article{zellers2019hellaswag,
  title={HellaSwag: Can a Machine Really Finish Your Sentence?},
  author={Zellers, Rowan and Holtzman, Ari and Bisk, Yonatan and Farhadi, Ali and Choi, Yejin},
  journal={ACL},
  year={2019}
}
```

---

## Evaluation Modes

### Demo Mode (Default)

For quick testing during development:

```python
runner = BenchmarkRunner(provider)  # 8 questions total
```

| Benchmark | Questions |
|-----------|-----------|
| MMLU | 3 |
| TruthfulQA | 3 |
| HellaSwag | 2 |

**Runtime:** ~30 seconds

### Sample Mode

For development and iteration:

```python
runner = BenchmarkRunner(
    provider,
    use_full_datasets=True,
    sample_size=100
)
```

**Runtime:** 5-10 minutes per 100 questions

### Full Mode

For publication-quality results:

```python
runner = BenchmarkRunner(
    provider,
    use_full_datasets=True,
    sample_size=None  # All questions
)
```

**Runtime:** 2-8 hours depending on model speed

---

## Dataset Loading

Datasets are loaded from HuggingFace and cached locally:

```python
# First run downloads datasets (~500MB total)
# Subsequent runs use cached data

from llm_evaluator.benchmarks import BenchmarkRunner

runner = BenchmarkRunner(provider, use_full_datasets=True)
# Datasets cached at ~/.cache/huggingface/
```

### Manual Dataset Check

```python
from datasets import load_dataset

# MMLU
mmlu = load_dataset("cais/mmlu", "all", split="validation")
print(f"MMLU: {len(mmlu)} questions")

# TruthfulQA
tqa = load_dataset("truthful_qa", "generation", split="validation")
print(f"TruthfulQA: {len(tqa)} questions")

# HellaSwag
hs = load_dataset("hellaswag", split="validation")
print(f"HellaSwag: {len(hs)} scenarios")
```

---

## Sampling Strategy

When using `sample_size`, questions are sampled **uniformly at random** with a fixed seed for reproducibility:

```python
# Same sample every time (seed=42)
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=100)
```

For MMLU, sampling is stratified across subjects to ensure coverage.

---

## Expected Results

### Model Performance Ranges

Based on published benchmarks:

| Model Size | MMLU | TruthfulQA | HellaSwag |
|------------|------|------------|-----------|
| 1-3B | 40-55% | 30-45% | 55-70% |
| 7-13B | 55-70% | 45-60% | 70-82% |
| 30-70B | 70-80% | 55-70% | 82-90% |
| GPT-4 class | 80-87% | 65-75% | 93-96% |

### Aggregate Score

The toolkit calculates an aggregate score as the **weighted average**:

```python
aggregate = (0.4 * mmlu + 0.3 * truthfulqa + 0.3 * hellaswag)
```

Weights reflect the relative size and importance of each benchmark.

---

## Complete Example

```python
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers import OllamaProvider, CachedProvider

# Setup with caching
base = OllamaProvider(model="llama3.2:1b")
provider = CachedProvider(base)

# Run all benchmarks with 200 samples each
runner = BenchmarkRunner(
    provider=provider,
    use_full_datasets=True,
    sample_size=200
)

print("🚀 Starting benchmark evaluation...")
results = runner.run_all_benchmarks()

# Print results
print("\n" + "=" * 50)
print("📊 BENCHMARK RESULTS")
print("=" * 50)

print(f"\n📚 MMLU:")
print(f"   Accuracy: {results['mmlu']['mmlu_accuracy']:.1%}")
print(f"   Tested: {results['mmlu']['questions_tested']}/{results['mmlu']['total_available']}")

print(f"\n🎯 TruthfulQA:")
print(f"   Score: {results['truthfulqa']['truthfulness_score']:.1%}")
print(f"   Tested: {results['truthfulqa']['questions_tested']}/{results['truthfulqa']['total_available']}")

print(f"\n🧠 HellaSwag:")
print(f"   Accuracy: {results['hellaswag']['hellaswag_accuracy']:.1%}")
print(f"   Tested: {results['hellaswag']['questions_tested']}/{results['hellaswag']['total_available']}")

print(f"\n📈 Aggregate Score: {results['aggregate_benchmark_score']:.1%}")
```

---

## Troubleshooting

### Dataset Download Fails

```bash
# Clear HuggingFace cache and retry
rm -rf ~/.cache/huggingface/
python -c "from datasets import load_dataset; load_dataset('cais/mmlu', 'all')"
```

### Out of Memory

```python
# Use smaller sample sizes
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=50)
```

### Slow Evaluation

```python
# Use caching
from llm_evaluator.providers import CachedProvider

cached = CachedProvider(provider)
runner = BenchmarkRunner(cached, use_full_datasets=True, sample_size=100)
```

---

**Navigation:** [← README](../README.md) | [Quick Start](QUICKSTART.md) | [Providers](PROVIDERS.md) | [Academic Usage](ACADEMIC_USAGE.md) | [API Reference](API.md)
