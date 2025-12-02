# 📘 API Reference

> Complete reference for all public classes, functions, and types in `llm-benchmark-toolkit`.

**Navigation:** [← README](../README.md) | [Quick Start](QUICKSTART.md) | [Providers](PROVIDERS.md) | [Academic Usage](ACADEMIC_USAGE.md)

---

## Table of Contents

- [Core Classes](#core-classes)
  - [ModelEvaluator](#modelevaluator)
  - [BenchmarkRunner](#benchmarkrunner)
  - [EvaluationResults](#evaluationresults)
  - [AcademicEvaluationResults](#academicevaluationresults)
- [Providers](#providers)
  - [LLMProvider (Base)](#llmprovider-base)
  - [OllamaProvider](#ollamaprovider)
  - [OpenAIProvider](#openaiprovider)
  - [AnthropicProvider](#anthropicprovider)
  - [DeepSeekProvider](#deepseekprovider)
  - [HuggingFaceProvider](#huggingfaceprovider)
  - [CachedProvider](#cachedprovider)
- [Configuration](#configuration)
  - [GenerationConfig](#generationconfig)
  - [GenerationResult](#generationresult)
- [Statistical Functions](#statistical-functions)
- [Export Functions](#export-functions)
- [Visualization](#visualization)
- [Errors](#errors)

---

## Core Classes

### ModelEvaluator

Main class for comprehensive LLM evaluation.

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers import OllamaProvider

provider = OllamaProvider(model="llama3.2:1b")
evaluator = ModelEvaluator(provider=provider)
```

#### Constructor

```python
ModelEvaluator(
    provider: Optional[LLMProvider] = None,
    config: Optional[GenerationConfig] = None
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `LLMProvider` | `OllamaProvider` | LLM provider instance |
| `config` | `GenerationConfig` | `None` | Generation configuration |

#### Methods

##### `evaluate_all()`

Run complete evaluation suite.

```python
results = evaluator.evaluate_all()
print(f"Overall: {results.overall_score:.1%}")
```

**Returns:** `EvaluationResults`

##### `evaluate_all_academic()`

Run academic-grade evaluation with statistical rigor.

```python
results = evaluator.evaluate_all_academic(
    sample_size=500,
    compare_baselines=True
)
print(f"MMLU: {results.mmlu_accuracy:.1%}")
print(f"95% CI: [{results.mmlu_ci[0]:.1%}, {results.mmlu_ci[1]:.1%}]")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sample_size` | `int` | `100` | Questions per benchmark |
| `compare_baselines` | `bool` | `True` | Compare to GPT-4, Claude, etc. |

**Returns:** `AcademicEvaluationResults`

##### `run_benchmark()`

Run a specific benchmark.

```python
mmlu_result = evaluator.run_benchmark("mmlu", sample_size=100)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `benchmark` | `str` | One of: `"mmlu"`, `"truthfulqa"`, `"hellaswag"` |
| `sample_size` | `int` | Number of questions |

---

### BenchmarkRunner

Direct access to benchmark datasets.

```python
from llm_evaluator.benchmarks import BenchmarkRunner

runner = BenchmarkRunner(
    provider=provider,
    use_full_datasets=True,
    sample_size=100
)
```

#### Constructor

```python
BenchmarkRunner(
    provider: LLMProvider,
    use_full_datasets: bool = False,
    sample_size: Optional[int] = None
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `LLMProvider` | Required | LLM provider |
| `use_full_datasets` | `bool` | `False` | Use HuggingFace datasets |
| `sample_size` | `int\|None` | `None` | Questions to sample (`None` = all) |

#### Methods

##### `run_all_benchmarks()`

```python
results = runner.run_all_benchmarks()
print(f"MMLU: {results['mmlu']['mmlu_accuracy']:.1%}")
print(f"TruthfulQA: {results['truthfulqa']['truthfulness_score']:.1%}")
print(f"HellaSwag: {results['hellaswag']['hellaswag_accuracy']:.1%}")
```

##### `run_mmlu_full()` / `run_mmlu_sample()`

```python
mmlu = runner.run_mmlu_full()  # All 14,042 questions
mmlu = runner.run_mmlu_sample()  # Sampled questions
```

##### `run_truthfulqa_full()` / `run_truthfulqa_sample()`

```python
tqa = runner.run_truthfulqa_full()  # All 817 questions
```

##### `run_hellaswag_full()` / `run_hellaswag_sample()`

```python
hs = runner.run_hellaswag_full()  # All 10,042 scenarios
```

---

### EvaluationResults

Container for standard evaluation results.

```python
@dataclass
class EvaluationResults:
    model_name: str
    accuracy: float
    avg_response_time: float
    token_efficiency: float
    hallucination_rate: float
    coherence_score: float
    overall_score: float
    detailed_metrics: DetailedMetrics
    system_info: Optional[Dict[str, Any]]
```

---

### AcademicEvaluationResults

Academic-grade results with confidence intervals.

```python
@dataclass
class AcademicEvaluationResults:
    model_name: str
    # MMLU
    mmlu_accuracy: float
    mmlu_ci: Tuple[float, float]  # 95% CI
    mmlu_se: float                # Standard error
    mmlu_n: int                   # Sample size
    # TruthfulQA
    truthfulqa_accuracy: float
    truthfulqa_ci: Tuple[float, float]
    truthfulqa_se: float
    truthfulqa_n: int
    # HellaSwag
    hellaswag_accuracy: float
    hellaswag_ci: Tuple[float, float]
    hellaswag_se: float
    hellaswag_n: int
    # Aggregate
    average_accuracy: float
    baseline_comparison: Dict[str, Any]
    reproducibility_manifest: Dict[str, Any]
```

#### Methods

##### `to_dict()`

Convert to JSON-serializable dictionary.

```python
data = results.to_dict()
json.dump(data, open("results.json", "w"))
```

---

## Providers

### LLMProvider (Base)

Abstract base class for all providers.

```python
from llm_evaluator.providers import LLMProvider

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> GenerationResult:
        """Generate text from prompt."""
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return model identifier."""
        pass
    
    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        """Return provider type enum."""
        pass
```

---

### OllamaProvider

Local LLM provider using Ollama.

```python
from llm_evaluator.providers import OllamaProvider

provider = OllamaProvider(
    model="llama3.2:1b",
    base_url="http://localhost:11434",
    config=GenerationConfig(temperature=0.7)
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | Required | Model name (e.g., `"llama3.2:1b"`) |
| `base_url` | `str` | `"http://localhost:11434"` | Ollama API URL |
| `config` | `GenerationConfig` | `None` | Generation settings |

**Supported models:** Any model available via `ollama list`

---

### OpenAIProvider

OpenAI API provider.

```python
from llm_evaluator.providers import OpenAIProvider

provider = OpenAIProvider(
    model="gpt-4o-mini",
    api_key="sk-..."  # Or set OPENAI_API_KEY env var
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | `"gpt-4o-mini"` | Model name |
| `api_key` | `str` | `None` | API key (uses env if not set) |
| `config` | `GenerationConfig` | `None` | Generation settings |

**Supported models:** `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-3.5-turbo`

---

### AnthropicProvider

Anthropic Claude API provider.

```python
from llm_evaluator.providers import AnthropicProvider

provider = AnthropicProvider(
    model="claude-3-5-sonnet-20241022",
    api_key="sk-ant-..."  # Or set ANTHROPIC_API_KEY env var
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | `"claude-3-5-sonnet-20241022"` | Model name |
| `api_key` | `str` | `None` | API key |
| `config` | `GenerationConfig` | `None` | Generation settings |

**Supported models:** `claude-3-5-sonnet-*`, `claude-3-opus-*`, `claude-3-haiku-*`

---

### DeepSeekProvider

DeepSeek API provider (OpenAI-compatible).

```python
from llm_evaluator.providers import DeepSeekProvider

provider = DeepSeekProvider(
    model="deepseek-chat",
    api_key="sk-..."  # Or set DEEPSEEK_API_KEY env var
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | `"deepseek-chat"` | Model name |
| `api_key` | `str` | `None` | API key |

**Supported models:** `deepseek-chat`, `deepseek-coder`, `deepseek-reasoner`

---

### HuggingFaceProvider

HuggingFace Inference API provider.

```python
from llm_evaluator.providers import HuggingFaceProvider

provider = HuggingFaceProvider(
    model="meta-llama/Llama-2-7b-chat-hf",
    api_key="hf_..."  # Or set HF_TOKEN env var
)
```

---

### CachedProvider

Wrapper that adds caching to any provider.

```python
from llm_evaluator.providers import CachedProvider, OllamaProvider

base_provider = OllamaProvider(model="llama3.2:1b")
provider = CachedProvider(
    provider=base_provider,
    cache_dir="~/.cache/llm-eval"
)

# Check cache stats
stats = provider.get_cache_stats()
print(f"Hit rate: {stats['hit_rate_percent']:.1f}%")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | `LLMProvider` | Required | Base provider to wrap |
| `cache_dir` | `str` | `"~/.cache/llm-eval"` | Cache directory |

#### Methods

##### `get_cache_stats()`

```python
stats = cached.get_cache_stats()
# Returns: {'hits': 150, 'misses': 50, 'hit_rate_percent': 75.0}
```

##### `clear_cache()`

```python
cached.clear_cache()
```

---

## Configuration

### GenerationConfig

Configuration for text generation.

```python
from llm_evaluator.providers import GenerationConfig

config = GenerationConfig(
    temperature=0.7,
    max_tokens=512,
    top_p=0.9,
    top_k=40,
    timeout_seconds=30,
    retry_attempts=3
)
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `temperature` | `float` | `0.7` | Sampling temperature |
| `max_tokens` | `int` | `512` | Max tokens to generate |
| `top_p` | `float` | `0.9` | Nucleus sampling |
| `top_k` | `int` | `40` | Top-k sampling |
| `timeout_seconds` | `int` | `30` | Request timeout |
| `retry_attempts` | `int` | `3` | Retry on failure |

---

### GenerationResult

Result from LLM generation.

```python
@dataclass
class GenerationResult:
    text: str                    # Generated text
    response_time: float         # Seconds
    tokens_used: int             # Total tokens
    model: str                   # Model name
    provider: str                # Provider name
    prompt_tokens: int           # Input tokens
    completion_tokens: int       # Output tokens
    total_tokens: int            # Total tokens
    cost_usd: float              # Estimated cost
    finish_reason: str           # "stop", "length", etc.
    cached: bool                 # From cache?
    error: Optional[str]         # Error message if any
```

---

## Statistical Functions

### calculate_wilson_ci()

Wilson score confidence interval for accuracy.

```python
from llm_evaluator import calculate_wilson_ci

lower, upper = calculate_wilson_ci(
    correct=850,
    total=1000,
    confidence=0.95
)
print(f"95% CI: [{lower:.1%}, {upper:.1%}]")
# Output: 95% CI: [82.7%, 87.1%]
```

### calculate_standard_error()

Standard error for proportion.

```python
from llm_evaluator import calculate_standard_error

se = calculate_standard_error(correct=850, total=1000)
print(f"SE: {se:.4f}")
```

### bootstrap_confidence_interval()

Bootstrap CI for complex metrics.

```python
from llm_evaluator import bootstrap_confidence_interval
import numpy as np

scores = [0.8, 0.9, 0.75, 0.85, 0.92]
lower, upper = bootstrap_confidence_interval(
    scores,
    statistic=np.mean,
    n_bootstrap=10000,
    confidence=0.95
)
```

### mcnemar_test()

McNemar's test for comparing two models.

```python
from llm_evaluator import mcnemar_test

# model_a_correct[i] = True if model A got question i correct
statistic, p_value, significant = mcnemar_test(
    model_a_correct,
    model_b_correct,
    alpha=0.05
)

if significant:
    print("Models are significantly different (p < 0.05)")
```

### cohens_h()

Effect size between two proportions.

```python
from llm_evaluator import cohens_h

h = cohens_h(p1=0.85, p2=0.80)
# h < 0.2: small, 0.2-0.8: medium, > 0.8: large
```

---

## Export Functions

### export_to_latex()

Generate LaTeX table for papers.

```python
from llm_evaluator import export_to_latex

results = {
    'llama3.2': {'mmlu': 0.68, 'mmlu_ci': (0.65, 0.71), 'truthfulqa': 0.55},
    'gpt-4o': {'mmlu': 0.86, 'mmlu_ci': (0.84, 0.88), 'truthfulqa': 0.72}
}

latex = export_to_latex(
    results,
    include_ci=True,
    caption="Benchmark Results",
    label="tab:results"
)
print(latex)
```

### generate_bibtex()

Generate BibTeX citations.

```python
from llm_evaluator import generate_bibtex

bibtex = generate_bibtex()
# Returns citations for MMLU, TruthfulQA, HellaSwag papers
```

### generate_reproducibility_manifest()

Generate reproducibility info for papers.

```python
from llm_evaluator import generate_reproducibility_manifest

manifest = generate_reproducibility_manifest(
    model_name="llama3.2:1b",
    sample_size=500
)
# Includes: Python version, package versions, timestamps, etc.
```

---

## Visualization

### EvaluationVisualizer

Create charts and dashboards.

```python
from llm_evaluator import EvaluationVisualizer

viz = EvaluationVisualizer(output_dir="outputs")

# Radar chart
viz.create_radar_chart(results, "llama3.2:1b")

# Comparison bar chart
viz.create_comparison_chart(all_results)

# Full dashboard
viz.create_dashboard(all_results)
```

### quick_comparison()

Quick comparison visualization.

```python
from llm_evaluator import quick_comparison

results = {
    "llama3.2:1b": {"mmlu": 0.65, "truthfulqa": 0.55, "hellaswag": 0.72},
    "mistral:7b": {"mmlu": 0.78, "truthfulqa": 0.62, "hellaswag": 0.81}
}

quick_comparison(results, output_dir="outputs")
# Creates: comparison.png, radar.png
```

---

## Errors

### ProviderError

Base exception for all provider errors.

```python
from llm_evaluator.providers import ProviderError

try:
    result = provider.generate("Hello")
except ProviderError as e:
    print(f"Provider error: {e.message}")
```

### RateLimitError

API rate limit exceeded.

```python
from llm_evaluator.providers import RateLimitError

try:
    result = provider.generate("Hello")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}s")
```

### AuthenticationError

Invalid API key.

```python
from llm_evaluator.providers import AuthenticationError
```

### ModelNotFoundError

Model not available.

```python
from llm_evaluator.providers import ModelNotFoundError
```

### TimeoutError

Request timed out.

```python
from llm_evaluator.providers import TimeoutError
```

---

## Full Example

```python
from llm_evaluator import (
    ModelEvaluator,
    export_to_latex,
    generate_bibtex,
    quick_comparison
)
from llm_evaluator.providers import (
    OllamaProvider,
    OpenAIProvider,
    CachedProvider,
    GenerationConfig
)

# Configure provider with caching
config = GenerationConfig(temperature=0.3, max_tokens=256)
base_provider = OllamaProvider(model="llama3.2:1b", config=config)
provider = CachedProvider(base_provider)

# Run academic evaluation
evaluator = ModelEvaluator(provider=provider)
results = evaluator.evaluate_all_academic(
    sample_size=500,
    compare_baselines=True
)

# Print results with CI
print(f"MMLU: {results.mmlu_accuracy:.1%} ± {results.mmlu_se*100:.1f}%")
print(f"95% CI: [{results.mmlu_ci[0]:.1%}, {results.mmlu_ci[1]:.1%}]")

# Export for paper
latex = export_to_latex(results.to_dict())
bibtex = generate_bibtex()

# Visualize
quick_comparison({"llama3.2": results.to_dict()}, output_dir="figures")
```

---

**Navigation:** [← README](../README.md) | [Quick Start](QUICKSTART.md) | [Providers](PROVIDERS.md) | [Academic Usage](ACADEMIC_USAGE.md)
