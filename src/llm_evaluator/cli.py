"""
CLI tool for LLM Evaluation Suite

Provides command-line interface for running evaluations, comparisons, and visualizations.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

import click

from llm_evaluator import ModelEvaluator
from llm_evaluator.benchmarks import BenchmarkRunner
from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.evaluator import AcademicEvaluationResults
from llm_evaluator.export import export_to_latex, generate_bibtex

# Import optional providers
try:
    from llm_evaluator.providers.openai_provider import OpenAIProvider

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from llm_evaluator.providers.anthropic_provider import AnthropicProvider

    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    from llm_evaluator.providers.huggingface_provider import HuggingFaceProvider

    HAS_HUGGINGFACE = True
except ImportError:
    HAS_HUGGINGFACE = False

try:
    from llm_evaluator.providers.deepseek_provider import DeepSeekProvider

    HAS_DEEPSEEK = True
except ImportError:
    HAS_DEEPSEEK = False

from llm_evaluator.providers.cached_provider import CachedProvider

# Version
__version__ = "2.0.0"


def detect_provider_from_env() -> Tuple[Optional[str], Optional[str]]:
    """
    Auto-detect provider and model from environment variables.
    
    Returns:
        Tuple of (provider_name, suggested_model) or (None, None)
    """
    if os.environ.get("OPENAI_API_KEY"):
        return ("openai", "gpt-4o-mini")
    if os.environ.get("ANTHROPIC_API_KEY"):
        return ("anthropic", "claude-3-5-sonnet-20241022")
    if os.environ.get("DEEPSEEK_API_KEY"):
        return ("deepseek", "deepseek-chat")
    if os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_API_KEY"):
        return ("huggingface", "meta-llama/Llama-2-7b-chat-hf")
    # Check if Ollama is running
    try:
        import requests
        resp = requests.get("http://localhost:11434/api/version", timeout=1)
        if resp.status_code == 200:
            return ("ollama", "llama3.2:1b")
    except Exception:
        pass
    return (None, None)


def echo_success(msg: str) -> None:
    """Print success message in green"""
    click.echo(click.style(f"✅ {msg}", fg="green"))


def echo_error(msg: str) -> None:
    """Print error message in red"""
    click.echo(click.style(f"❌ {msg}", fg="red"), err=True)


def echo_warning(msg: str) -> None:
    """Print warning message in yellow"""
    click.echo(click.style(f"⚠️  {msg}", fg="yellow"))


def echo_info(msg: str) -> None:
    """Print info message in blue"""
    click.echo(click.style(f"ℹ️  {msg}", fg="blue"))


@click.group()
@click.version_option(version=__version__, prog_name="llm-eval")
def cli():
    """
    🚀 LLM Evaluation Suite - Command Line Interface

    Evaluate, compare, and visualize LLM performance across multiple models and benchmarks.

    Examples:
        llm-eval run --model llama3.2:1b
        llm-eval compare --models llama3.2,mistral:7b
        llm-eval benchmark --model gpt-3.5-turbo --provider openai
    """
    pass


def create_provider(model: str, provider_type: str, cache: bool = False):
    """Create provider instance based on type"""

    if provider_type == "ollama":
        base_provider = OllamaProvider(model=model)
    elif provider_type == "openai":
        if not HAS_OPENAI:
            echo_error("OpenAI provider not installed. Run: pip install openai")
            sys.exit(1)
        base_provider = OpenAIProvider(model=model)
    elif provider_type == "anthropic":
        if not HAS_ANTHROPIC:
            echo_error("Anthropic provider not installed. Run: pip install anthropic")
            sys.exit(1)
        base_provider = AnthropicProvider(model=model)
    elif provider_type == "huggingface":
        if not HAS_HUGGINGFACE:
            echo_error("HuggingFace provider not installed. Run: pip install huggingface-hub")
            sys.exit(1)
        base_provider = HuggingFaceProvider(model=model)
    elif provider_type == "deepseek":
        if not HAS_DEEPSEEK:
            echo_error("DeepSeek provider not installed. Run: pip install openai")
            sys.exit(1)
        base_provider = DeepSeekProvider(model=model)
    elif provider_type == "auto":
        # Auto-detect from environment
        detected_provider, detected_model = detect_provider_from_env()
        if detected_provider:
            echo_info(f"Auto-detected provider: {detected_provider} (model: {detected_model})")
            return create_provider(detected_model if model == "auto" else model, detected_provider, cache)
        else:
            echo_error("No provider detected. Set an API key or start Ollama.")
            echo_info("Supported env vars: OPENAI_API_KEY, ANTHROPIC_API_KEY, DEEPSEEK_API_KEY, HF_TOKEN")
            sys.exit(1)
    else:
        echo_error(f"Unknown provider: {provider_type}")
        sys.exit(1)

    # Wrap with cache if requested
    if cache:
        return CachedProvider(base_provider)
    return base_provider


@cli.command()
@click.option("--model", "-m", default=None, help="Model name (auto-detected if not set)")
@click.option("--sample-size", "-s", type=int, default=20, help="Sample size (default: 20)")
@click.option("--output", "-o", default=None, help="Output file (optional)")
def quick(model: Optional[str], sample_size: int, output: Optional[str]):
    """
    🚀 Quick evaluation with zero configuration!

    Auto-detects your provider from environment variables:
    - OPENAI_API_KEY → Uses OpenAI (gpt-4o-mini)
    - ANTHROPIC_API_KEY → Uses Anthropic (claude-3-5-sonnet)
    - DEEPSEEK_API_KEY → Uses DeepSeek (deepseek-chat)
    - HF_TOKEN → Uses HuggingFace
    - Ollama running → Uses Ollama (llama3.2:1b)

    Examples:
        llm-eval quick                      # Auto-detect everything
        llm-eval quick --model gpt-4o       # Use specific model
        llm-eval quick -s 50                # Larger sample size
    """
    click.echo("\n" + "=" * 50)
    click.echo(click.style("🚀 LLM QUICK EVALUATION", fg="cyan", bold=True))
    click.echo("=" * 50)

    # Auto-detect provider
    detected_provider, detected_model = detect_provider_from_env()
    
    if not detected_provider:
        echo_error("No provider detected!")
        click.echo("\n📋 To use quick evaluation, set one of these environment variables:")
        click.echo("   • OPENAI_API_KEY    → For GPT models")
        click.echo("   • ANTHROPIC_API_KEY → For Claude models")  
        click.echo("   • DEEPSEEK_API_KEY  → For DeepSeek models")
        click.echo("   • HF_TOKEN          → For HuggingFace models")
        click.echo("   • Or start Ollama   → ollama serve")
        sys.exit(1)

    # Use provided model or detected one
    use_model = model if model else detected_model
    
    echo_success(f"Provider: {detected_provider}")
    echo_success(f"Model: {use_model}")
    echo_success(f"Sample size: {sample_size}")
    
    click.echo("\n⏳ Starting evaluation...")

    # Create provider with caching
    llm_provider = create_provider(use_model, detected_provider, cache=True)

    if not llm_provider.is_available():
        echo_error(f"Provider {detected_provider} is not responding")
        sys.exit(1)

    # Run benchmarks
    runner = BenchmarkRunner(
        provider=llm_provider,
        use_full_datasets=True,
        sample_size=sample_size
    )

    click.echo("\n📊 Running benchmarks...")
    
    results = {}
    
    with click.progressbar(["mmlu", "truthfulqa", "hellaswag"], label="Progress") as benchmarks:
        for bench in benchmarks:
            if bench == "mmlu":
                results["mmlu"] = runner.run_mmlu_sample()
            elif bench == "truthfulqa":
                results["truthfulqa"] = runner.run_truthfulqa_sample()
            elif bench == "hellaswag":
                results["hellaswag"] = runner.run_hellaswag_sample()

    # Display results
    click.echo("\n" + "=" * 50)
    click.echo(click.style("📊 RESULTS", fg="green", bold=True))
    click.echo("=" * 50)
    
    click.echo(f"\n  🎯 MMLU:       {results.get('mmlu', {}).get('mmlu_accuracy', 0):.1%}")
    click.echo(f"  🎯 TruthfulQA: {results.get('truthfulqa', {}).get('truthfulness_score', 0):.1%}")
    click.echo(f"  🎯 HellaSwag:  {results.get('hellaswag', {}).get('hellaswag_accuracy', 0):.1%}")
    
    # Calculate overall
    scores = [
        results.get('mmlu', {}).get('mmlu_accuracy', 0),
        results.get('truthfulqa', {}).get('truthfulness_score', 0),
        results.get('hellaswag', {}).get('hellaswag_accuracy', 0)
    ]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    click.echo(f"\n  📈 Overall:    {avg_score:.1%}")
    
    # Save if output specified
    if output:
        output_data = {
            "model": use_model,
            "provider": detected_provider,
            "sample_size": sample_size,
            "results": results
        }
        Path(output).write_text(json.dumps(output_data, indent=2))
        echo_success(f"Results saved to: {output}")
    
    # Cache stats
    if isinstance(llm_provider, CachedProvider):
        stats = llm_provider.get_cache_stats()
        click.echo(f"\n  💾 Cache: {stats['hit_rate_percent']:.0f}% hit rate")
    
    click.echo("\n" + "=" * 50)
    click.echo("✨ Evaluation complete!")
    click.echo("=" * 50 + "\n")


@cli.command()
@click.option("--model", "-m", default="llama3.2:1b", help="Model name")
@click.option(
    "--provider",
    "-p",
    default="ollama",
    type=click.Choice(["ollama", "openai", "anthropic", "huggingface", "deepseek", "auto"]),
    help="Provider type",
)
@click.option("--cache/--no-cache", default=True, help="Enable caching")
@click.option("--output", "-o", default="evaluation_report.md", help="Output file")
def run(model: str, provider: str, cache: bool, output: str):
    """
    Run full evaluation on a single model

    Example:
        llm-eval run --model llama3.2:1b --provider ollama
    """
    click.echo(f"🚀 Running evaluation on {model} ({provider})")

    # Create provider
    llm_provider = create_provider(model, provider, cache)

    # Check availability
    if not llm_provider.is_available():
        click.echo(f"❌ Provider not available. Is {provider} running?", err=True)
        sys.exit(1)

    # Run evaluation
    evaluator = ModelEvaluator(provider=llm_provider)

    with click.progressbar(length=3, label="Evaluating") as bar:
        bar.update(1)
        results = evaluator.evaluate_all()
        bar.update(2)

    # Generate report
    evaluator.generate_report(results, output)

    # Print summary
    click.echo("\n✅ Evaluation complete!")
    click.echo(f"📊 Overall Score: {results.overall_score:.1%}")
    click.echo(f"📄 Report saved to: {output}")

    # Show cache stats if caching enabled
    if cache and isinstance(llm_provider, CachedProvider):
        stats = llm_provider.get_cache_stats()
        click.echo("\n💾 Cache Stats:")
        click.echo(f"   Hit rate: {stats['hit_rate_percent']:.1f}%")
        click.echo(f"   Hits: {stats['hits']} | Misses: {stats['misses']}")


@cli.command()
@click.option("--models", "-m", required=True, help="Comma-separated model names")
@click.option(
    "--provider",
    "-p",
    default="ollama",
    type=click.Choice(["ollama", "openai", "anthropic", "huggingface"]),
    help="Provider type (same for all models)",
)
@click.option("--cache/--no-cache", default=True, help="Enable caching")
@click.option("--output", "-o", default="comparison.json", help="Output JSON file")
def compare(models: str, provider: str, cache: bool, output: str):
    """
    Compare multiple models side-by-side

    Example:
        llm-eval compare --models llama3.2:1b,mistral:7b --provider ollama
    """
    model_list = [m.strip() for m in models.split(",")]

    click.echo(f"🔄 Comparing {len(model_list)} models: {', '.join(model_list)}")

    results = {}

    for model in model_list:
        click.echo(f"\n📊 Evaluating {model}...")

        llm_provider = create_provider(model, provider, cache)

        if not llm_provider.is_available():
            click.echo(f"⚠️  {model} not available, skipping", err=True)
            continue

        evaluator = ModelEvaluator(provider=llm_provider)
        eval_results = evaluator.evaluate_all()

        results[model] = {
            "overall_score": eval_results.overall_score,
            "accuracy": eval_results.accuracy,
            "avg_response_time": eval_results.avg_response_time,
            "coherence_score": eval_results.coherence_score,
        }

        click.echo(f"   Overall: {eval_results.overall_score:.1%}")

    # Save results
    Path(output).write_text(json.dumps(results, indent=2))

    # Print comparison table
    click.echo("\n📊 Comparison Results:")
    click.echo(f"{'Model':<30} {'Score':<10} {'Accuracy':<10} {'Speed (s)':<12}")
    click.echo("=" * 70)

    for model_name, data in sorted(
        results.items(), key=lambda x: x[1]["overall_score"], reverse=True
    ):
        click.echo(
            f"{model_name:<30} "
            f"{data['overall_score']:<10.1%} "
            f"{data['accuracy']:<10.1%} "
            f"{data['avg_response_time']:<12.2f}"
        )

    click.echo(f"\n✅ Results saved to: {output}")


@cli.command()
@click.option("--model", "-m", default="llama3.2:1b", help="Model name")
@click.option(
    "--provider",
    "-p",
    default="ollama",
    type=click.Choice(["ollama", "openai", "anthropic", "huggingface"]),
    help="Provider type",
)
@click.option(
    "--benchmarks",
    "-b",
    default="mmlu,truthfulqa,hellaswag",
    help="Comma-separated benchmark names",
)
@click.option("--sample-size", "-s", type=int, help="Sample size (None = demo mode)")
@click.option("--full", is_flag=True, help="Run full benchmarks (24,901 questions)")
@click.option("--cache/--no-cache", default=True, help="Enable caching")
@click.option("--output", "-o", default="benchmark_results.json", help="Output file")
def benchmark(
    model: str,
    provider: str,
    benchmarks: str,
    sample_size: Optional[int],
    full: bool,
    cache: bool,
    output: str,
):
    """
    Run specific benchmarks on a model

    Examples:
        llm-eval benchmark --model llama3.2:1b --benchmarks mmlu
        llm-eval benchmark --model gpt-3.5-turbo --provider openai --sample-size 100
        llm-eval benchmark --model llama3.2:1b --full  # Warning: takes hours!
    """
    click.echo(f"📊 Running benchmarks on {model} ({provider})")

    if full and not click.confirm("⚠️  Full benchmarks take 2-8 hours. Continue?"):
        click.echo("Aborted.")
        sys.exit(0)

    # Create provider
    llm_provider = create_provider(model, provider, cache)

    if not llm_provider.is_available():
        click.echo(f"❌ Provider not available. Is {provider} running?", err=True)
        sys.exit(1)

    # Setup benchmark runner
    use_full = full or (sample_size is not None)
    runner = BenchmarkRunner(
        provider=llm_provider, use_full_datasets=use_full, sample_size=None if full else sample_size
    )

    # Parse benchmarks
    benchmark_list = [b.strip() for b in benchmarks.split(",")]

    results = {}

    for bench in benchmark_list:
        click.echo(f"\n🎯 Running {bench.upper()}...")

        if bench == "mmlu":
            results["mmlu"] = runner.run_mmlu_sample()
        elif bench == "truthfulqa":
            results["truthfulqa"] = runner.run_truthfulqa_sample()
        elif bench == "hellaswag":
            results["hellaswag"] = runner.run_hellaswag_sample()
        else:
            click.echo(f"⚠️  Unknown benchmark: {bench}", err=True)
            continue

        # Print result
        accuracy_key = f"{bench}_accuracy" if bench != "truthfulqa" else "truthfulness_score"
        if accuracy_key in results[bench]:
            click.echo(f"   Accuracy: {results[bench][accuracy_key]:.1%}")

    # Save results
    Path(output).write_text(json.dumps(results, indent=2))
    click.echo(f"\n✅ Results saved to: {output}")

    # Show cache stats
    if cache and isinstance(llm_provider, CachedProvider):
        stats = llm_provider.get_cache_stats()
        click.echo(f"\n💾 Cache Stats: {stats['hit_rate_percent']:.1f}% hit rate")


@cli.command()
@click.argument("results_file", type=click.Path(exists=True))
@click.option("--output", "-o", default="visualization.html", help="Output HTML file")
def visualize(results_file: str, output: str):
    """
    Generate interactive visualizations from results

    Example:
        llm-eval visualize comparison.json --output dashboard.html
    """
    click.echo(f"📈 Generating visualizations from {results_file}")

    # TODO: Implement visualization generation
    # This would use the visualizations.py module to create charts
    # data = json.loads(Path(results_file).read_text())

    click.echo("⚠️  Visualization feature coming soon!")
    click.echo("For now, use: from llm_evaluator.visualizations import EvaluationVisualizer")


@cli.command()
def providers():
    """List available providers and their status"""
    click.echo("\n🔌 Available Providers:\n")

    # Auto-detection status
    detected_provider, detected_model = detect_provider_from_env()
    if detected_provider:
        echo_success(f"Auto-detected: {detected_provider} ({detected_model})")
        click.echo("")

    providers_status = [
        ("ollama", True, "Local LLMs (llama3.2, mistral, etc.)"),
        ("openai", HAS_OPENAI, "GPT-3.5, GPT-4, GPT-4o (pip install openai)"),
        ("anthropic", HAS_ANTHROPIC, "Claude 3/3.5 (pip install anthropic)"),
        ("deepseek", HAS_DEEPSEEK, "DeepSeek-V3, DeepSeek-R1 (pip install openai)"),
        ("huggingface", HAS_HUGGINGFACE, "Inference API (pip install huggingface-hub)"),
    ]

    for name, available, description in providers_status:
        status = "✅" if available else "❌"
        click.echo(f"  {status} {name:<15} - {description}")
    
    click.echo("\n📋 Environment Variables:")
    env_vars = [
        ("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", "")[:8] + "..." if os.environ.get("OPENAI_API_KEY") else "Not set"),
        ("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", "")[:8] + "..." if os.environ.get("ANTHROPIC_API_KEY") else "Not set"),
        ("DEEPSEEK_API_KEY", os.environ.get("DEEPSEEK_API_KEY", "")[:8] + "..." if os.environ.get("DEEPSEEK_API_KEY") else "Not set"),
        ("HF_TOKEN", os.environ.get("HF_TOKEN", "")[:8] + "..." if os.environ.get("HF_TOKEN") else "Not set"),
    ]
    
    for var, value in env_vars:
        status = "✅" if "Not set" not in value else "❌"
        click.echo(f"  {status} {var:<20} {value}")
    
    click.echo("")


@cli.command()
@click.option("--model", "-m", default="llama3.2:1b", help="Model name")
@click.option(
    "--provider",
    "-p",
    default="ollama",
    type=click.Choice(["ollama", "openai", "anthropic", "huggingface", "deepseek", "auto"]),
    help="Provider type",
)
@click.option("--sample-size", "-s", type=int, default=100, help="Sample size for benchmarks")
@click.option("--cache/--no-cache", default=True, help="Enable caching")
@click.option("--output-latex", type=click.Path(), help="Output LaTeX table file")
@click.option("--output-bibtex", type=click.Path(), help="Output BibTeX citations file")
@click.option("--output-json", "-o", default="academic_results.json", help="Output JSON file")
@click.option(
    "--compare-baselines/--no-compare-baselines",
    default=True,
    help="Compare against published baselines",
)
def academic(
    model: str,
    provider: str,
    sample_size: int,
    cache: bool,
    output_latex: Optional[str],
    output_bibtex: Optional[str],
    output_json: str,
    compare_baselines: bool,
):
    """
    Run academic-quality evaluation with statistical rigor

    Produces results suitable for academic papers with:
    - 95% confidence intervals (Wilson method)
    - Comparison against published baselines
    - Error analysis and calibration metrics
    - LaTeX tables and BibTeX citations

    Examples:
        llm-eval academic --model llama3.2:1b --output-latex results.tex
        llm-eval academic --model gpt-4 --provider openai --output-bibtex citations.bib
    """
    click.echo(f"🎓 Running academic evaluation on {model} ({provider})")
    click.echo(f"   Sample size: {sample_size}")
    click.echo(f"   Compare baselines: {compare_baselines}")

    # Create provider
    llm_provider = create_provider(model, provider, cache)

    if not llm_provider.is_available():
        click.echo(f"❌ Provider not available. Is {provider} running?", err=True)
        sys.exit(1)

    # Run academic evaluation
    evaluator = ModelEvaluator(provider=llm_provider)

    click.echo("\n📊 Running benchmarks with statistical analysis...")

    try:
        results: AcademicEvaluationResults = evaluator.evaluate_all_academic(
            sample_size=sample_size,
        )
    except Exception as e:
        click.echo(f"❌ Error during evaluation: {e}", err=True)
        sys.exit(1)

    # Print results summary
    click.echo("\n" + "=" * 60)
    click.echo("📊 ACADEMIC EVALUATION RESULTS")
    click.echo("=" * 60)

    click.echo(f"\n📈 MMLU Accuracy: {results.mmlu_accuracy:.1%}")
    if results.mmlu_ci:
        click.echo(f"   95% CI: [{results.mmlu_ci[0]:.1%}, {results.mmlu_ci[1]:.1%}]")

    click.echo(f"\n📈 TruthfulQA Score: {results.truthfulqa_accuracy:.1%}")
    if results.truthfulqa_ci:
        click.echo(f"   95% CI: [{results.truthfulqa_ci[0]:.1%}, {results.truthfulqa_ci[1]:.1%}]")

    click.echo(f"\n📈 HellaSwag Accuracy: {results.hellaswag_accuracy:.1%}")
    if results.hellaswag_ci:
        click.echo(f"   95% CI: [{results.hellaswag_ci[0]:.1%}, {results.hellaswag_ci[1]:.1%}]")

    # Baseline comparison
    if compare_baselines and results.baseline_comparison:
        click.echo("\n" + "-" * 40)
        click.echo("📊 BASELINE COMPARISON")
        click.echo("-" * 40)
        for baseline_name, comparison in results.baseline_comparison.items():
            diff = comparison.get("difference", 0)
            sign = "+" if diff > 0 else ""
            click.echo(f"   vs {baseline_name}: {sign}{diff:.1%}")

    # Save JSON results
    results_dict = {
        "model": model,
        "provider": provider,
        "sample_size": sample_size,
        "mmlu_accuracy": results.mmlu_accuracy,
        "mmlu_ci": results.mmlu_ci,
        "truthfulqa_accuracy": results.truthfulqa_accuracy,
        "truthfulqa_ci": results.truthfulqa_ci,
        "hellaswag_accuracy": results.hellaswag_accuracy,
        "hellaswag_ci": results.hellaswag_ci,
        "baseline_comparison": results.baseline_comparison,
        "reproducibility_manifest": results.reproducibility_manifest,
    }
    Path(output_json).write_text(json.dumps(results_dict, indent=2, default=str))
    click.echo(f"\n✅ Results saved to: {output_json}")

    # Export LaTeX if requested
    if output_latex:
        # Prepare results in format expected by export_to_latex
        latex_results = {
            model: {
                "mmlu": results.mmlu_accuracy,
                "mmlu_ci": results.mmlu_ci,
                "truthfulqa": results.truthfulqa_accuracy,
                "truthfulqa_ci": results.truthfulqa_ci,
                "hellaswag": results.hellaswag_accuracy,
                "hellaswag_ci": results.hellaswag_ci,
            }
        }
        latex_content = export_to_latex(latex_results)
        Path(output_latex).write_text(latex_content)
        click.echo(f"📄 LaTeX table saved to: {output_latex}")

    # Export BibTeX if requested
    if output_bibtex:
        eval_metadata = {
            "version": "2.0.0",
            "date": results.timestamp,
            "author": "LLM Evaluation Suite",
            "models_evaluated": [model],
            "n_samples": sample_size,
        }
        bibtex_content = generate_bibtex(eval_metadata)
        Path(output_bibtex).write_text(bibtex_content)
        click.echo(f"📚 BibTeX citations saved to: {output_bibtex}")

    # Show cache stats
    if cache and isinstance(llm_provider, CachedProvider):
        stats = llm_provider.get_cache_stats()
        click.echo(f"\n💾 Cache Stats: {stats['hit_rate_percent']:.1f}% hit rate")


if __name__ == "__main__":
    cli()
