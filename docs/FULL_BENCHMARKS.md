# 🎯 Full Benchmark Datasets Guide

## Overview

The LLM Evaluator now supports **PRODUCTION-READY benchmark datasets**:

| Benchmark      | Demo Mode   | Full Mode            | Status              |
| -------------- | ----------- | -------------------- | ------------------- |
| **MMLU**       | 3 questions | **14,042 questions** | ✅ Production-Ready |
| **TruthfulQA** | 3 questions | **817 questions**    | ✅ Production-Ready |
| **HellaSwag**  | 2 scenarios | **10,042 scenarios** | ✅ Production-Ready |

## 📊 Modes of Operation

### 1. Demo Mode (Default - Fast)

For quick testing and development:

```python
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers.ollama_provider import OllamaProvider

provider = OllamaProvider(model="llama3.2:1b")
runner = BenchmarkRunner(provider)  # Default: demo mode

results = runner.run_all_benchmarks()
# Uses 3+3+2 = 8 questions total
# Runtime: ~30 seconds
```

### 2. Sampling Mode (Recommended)

Best balance between accuracy and speed:

```python
runner = BenchmarkRunner(
    provider=provider,
    use_full_datasets=True,  # Use real HuggingFace datasets
    sample_size=100          # Sample 100 questions per benchmark
)

results = runner.run_all_benchmarks()
# Uses 100+100+100 = 300 real questions
# Runtime: ~5-10 minutes
# Accuracy: Much more reliable than demo
```

### 3. Full Mode (Production)

Complete evaluation with all questions:

```python
runner = BenchmarkRunner(
    provider=provider,
    use_full_datasets=True,  # Use real datasets
    sample_size=None         # No sampling = ALL questions
)

results = runner.run_all_benchmarks()
# Uses 14,042 + 817 + 10,042 = 24,901 questions
# Runtime: 2-8 HOURS (depends on model and hardware)
# Accuracy: Publication-ready, academically valid
```

## 🚀 Quick Start Examples

### Example 1: Quick Test with Real Data

```python
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers.ollama_provider import OllamaProvider

# Initialize
provider = OllamaProvider(model="llama3.2:1b")

# Use 50-question samples for quick testing
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=50)

# Run individual benchmarks
mmlu_result = runner.run_mmlu_sample()
print(f"MMLU: {mmlu_result['mmlu_accuracy']:.1%}")
print(f"Tested: {mmlu_result['questions_tested']}/{mmlu_result['total_available']}")
```

### Example 2: Compare Multiple Models

```python
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers.ollama_provider import OllamaProvider

models = ["llama3.2:1b", "mistral:7b", "phi3:3.8b"]
results = {}

for model_name in models:
    print(f"\n📊 Evaluating {model_name}...")
    provider = OllamaProvider(model=model_name)

    # Use sampling for reasonable runtime
    runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=100)
    results[model_name] = runner.run_all_benchmarks()

# Print comparison
print("\n" + "="*60)
print("Model Comparison (100-question samples)")
print("="*60)
for name, result in results.items():
    print(f"\n{name}:")
    print(f"  MMLU:       {result['mmlu']['mmlu_accuracy']:.1%}")
    print(f"  TruthfulQA: {result['truthfulqa']['truthfulness_score']:.1%}")
    print(f"  HellaSwag:  {result['hellaswag']['hellaswag_accuracy']:.1%}")
    print(f"  Aggregate:  {result['aggregate_benchmark_score']:.1%}")
```

### Example 3: Production Evaluation

```python
# For publication-ready results
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=None)

print("⚠️  Starting FULL evaluation (will take hours)...")
results = runner.run_all_benchmarks()

print(f"\n✅ PRODUCTION RESULTS:")
print(f"MMLU:       {results['mmlu']['mmlu_accuracy']:.1%} (n={results['mmlu']['questions_tested']})")
print(f"TruthfulQA: {results['truthfulqa']['truthfulness_score']:.1%} (n={results['truthfulqa']['questions_tested']})")
print(f"HellaSwag:  {results['hellaswag']['hellaswag_accuracy']:.1%} (n={results['hellaswag']['questions_tested']})")
```

## 📦 Installation

The `datasets` library is already in `requirements.txt`:

```bash
pip install -e .
```

Or install separately:

