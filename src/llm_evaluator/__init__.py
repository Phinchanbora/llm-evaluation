"""
LLM Evaluation Suite

A production-ready framework for comprehensive evaluation of Large Language Models.

Key Features:
- Performance Metrics: Response time, throughput, token efficiency
- Quality Metrics: Accuracy, coherence, hallucination detection
- Standard Benchmarks: MMLU (14,042), TruthfulQA (817), HellaSwag (10,042)
- Interactive Visualizations: Dashboards, radar charts, heatmaps
- Clean Architecture: Provider abstraction, dependency injection

Quick Start:
    >>> from llm_evaluator import ModelEvaluator
    >>> from llm_evaluator.providers.ollama_provider import OllamaProvider
    >>> 
    >>> provider = OllamaProvider(model="llama3.2:1b")
    >>> evaluator = ModelEvaluator(provider=provider)
    >>> results = evaluator.evaluate_all()
    >>> print(f"Score: {results.overall_score:.1%}")
    Score: 73.5%

Advanced Usage:
    >>> # Compare multiple models
    >>> from llm_evaluator import quick_comparison
    >>> 
    >>> results = {
    ...     "llama3.2:1b": {"mmlu": 0.65, "accuracy": 0.75},
    ...     "mistral:7b": {"mmlu": 0.78, "accuracy": 0.82}
    ... }
    >>> quick_comparison(results, output_dir="outputs")
    
    >>> # Full benchmark evaluation
    >>> from llm_evaluator.benchmarks import BenchmarkRunner
    >>> 
    >>> runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=100)
    >>> benchmark_results = runner.run_all_benchmarks()
    >>> print(f"MMLU: {benchmark_results['mmlu_accuracy']:.1%}")
    MMLU: 67.3%

Examples: examples/demo.py
Documentation: docs/
Repository: https://github.com/NahuelGiudizi/llm-evaluation
"""

__version__ = "1.0.0"
__author__ = "Nahuel Giudizi"
__license__ = "MIT"

from .evaluator import ModelEvaluator, EvaluationResults
from .metrics import PerformanceMetrics, QualityMetrics
from .benchmarks import BenchmarkRunner
from .visualizations import EvaluationVisualizer, quick_comparison
from .providers import LLMProvider, GenerationConfig, ProviderError

__all__ = [
    "ModelEvaluator",
    "EvaluationResults",
    "PerformanceMetrics",
    "QualityMetrics",
    "BenchmarkRunner",
    "EvaluationVisualizer",
    "quick_comparison",
    "LLMProvider",
    "GenerationConfig",
    "ProviderError",
]
