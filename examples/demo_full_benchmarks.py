"""
Demo: Full Benchmark Datasets (Production-Ready)

This demonstrates the use of real, complete datasets:
- MMLU: 14,042 questions (vs 3 demo questions)
- TruthfulQA: 817 questions (vs 3 demo questions)  
- HellaSwag: 10,042 scenarios (vs 2 demo scenarios)

⚠️ WARNING: Running full datasets can take HOURS depending on your model and hardware.
Use sample_size parameter for faster testing with real data.
"""

from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.providers import GenerationConfig
from llm_evaluator.benchmarks import BenchmarkRunner


def demo_with_sampling():
    """Recommended: Use real datasets with sampling for reasonable runtime"""
    print("="*60)
    print("FULL BENCHMARKS DEMO - SAMPLING MODE (Recommended)")
    print("="*60)
    print("\n📊 Using real datasets with 100-question samples")
    print("⏱️  Estimated time: 5-10 minutes\n")
    
    # Configure
    config = GenerationConfig(
        temperature=0.7,
        max_tokens=500,
        timeout_seconds=30,
        retry_attempts=3
    )
    
    model = "llama3.2:1b"
    provider = OllamaProvider(model=model, config=config)
    
    # Check availability
    if not provider.is_available():
        print(f"❌ {model} not available. Make sure Ollama is running.")
        print(f"   Run: ollama pull {model}")
        return
    
    print(f"✅ {model} is ready!\n")
    
    # Initialize with sampling (100 questions per benchmark)
    runner = BenchmarkRunner(
        provider=provider,
        use_full_datasets=True,  # Use real datasets
        sample_size=100          # But sample only 100 questions
    )
    
    # Run benchmarks
    print("🚀 Running benchmarks with real data (sampled)...\n")
    
    try:
        results = runner.run_all_benchmarks()
        
        print("\n" + "="*60)
        print("📊 RESULTS (Real Data, 100-question samples)")
        print("="*60)
        print(f"\nMMLU Accuracy:        {results['mmlu']['mmlu_accuracy']:.1%}")
        print(f"TruthfulQA Score:     {results['truthfulqa']['truthfulness_score']:.1%}")
        print(f"HellaSwag Accuracy:   {results['hellaswag']['hellaswag_accuracy']:.1%}")
        print(f"\n🎯 Aggregate Score:   {results['aggregate_benchmark_score']:.1%}")
        print("\n✅ These results use REAL benchmark data and are more reliable!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_full_datasets():
    """⚠️ Advanced: Run COMPLETE datasets (takes hours)"""
    print("="*60)
    print("FULL BENCHMARKS DEMO - COMPLETE DATASETS")
    print("="*60)
    print("\n⚠️  WARNING: This will run ALL questions:")
    print("   - MMLU: 14,042 questions")
    print("   - TruthfulQA: 817 questions")
    print("   - HellaSwag: 10,042 scenarios")
    print("\n⏱️  Estimated time: 2-8 HOURS (depending on model)")
    print()
    
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    # Configure
    config = GenerationConfig(
        temperature=0.7,
        max_tokens=500,
        timeout_seconds=30,
        retry_attempts=3
    )
    
    model = "llama3.2:1b"
    provider = OllamaProvider(model=model, config=config)
    
    if not provider.is_available():
        print(f"❌ {model} not available.")
        return
    
    # Initialize with full datasets (no sampling)
    runner = BenchmarkRunner(
        provider=provider,
        use_full_datasets=True,  # Use real datasets
        sample_size=None         # No sampling = ALL questions
    )
    
    print(f"\n🚀 Running COMPLETE benchmarks on {model}...")
    print("This will take several hours...\n")
    
    try:
        results = runner.run_all_benchmarks()
        
        print("\n" + "="*60)
        print("📊 COMPLETE BENCHMARK RESULTS")
        print("="*60)
        print(f"\nMMLU:       {results['mmlu']['mmlu_accuracy']:.1%} ({results['mmlu']['questions_tested']} questions)")
        print(f"TruthfulQA: {results['truthfulqa']['truthfulness_score']:.1%} ({results['truthfulqa']['questions_tested']} questions)")
        print(f"HellaSwag:  {results['hellaswag']['hellaswag_accuracy']:.1%} ({results['hellaswag']['questions_tested']} scenarios)")
        print(f"\n🎯 Aggregate: {results['aggregate_benchmark_score']:.1%}")
        print("\n✅ PRODUCTION-READY RESULTS - Valid for research and publication!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_comparison():
    """Compare demo vs sampled real data"""
    print("="*60)
    print("COMPARISON: Demo Mode vs Real Data")
    print("="*60)
    
    config = GenerationConfig(temperature=0.7, max_tokens=500, timeout_seconds=30)
    model = "llama3.2:1b"
    provider = OllamaProvider(model=model, config=config)
    
    if not provider.is_available():
        print(f"❌ {model} not available.")
        return
    
    print(f"\n📊 Testing {model} in both modes...\n")
    
    # Demo mode
    print("1️⃣  Running DEMO mode (3 questions)...")
    runner_demo = BenchmarkRunner(provider=provider, use_full_datasets=False)
    demo_results = runner_demo.run_all_benchmarks()
    
    print("\n2️⃣  Running SAMPLED mode (50 real questions)...")
    runner_real = BenchmarkRunner(provider=provider, use_full_datasets=True, sample_size=50)
    real_results = runner_real.run_all_benchmarks()
    
    # Compare
    print("\n" + "="*60)
    print("📊 COMPARISON")
    print("="*60)
    print("\n{:<20} {:<15} {:<15}".format("Benchmark", "Demo (3q)", "Real (50q)"))
    print("-" * 50)
    print("{:<20} {:<15.1%} {:<15.1%}".format(
        "MMLU", 
        demo_results['mmlu']['mmlu_accuracy'],
        real_results['mmlu']['mmlu_accuracy']
    ))
    print("{:<20} {:<15.1%} {:<15.1%}".format(
        "TruthfulQA",
        demo_results['truthfulqa']['truthfulness_score'],
        real_results['truthfulqa']['truthfulness_score']
    ))
    print("{:<20} {:<15.1%} {:<15.1%}".format(
        "HellaSwag",
        demo_results['hellaswag']['hellaswag_accuracy'],
        real_results['hellaswag']['hellaswag_accuracy']
    ))
    print("-" * 50)
    print("{:<20} {:<15.1%} {:<15.1%}".format(
        "AGGREGATE",
        demo_results['aggregate_benchmark_score'],
        real_results['aggregate_benchmark_score']
    ))
    print("\n💡 Notice the difference? Real data provides more accurate assessment!")


if __name__ == "__main__":
    print("\n🎯 Full Benchmark Datasets Demo\n")
    print("Choose mode:")
    print("1. Sampling mode (100 questions, ~5-10 min) [RECOMMENDED]")
    print("2. Complete datasets (ALL questions, ~2-8 hours)")
    print("3. Compare demo vs real data")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        demo_with_sampling()
    elif choice == "2":
        demo_full_datasets()
    elif choice == "3":
        demo_comparison()
    else:
        print("Exiting...")
