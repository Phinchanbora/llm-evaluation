# Academic Usage Guide

## Overview

LLM Evaluation Suite v2.0 provides **publication-quality** evaluation capabilities designed for academic papers. This guide covers statistical rigor, baseline comparisons, and proper reporting formats.

## Key Features for Academic Use

### 1. Statistical Rigor

All metrics include:
- **95% Confidence Intervals** (Wilson score method)
- **Standard Error calculations**
- **Bootstrap confidence intervals** for complex metrics
- **McNemar's test** for statistical significance between models

### 2. Published Baselines

Compare your results against documented performance from:
- GPT-4 (OpenAI, 2023)
- Claude 3 Opus (Anthropic, 2024)
- Llama 3 70B (Meta, 2024)
- Gemini Pro (Google, 2024)
- Mistral Large (Mistral AI, 2024)

### 3. Error Analysis

Comprehensive error categorization:
- Knowledge gaps
- Reasoning failures
- Format/parsing errors
- Calibration metrics (Expected Calibration Error)
- Inter-rater agreement (Cohen's Kappa)

### 4. Export Formats

- **LaTeX tables** ready for papers
- **BibTeX citations** for benchmarks
- **Reproducibility manifests** for appendices

---

## Quick Start

### Command Line

```bash
# Basic academic evaluation
llm-eval academic --model llama3.2:1b --sample-size 500

# Full export with LaTeX and BibTeX
llm-eval academic --model gpt-4 --provider openai \
    --output-latex results.tex \
    --output-bibtex citations.bib \
    --output-json results.json
```

### Python API

```python
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.openai_provider import OpenAIProvider
from llm_evaluator.export import export_to_latex, generate_bibtex

# Setup
provider = OpenAIProvider(model="gpt-4")
evaluator = ModelEvaluator(provider=provider)

# Run academic evaluation
results = evaluator.evaluate_all_academic(
    sample_size=500,
    compare_baselines=True
)

# Access results with confidence intervals
print(f"MMLU: {results.mmlu_accuracy:.1%}")
print(f"95% CI: [{results.mmlu_ci[0]:.1%}, {results.mmlu_ci[1]:.1%}]")

# Compare to baselines
for baseline, comparison in results.baseline_comparison.items():
    print(f"vs {baseline}: {comparison['difference']:+.1%}")
```

---

## Statistical Methods

### Wilson Score Confidence Intervals

We use the **Wilson score interval** for binomial proportions, which is preferred over the normal approximation for:
- Small sample sizes (n < 100)
- Proportions near 0 or 1
- Asymmetric confidence bounds

```python
from llm_evaluator.statistical_metrics import calculate_wilson_ci

accuracy = 0.85
n_samples = 100
lower, upper = calculate_wilson_ci(accuracy, n_samples, confidence=0.95)
# Returns: (0.766, 0.908)
```

### Bootstrap Confidence Intervals

For complex metrics (e.g., F1 score, calibration error):

```python
from llm_evaluator.statistical_metrics import bootstrap_confidence_interval

scores = [0.8, 0.9, 0.75, 0.85, 0.92]
lower, upper = bootstrap_confidence_interval(
    scores, 
    statistic=np.mean,
    n_bootstrap=10000,
    confidence=0.95
)
```

### McNemar's Test

For comparing two models on the same test set:

```python
from llm_evaluator.statistical_metrics import mcnemar_test

# model_a_correct[i] = True if model A got question i correct
# model_b_correct[i] = True if model B got question i correct
statistic, p_value, significant = mcnemar_test(
    model_a_correct, 
    model_b_correct,
    alpha=0.05
)

if significant:
    print("Models are significantly different (p < 0.05)")
```

### Effect Size (Cohen's h)

Measure practical significance between proportions:

```python
from llm_evaluator.statistical_metrics import cohens_h

p1 = 0.85  # Model A accuracy
p2 = 0.80  # Model B accuracy
h = cohens_h(p1, p2)

# Interpretation:
# |h| < 0.2: Small effect
# 0.2 ≤ |h| < 0.5: Medium effect
# |h| ≥ 0.5: Large effect
```

---

## Baseline Comparison

### Available Baselines

```python
from llm_evaluator.academic_baselines import ACADEMIC_BASELINES

for model_name, data in ACADEMIC_BASELINES.items():
    print(f"{model_name}:")
    print(f"  MMLU: {data['mmlu']:.1%}")
    print(f"  TruthfulQA: {data['truthfulqa']:.1%}")
    print(f"  Reference: {data['reference']}")
```

### Comparing Your Model

```python
from llm_evaluator.academic_baselines import compare_to_baseline

your_results = {
    "mmlu": 0.78,
    "truthfulqa": 0.65,
    "hellaswag": 0.82
}

comparison = compare_to_baseline(your_results, "gpt-4")
# Returns:
# {
#     "mmlu_difference": -0.084,      # 8.4% lower than GPT-4
#     "truthfulqa_difference": -0.08, # 8% lower
#     "hellaswag_difference": -0.14   # 14% lower
# }
```

---

## Error Analysis

### Categorizing Errors

```python
from llm_evaluator.error_analysis import ErrorAnalyzer

analyzer = ErrorAnalyzer()

for question, expected, actual, confidence in results:
    if expected != actual:
        analyzer.add_error(
            question=question,
            expected=expected,
            actual=actual,
            confidence=confidence
        )

# Get error breakdown
summary = analyzer.get_summary()
print(f"Total errors: {summary['total_errors']}")
print(f"By category: {summary['categories']}")
```

### Expected Calibration Error (ECE)

Measures if model confidence matches actual accuracy:

```python
from llm_evaluator.error_analysis import expected_calibration_error

# confidences[i] = model's confidence for question i
# correctness[i] = 1 if correct, 0 if wrong
ece = expected_calibration_error(confidences, correctness, n_bins=10)
# ECE close to 0 = well-calibrated
# ECE > 0.1 = poorly calibrated
```

---

## Export for Papers

### LaTeX Tables

```python
from llm_evaluator.export import export_to_latex

results = {
    "mmlu_accuracy": 0.85,
    "mmlu_ci": (0.82, 0.88),
    "truthfulqa_score": 0.72,
    "truthfulqa_ci": (0.68, 0.76),
    "hellaswag_accuracy": 0.89,
    "hellaswag_ci": (0.86, 0.92),
}

latex = export_to_latex(results, model_name="Our Model")
print(latex)
```

Output:
```latex
\begin{table}[h]
\centering
\caption{Benchmark Results for Our Model}
\begin{tabular}{lcc}
\toprule
\textbf{Benchmark} & \textbf{Score} & \textbf{95\% CI} \\
\midrule
MMLU & 85.0\% & [82.0\%, 88.0\%] \\
TruthfulQA & 72.0\% & [68.0\%, 76.0\%] \\
HellaSwag & 89.0\% & [86.0\%, 92.0\%] \\
\bottomrule
\end{tabular}
\end{table}
```

### BibTeX Citations

```python
from llm_evaluator.export import generate_bibtex

bibtex = generate_bibtex()
# Returns citations for MMLU, TruthfulQA, HellaSwag papers
```

### Reproducibility Manifest

```python
from llm_evaluator.export import generate_reproducibility_manifest

manifest = generate_reproducibility_manifest(
    model="llama3.2:1b",
    provider="ollama",
    sample_size=500,
    random_seed=42,
    results=results
)
# Includes: timestamp, package version, hardware info, all parameters
```

---

## Best Practices for Papers

### 1. Sample Size

- **Minimum**: 100 samples per benchmark (for reasonable CIs)
- **Recommended**: 500+ samples
- **Full benchmark**: Use `--full` flag (24,901 questions)

### 2. Reporting Format

Always report:
```
MMLU: 85.0% (95% CI: [82.0%, 88.0%], n=500)
```

### 3. Statistical Significance

When comparing models:
```
Model A vs Model B: Δ = +5.2% (p < 0.001, McNemar's test)
Effect size: Cohen's h = 0.32 (medium)
```

### 4. Reproducibility

Include in appendix:
- Package version
- Random seed
- Sample size
- Provider configuration
- Full reproducibility manifest

### 5. Citation

```bibtex
@software{llm_evaluation_suite,
  title = {LLM Evaluation Suite},
  version = {2.0.0},
  year = {2024},
  url = {https://github.com/yourusername/llm-evaluation}
}
```

---

## Example Paper Methods Section

```python
from llm_evaluator.export import generate_methods_section

methods = generate_methods_section(
    model="llama3.2:1b",
    sample_size=500,
    benchmarks=["mmlu", "truthfulqa", "hellaswag"]
)
print(methods)
```

Output:
> We evaluated model performance using the LLM Evaluation Suite (v2.0.0). 
> We report accuracy on MMLU (Hendrycks et al., 2021), TruthfulQA 
> (Lin et al., 2022), and HellaSwag (Zellers et al., 2019). All metrics 
> include 95% Wilson score confidence intervals computed over n=500 
> samples per benchmark. Statistical comparisons use McNemar's test 
> with α=0.05.

---

## Complete Example

See `examples/academic_evaluation.py` for a full working example that:
1. Runs evaluation with proper sample size
2. Compares against published baselines
3. Performs error analysis
4. Exports LaTeX tables and BibTeX
5. Generates reproducibility manifest