```bash
pip install datasets
```

## 🎮 Interactive Demo

Run the interactive demo script:

```bash
python examples/demo_full_benchmarks.py
```

Choose from:

1. **Sampling mode** (100 questions, ~5-10 min) [RECOMMENDED]
2. **Complete datasets** (ALL questions, ~2-8 hours)
3. **Compare demo vs real data**

## ⚡ Performance Tips

### For Faster Evaluation

1. **Use smaller sample sizes** during development:

   ```python
   runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=20)
   ```

2. **Use faster models** for initial testing:

   ```python
   provider = OllamaProvider(model="llama3.2:1b")  # Faster
   # vs
   provider = OllamaProvider(model="deepseek:33b")  # Slower but more accurate
   ```

3. **Increase timeout for large models**:
   ```python
   config = GenerationConfig(timeout_seconds=60)  # Default: 30
   provider = OllamaProvider(model="llama3.2:1b", config=config)
   ```

### For GPU Acceleration

If you have a GPU, make sure Ollama is using it:

```bash
# Check GPU usage
nvidia-smi  # Linux/Windows with NVIDIA
# or
ollama list  # Should show GPU in output
```

## 📊 Result Structure

All benchmarks return detailed results:

```python
{
    'mmlu_accuracy': 0.68,           # Accuracy score (0-1)
    'questions_tested': 100,         # Number of questions evaluated
    'correct': 68,                   # Number of correct answers
    'total_available': 14042,        # Total questions in dataset
    'mode': 'sample_100'             # Mode used ('demo', 'full', or 'sample_N')
}
```

## 🔄 Backward Compatibility

Old code continues to work without changes:

```python
# Old way (still works - uses demo mode)
runner = BenchmarkRunner(provider)
results = runner.run_all_benchmarks()

# New way (explicit)
runner = BenchmarkRunner(provider, use_full_datasets=False)
results = runner.run_all_benchmarks()
```

## ✅ Validation Status

| Aspect                 | Status                                      |
| ---------------------- | ------------------------------------------- |
| MMLU Dataset           | ✅ Loads from HuggingFace `cais/mmlu`       |
| TruthfulQA Dataset     | ✅ Loads from HuggingFace `truthful_qa`     |
| HellaSwag Dataset      | ✅ Loads from HuggingFace `Rowan/hellaswag` |
| Backward Compatibility | ✅ Old code works unchanged                 |
| Unit Tests             | ✅ Full test coverage                       |
| Academic Validity      | ✅ Production-ready (full mode)             |

## 🎯 Use Case Recommendations

| Use Case                    | Recommended Mode | Sample Size | Runtime   |
| --------------------------- | ---------------- | ----------- | --------- |
| **Development/Debugging**   | Demo             | N/A         | 30 sec    |
| **Quick Model Comparison**  | Sampling         | 50-100      | 5-10 min  |
| **Validation Testing**      | Sampling         | 500-1000    | 30-60 min |
| **Research Paper**          | Full             | None        | 2-8 hours |
| **Production Benchmarking** | Full             | None        | 2-8 hours |

## 🐛 Troubleshooting

### "datasets library not available"

```bash
pip install datasets
```

### "Dataset download failed"

Check internet connection. Datasets are cached after first download in `~/.cache/huggingface/datasets/`

### Timeout errors with large models

```python
config = GenerationConfig(
    timeout_seconds=120,  # Increase timeout
    retry_attempts=5      # More retries
)
```

### Out of memory errors

Use smaller sample size or smaller model:

```python
runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=20)
```

## 📚 References

- MMLU Paper: [Measuring Massive Multitask Language Understanding](https://arxiv.org/abs/2009.03300)
- TruthfulQA Paper: [TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://arxiv.org/abs/2109.07958)
- HellaSwag Paper: [HellaSwag: Can a Machine Really Finish Your Sentence?](https://arxiv.org/abs/1905.07830)

## 🤝 Contributing

To add more benchmarks:

1. Add dataset loader in `benchmarks.py`:

   ```python
   @lru_cache(maxsize=1)
   def _load_your_dataset():
       return load_dataset('your/dataset')
   ```

2. Add demo and full methods
3. Update `run_all_benchmarks()`
4. Add tests in `tests/test_full_benchmarks.py`

## 📝 License

MIT - Same as main project
