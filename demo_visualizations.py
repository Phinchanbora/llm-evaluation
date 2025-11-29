"""Demo script showing visualization capabilities"""

from llm_evaluator import ModelEvaluator, EvaluationVisualizer, quick_comparison
from pathlib import Path

def main():
    print("=" * 80)
    print("LLM EVALUATION - VISUALIZATION DEMO")
    print("=" * 80)
    print()

    # Simulate evaluation results for multiple models
    print("📊 Simulating evaluation results for 3 models...\n")
    
    results = {
        "llama3.2:1b": {
            "mmlu": 0.65,
            "truthful_qa": 0.58,
            "hellaswag": 0.72,
            "accuracy": 0.75,
            "coherence": 0.68,
            "consistency": 0.82,
            "avg_response_time": 0.45,
            "tokens_per_second": 85.3
        },
        "mistral:7b": {
            "mmlu": 0.78,
            "truthful_qa": 0.71,
            "hellaswag": 0.83,
            "accuracy": 0.82,
            "coherence": 0.79,
            "consistency": 0.88,
            "avg_response_time": 0.92,
            "tokens_per_second": 42.1
        },
        "phi3:3.8b": {
            "mmlu": 0.71,
            "truthful_qa": 0.65,
            "hellaswag": 0.77,
            "accuracy": 0.78,
            "coherence": 0.73,
            "consistency": 0.85,
            "avg_response_time": 0.68,
            "tokens_per_second": 58.7
        }
    }

    # Create output directory
    output_dir = Path("outputs/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("✅ Generating visualizations...\n")

    # Initialize visualizer
    viz = EvaluationVisualizer()

    # 1. Benchmark comparison
    print("📊 Creating benchmark comparison chart...")
    benchmark_scores = {
        model: {k: v for k, v in metrics.items() 
                if k in ["mmlu", "truthful_qa", "hellaswag"]}
        for model, metrics in results.items()
    }
    viz.plot_benchmark_comparison(
        benchmark_scores,
        output_path=output_dir / "benchmark_comparison.png"
    )
    print(f"   Saved: {output_dir / 'benchmark_comparison.png'}\n")

    # 2. Interactive benchmark comparison
    print("📊 Creating interactive benchmark chart...")
    fig = viz.plot_benchmark_comparison(
        benchmark_scores,
        output_path=output_dir / "benchmark_interactive.html",
        interactive=True
    )
    print(f"   Saved: {output_dir / 'benchmark_interactive.html'}\n")

    # 3. Radar chart for quality metrics
    print("🎯 Creating radar chart...")
    quality_metrics = {
        model: {k: v for k, v in metrics.items() 
                if k in ["accuracy", "coherence", "consistency"]}
        for model, metrics in results.items()
    }
    viz.plot_radar_chart(
        quality_metrics,
        output_path=output_dir / "quality_radar.html"
    )
    print(f"   Saved: {output_dir / 'quality_radar.html'}\n")

    # 4. Performance heatmap
    print("🔥 Creating performance heatmap...")
    viz.plot_model_heatmap(
        results,
        output_path=output_dir / "performance_heatmap.png"
    )
    print(f"   Saved: {output_dir / 'performance_heatmap.png'}\n")

    # 5. Score distribution
    print("📦 Creating score distribution...")
    score_distributions = {
        "llama3.2:1b": [0.65, 0.58, 0.72, 0.75, 0.68, 0.82],
        "mistral:7b": [0.78, 0.71, 0.83, 0.82, 0.79, 0.88],
        "phi3:3.8b": [0.71, 0.65, 0.77, 0.78, 0.73, 0.85]
    }
    viz.plot_score_distribution(
        score_distributions,
        output_path=output_dir / "score_distribution.png"
    )
    print(f"   Saved: {output_dir / 'score_distribution.png'}\n")

    # 6. Performance trends
    print("📈 Creating performance trends...")
    time_series = {
        "llama3.2:1b": [(i, 0.45 + (i * 0.02)) for i in range(10)],
        "mistral:7b": [(i, 0.92 + (i * 0.01)) for i in range(10)],
        "phi3:3.8b": [(i, 0.68 + (i * 0.015)) for i in range(10)]
    }
    viz.plot_performance_trends(
        time_series,
        metric_name="Response Time (seconds)",
        output_path=output_dir / "response_time_trends.png"
    )
    print(f"   Saved: {output_dir / 'response_time_trends.png'}\n")

    # 7. Comprehensive dashboard
    print("🎨 Creating comprehensive dashboard...")
    viz.create_dashboard(
        results,
        output_path=output_dir / "evaluation_dashboard.html"
    )
    print(f"   Saved: {output_dir / 'evaluation_dashboard.html'}\n")

    # Summary
    print("=" * 80)
    print("✅ VISUALIZATION DEMO COMPLETE")
    print("=" * 80)
    print(f"\n📁 All visualizations saved to: {output_dir.absolute()}")
    print("\n📊 Generated charts:")
    print("   1. benchmark_comparison.png - Static bar chart")
    print("   2. benchmark_interactive.html - Interactive bar chart")
    print("   3. quality_radar.html - Multi-metric radar chart")
    print("   4. performance_heatmap.png - All metrics heatmap")
    print("   5. score_distribution.png - Box plot distribution")
    print("   6. response_time_trends.png - Performance over time")
    print("   7. evaluation_dashboard.html - Comprehensive dashboard")
    print("\n💡 Open the HTML files in your browser for interactive charts!")
    print()

    # Print comparison summary
    print("=" * 80)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 80)
    
    for model, metrics in results.items():
        avg_benchmark = sum([metrics["mmlu"], metrics["truthful_qa"], metrics["hellaswag"]]) / 3
        avg_quality = sum([metrics["accuracy"], metrics["coherence"], metrics["consistency"]]) / 3
        
        print(f"\n{model}:")
        print(f"  Avg Benchmark Score: {avg_benchmark:.2f}")
        print(f"  Avg Quality Score:   {avg_quality:.2f}")
        print(f"  Response Time:       {metrics['avg_response_time']:.2f}s")
        print(f"  Tokens/Second:       {metrics['tokens_per_second']:.1f}")

    print()


if __name__ == "__main__":
    main()
