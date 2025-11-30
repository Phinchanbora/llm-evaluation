"""
Main ModelEvaluator class for comprehensive LLM testing

Refactored with Clean Architecture principles:
- Dependency Injection for LLM providers
- Separation of concerns
- Comprehensive error handling
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from .providers import LLMProvider, GenerationConfig, ProviderError
from .providers.ollama_provider import OllamaProvider
from .metrics import PerformanceMetrics, QualityMetrics
from .benchmarks import BenchmarkRunner

logger = logging.getLogger(__name__)


@dataclass
class DetailedMetrics:
    """Strongly typed detailed metrics (no Any types)"""
    
    performance: Dict[str, float] = field(default_factory=lambda: {})
    quality: Dict[str, float] = field(default_factory=lambda: {})
    benchmarks: Dict[str, float] = field(default_factory=lambda: {})
    errors: List[str] = field(default_factory=lambda: [])


@dataclass
class EvaluationResults:
    """Container for evaluation results"""

    model_name: str
    accuracy: float
    avg_response_time: float
    token_efficiency: float
    hallucination_rate: float
    coherence_score: float
    overall_score: float
    detailed_metrics: DetailedMetrics


class ModelEvaluator:
    """
    Comprehensive LLM evaluation framework with Dependency Injection
    
    Refactored to use LLMProvider interface, enabling:
    - Easy provider swapping (Ollama, OpenAI, etc.)
    - Proper testing with mocks
    - Clean separation of concerns
    - Robust error handling

    Args:
        provider: LLM provider implementation (default: OllamaProvider)
        config: Generation configuration

    Example:
        >>> from llm_evaluator.providers.ollama_provider import OllamaProvider
        >>> provider = OllamaProvider(model="llama3.2:1b")
        >>> evaluator = ModelEvaluator(provider=provider)
        >>> results = evaluator.evaluate_all()
        >>> print(f"Overall Score: {results.overall_score:.2f}")
    """

    def __init__(
        self, 
        provider: Optional[LLMProvider] = None,
        config: Optional[GenerationConfig] = None
    ):
        """
        Initialize evaluator with dependency injection
        
        Args:
            provider: LLM provider instance (defaults to Ollama)
            config: Generation configuration
        """
        # Default to Ollama if no provider specified (backwards compatibility)
        self.provider = provider or OllamaProvider(model="llama3.2:1b", config=config)
        self.config = config or GenerationConfig()
        self.performance_metrics = PerformanceMetrics()
        self.quality_metrics = QualityMetrics()
        self.benchmark_runner = BenchmarkRunner(self.provider)

    def chat(self, prompt: str) -> tuple[str, float]:
        """
        Send prompt to LLM and return response with timing
        
        Now uses provider abstraction with error handling

        Args:
            prompt: User prompt to send to the model

        Returns:
            (response_text, response_time_in_seconds)
            
        Raises:
            ProviderError: If generation fails after retries
        """
        try:
            result = self.provider.generate(prompt, self.config)
            return result.text, result.response_time
        except ProviderError as e:
            logger.error(f"Provider error in chat: {e}")
            raise

    def evaluate_performance(self, num_samples: int = 10) -> Dict[str, float]:
        """
        Evaluate performance metrics: response time, token efficiency
        
        Now uses batch generation for better performance

        Args:
            num_samples: Number of test prompts to run

        Returns:
            Dictionary with performance metrics
            
        Raises:
            ProviderError: If generation fails
        """
        test_prompts = [
            "What is Python?",
            "Explain machine learning in one sentence.",
            "What is 2+2?",
            "Name three programming languages.",
            "What is the capital of France?",
            "Define artificial intelligence.",
            "What is a neural network?",
            "Explain what an API is.",
            "What does CPU stand for?",
            "What is cloud computing?",
        ][:num_samples]

        try:
            # Use batch generation for better efficiency
            results = self.provider.generate_batch(test_prompts, self.config)
            
            response_times = [r.response_time for r in results]
            token_counts = [r.token_count or len(r.text) / 4 for r in results]  # Fallback estimate

            return {
                "avg_response_time": sum(response_times) / len(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "avg_tokens_per_response": sum(token_counts) / len(token_counts),
                "tokens_per_second": sum(token_counts) / sum(response_times),
            }
        except ProviderError as e:
            logger.error(f"Performance evaluation failed: {e}")
            raise

    def evaluate_quality(self, test_set: Optional[List[Dict[str, str]]] = None) -> Dict[str, float]:
        """
        Evaluate quality metrics: accuracy, coherence, hallucination
        
        Uses provider interface with error handling

        Args:
            test_set: List of {"prompt": str, "expected": str} dicts

        Returns:
            Dictionary with quality metrics
            
        Raises:
            ProviderError: If generation fails
        """
        if test_set is None:
            # Default test set
            test_set = [
                {"prompt": "What is 5+3?", "expected": "8"},
                {"prompt": "What is the capital of Japan?", "expected": "Tokyo"},
                {"prompt": "How many continents are there?", "expected": "7"},
                {"prompt": "What year did World War 2 end?", "expected": "1945"},
                {"prompt": "What is H2O?", "expected": "water"},
            ]

        correct = 0
        coherent = 0

        try:
            for test in test_set:
                response, _ = self.chat(test["prompt"])

                # Check accuracy (simple substring match)
                if test["expected"].lower() in response.lower():
                    correct += 1

                # Check coherence (basic heuristics)
                if (
                    len(response) > 10
                    and not response.startswith("Error")
                    and response.count(".") <= 10
                ):  # Not too fragmented
                    coherent += 1

            accuracy = correct / len(test_set) if test_set else 0
            coherence = coherent / len(test_set) if test_set else 0

            # Hallucination detection (simplified)
            hallucination_prompts = [
                "Who won the 2025 World Cup?",  # Future event
                "What is the capital of Atlantis?",  # Fictional place
            ]

            hallucinations = 0
            for prompt in hallucination_prompts:
                response, _ = self.chat(prompt)
                # Good model should express uncertainty
                uncertainty_markers = [
                    "don't know",
                    "not sure",
                    "cannot",
                    "no information",
                    "unclear",
                    "uncertain",
                ]
                if not any(marker in response.lower() for marker in uncertainty_markers):
                    hallucinations += 1

            hallucination_rate = hallucinations / len(hallucination_prompts)

            return {
                "accuracy": accuracy,
                "coherence_score": coherence,
                "hallucination_rate": hallucination_rate,
            }
        except ProviderError as e:
            logger.error(f"Quality evaluation failed: {e}")
            raise

    def evaluate_all(self) -> EvaluationResults:
        """
        Run comprehensive evaluation across all metrics
        
        With proper error handling and logging

        Returns:
            EvaluationResults object with all metrics
            
        Raises:
            ProviderError: If evaluation fails
        """
        model_name = self.provider.model
        logger.info(f"Starting comprehensive evaluation for {model_name}")
        
        print(f"\n🔍 Evaluating {model_name}...")
        print("=" * 60)

        errors: List[str] = []
        
        # Performance metrics
        print("\n📊 Performance Metrics...")
        try:
            perf_metrics = self.evaluate_performance()
        except ProviderError as e:
            logger.error(f"Performance evaluation failed: {e}")
            errors.append(f"Performance: {str(e)}")
            perf_metrics: Dict[str, float] = {"avg_response_time": 0.0, "tokens_per_second": 0.0}

        # Quality metrics
        print("✅ Quality Metrics...")
        try:
            quality_metrics = self.evaluate_quality()
        except ProviderError as e:
            logger.error(f"Quality evaluation failed: {e}")
            errors.append(f"Quality: {str(e)}")
            quality_metrics: Dict[str, float] = {"accuracy": 0.0, "coherence_score": 0.0, "hallucination_rate": 1.0}

        # Calculate overall score
        # Normalize and combine metrics
        speed_score = min(
            1.0, 2.0 / max(perf_metrics["avg_response_time"], 0.1)
        )  # Faster is better
        accuracy_score = quality_metrics["accuracy"]
        coherence_score = quality_metrics["coherence_score"]
        anti_hallucination_score = 1.0 - quality_metrics["hallucination_rate"]

        overall_score = (
            speed_score * 0.2
            + accuracy_score * 0.3
            + coherence_score * 0.2
            + anti_hallucination_score * 0.3
        )

        results = EvaluationResults(
            model_name=model_name,
            accuracy=quality_metrics["accuracy"],
            avg_response_time=perf_metrics["avg_response_time"],
            token_efficiency=perf_metrics.get("tokens_per_second", 0),
            hallucination_rate=quality_metrics["hallucination_rate"],
            coherence_score=quality_metrics["coherence_score"],
            overall_score=overall_score,
            detailed_metrics=DetailedMetrics(
                performance=perf_metrics,
                quality=quality_metrics,
                benchmarks={},
                errors=errors
            ),
        )

        # Print summary
        print("\n" + "=" * 60)
        print(f"📋 EVALUATION SUMMARY: {model_name}")
        print("=" * 60)
        print(f"  Accuracy:          {results.accuracy:.1%}")
        print(f"  Avg Response Time: {results.avg_response_time:.2f}s")
        print(f"  Token Efficiency:  {results.token_efficiency:.1f} tokens/s")
        print(f"  Hallucination Rate: {results.hallucination_rate:.1%}")
        print(f"  Coherence Score:   {results.coherence_score:.1%}")
        print(f"  Overall Score:     {results.overall_score:.2f}/1.00")
        
        if errors:
            print(f"\n⚠️  Errors encountered: {len(errors)}")
            for error in errors:
                print(f"    - {error}")
        
        print("=" * 60 + "\n")
        
        logger.info(f"Evaluation completed: {model_name} scored {overall_score:.2f}")

        return results

    def generate_report(self, results: EvaluationResults, output: str = "report.md"):
        """
        Generate markdown report from evaluation results
        
        Args:
            results: Evaluation results to report
            output: Output file path
        """
        logger.info(f"Generating report: {output}")
        
        # Build error section outside f-string to avoid Python 3.11 syntax issues
        error_section = ""
        if results.detailed_metrics.errors:
            newline = '\n'
            errors_list = newline.join(f'- {e}' for e in results.detailed_metrics.errors)
            error_section = f'## Errors\n\n{errors_list}'
        
        report = f"""# Evaluation Report: {results.model_name}

## Summary

| Metric | Value |
|--------|-------|
| Accuracy | {results.accuracy:.1%} |
| Avg Response Time | {results.avg_response_time:.2f}s |
| Token Efficiency | {results.token_efficiency:.1f} tokens/s |
| Hallucination Rate | {results.hallucination_rate:.1%} |
| Coherence Score | {results.coherence_score:.1%} |
| **Overall Score** | **{results.overall_score:.2f}/1.00** |

## Performance Details

```
{results.detailed_metrics.performance}
```

## Quality Details

```
{results.detailed_metrics.quality}
```

{error_section}

---
Generated by LLM Evaluator v0.1.0
"""

        with open(output, "w", encoding="utf-8") as f:
            f.write(report)

        logger.info(f"Report saved to {output}")
        print(f"✅ Report saved to: {output}")


if __name__ == "__main__":
    # Quick demo with new provider architecture
    from .providers.ollama_provider import OllamaProvider
    
    provider = OllamaProvider(model="llama3.2:1b")
    evaluator = ModelEvaluator(provider=provider)
    results = evaluator.evaluate_all()
    evaluator.generate_report(results)
