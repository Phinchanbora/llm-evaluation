"""
Demo vs Real Comparison
=======================
This script demonstrates the CRITICAL difference between demo datasets (3-8 questions)
and real benchmark datasets (14,042+ questions).

Perfect for blog posts and presentations showing why proper evaluation matters.
"""

import sys
from pathlib import Path

# Add src to path for direct execution
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llm_evaluator.benchmarks import BenchmarkRunner, DATASETS_AVAILABLE
from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.providers import GenerationConfig


def print_header(title: str) -> None:
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def compare_demo_vs_sampling(model: str = "llama3.2:1b", sample_size: int = 100) -> None:
    """
    Compare demo mode (3 questions) vs sampling mode (100 questions)
    
    Args:
        model: Ollama model name
        sample_size: Number of questions to sample from real datasets
    """
    print_header(f"📊 DEMO vs REAL: {model}")
    
    print(f"\n🎯 Model: {model}")
    print(f"📦 Sample size: {sample_size} questions")
    print()
    
    # Check if full datasets are available
    if not DATASETS_AVAILABLE:
        print("⚠️  WARNING: 'datasets' library not installed!")
        print("   Install with: pip install datasets")
        print("\n   Showing demo mode only...")
        print()
    
    # Configure provider
    config = GenerationConfig(
        temperature=0.1,  # Low temperature for consistency
        max_tokens=100,
        timeout_seconds=30
    )
    provider = OllamaProvider(model=model, config=config)
    
    # DEMO MODE (3 questions only)
    print("🚀 Running DEMO mode (3 questions)...")
    print("   ⏱️  Expected time: ~15-30 seconds")
    demo_runner = BenchmarkRunner(provider)
    demo_results = demo_runner.run_mmlu_sample()
    
    print(f"\n   ✅ DEMO Results:")
    print(f"      Questions tested: {demo_results['questions_tested']}")
    print(f"      Accuracy: {demo_results['mmlu_accuracy']:.1%}")
    print(f"      Mode: {demo_results['mode']}")
    
    if not DATASETS_AVAILABLE:
        print("\n❌ Cannot compare with real datasets (library not installed)")
        return
    
    # SAMPLING MODE (100 real questions)
    print(f"\n🏭 Running SAMPLING mode ({sample_size} real questions)...")
    print(f"   ⏱️  Expected time: ~2-5 minutes")
    real_runner = BenchmarkRunner(
        provider=provider,
        use_full_datasets=True,
        sample_size=sample_size
    )
    real_results = real_runner.run_mmlu_sample()
    
    print(f"\n   ✅ REAL Results:")
    print(f"      Questions tested: {real_results['questions_tested']}")
    print(f"      Total available: {real_results['total_available']}")
    print(f"      Accuracy: {real_results['mmlu_accuracy']:.1%}")
    print(f"      Mode: {real_results['mode']}")
    
    # COMPARISON
    print_header("📈 COMPARISON: Demo vs Real")
    
    demo_acc = demo_results['mmlu_accuracy']
    real_acc = real_results['mmlu_accuracy']
    difference = abs(demo_acc - real_acc)
    
    print(f"\n   Demo (3 questions):     {demo_acc:>6.1%}")
    print(f"   Real ({sample_size} questions):   {real_acc:>6.1%}")
    print(f"   {'─' * 40}")
    print(f"   Absolute Difference:    {difference:>6.1%}")
    
    if difference > 0.10:
        print(f"\n   ⚠️  HUGE DIFFERENCE! ({difference:.1%})")
        print("   This is why you can't trust demo datasets!")
    elif difference > 0.05:
        print(f"\n   ⚠️  Significant difference ({difference:.1%})")
        print("   Demo results may be misleading")
    else:
        print(f"\n   ✅ Small difference ({difference:.1%})")
        print("   Demo happened to be representative (lucky!)")
    
    # Reliability analysis
    print("\n" + "─" * 80)
    print("📊 Statistical Reliability:")
    print(f"   Demo (n=3):      ❌ NOT statistically significant")
    print(f"   Real (n={sample_size}):   ✅ Statistically reliable")
    print(f"   Full (n=14042):  ✅✅ Publication-ready")


def compare_multiple_benchmarks(model: str = "llama3.2:1b") -> None:
    """Compare demo vs sampling across all benchmarks"""
    print_header(f"🎯 ALL BENCHMARKS: {model}")
    
    if not DATASETS_AVAILABLE:
        print("\n⚠️  Full datasets not available. Install: pip install datasets")
        return
    
    config = GenerationConfig(temperature=0.1, max_tokens=100, timeout_seconds=30)
    provider = OllamaProvider(model=model, config=config)
    
    # Demo mode
    print("\n🚀 Running DEMO mode (8 total questions)...")
    demo_runner = BenchmarkRunner(provider)
    demo_all = demo_runner.run_all_benchmarks()
    
    # Sampling mode
    print("\n🏭 Running SAMPLING mode (300 total questions)...")
    real_runner = BenchmarkRunner(provider, use_full_datasets=True, sample_size=100)
    real_all = real_runner.run_all_benchmarks()
    
    # Display comparison
    print_header("📊 RESULTS COMPARISON")
    
    benchmarks = [
        ("MMLU", "mmlu_accuracy"),
        ("TruthfulQA", "truthfulqa_score"),
        ("HellaSwag", "hellaswag_accuracy")
    ]
    
    print("\n" + "─" * 80)
    print(f"{'Benchmark':<15} {'Demo':<12} {'Real':<12} {'Difference':<12}")
    print("─" * 80)
    
    for name, key in benchmarks:
        demo_score = demo_all.get(key, 0.0)
        real_score = real_all.get(key, 0.0)
        diff = abs(demo_score - real_score)
        
        status = "⚠️" if diff > 0.10 else "✓"
        print(f"{status} {name:<13} {demo_score:>6.1%}      {real_score:>6.1%}      {diff:>6.1%}")
    
    print("─" * 80)
    print(f"\n💡 Key Insight: Average difference is significant!")
    print(f"   Don't trust evaluations with <50 questions per benchmark")


def main():
    """Main execution"""
    print_header("🔬 LLM EVALUATION: Demo vs Real Datasets")
    print("\nThis script demonstrates why proper evaluation matters.")
    print("We'll compare:")
    print("  • Demo mode: 3 questions (30 seconds)")
    print("  • Sampling mode: 100 questions (2-5 minutes)")
    print("\n⚡ Tip: Results may vary between runs due to model non-determinism")
    
    try:
        # Single benchmark comparison (MMLU)
        compare_demo_vs_sampling(model="llama3.2:1b", sample_size=100)
        
        # Optional: All benchmarks (takes longer)
        if DATASETS_AVAILABLE:
            print("\n\n")
            response = input("🤔 Run comparison for ALL benchmarks? (y/n): ")
            if response.lower() == 'y':
                compare_multiple_benchmarks(model="llama3.2:1b")
        
        print_header("✅ COMPARISON COMPLETE")
        print("\n💡 Key Takeaways:")
        print("   1. Demo datasets (3-8 questions) are unreliable")
        print("   2. Minimum 50-100 questions for meaningful results")
        print("   3. Full datasets (14,042+) for publication-quality evaluation")
        print("\n📚 Learn more: docs/FULL_BENCHMARKS.md")
        print("🔗 GitHub: https://github.com/NahuelGiudizi/llm-evaluation")
        
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("   Make sure Ollama is running: ollama serve")
        print("   And the model is available: ollama pull llama3.2:1b")


if __name__ == "__main__":
    main()
