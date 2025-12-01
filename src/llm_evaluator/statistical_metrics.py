"""
Statistical metrics for academic evaluation of LLMs.

Provides rigorous statistical analysis meeting publication standards for
ML conferences (ACL, EMNLP, ICLR, NeurIPS).

References:
    - Wilson (1927): Confidence intervals for binomial proportions
    - McNemar (1947): Test for paired nominal data
    - Efron & Tibshirani (1993): Bootstrap methods
    - Cohen (1988): Statistical power analysis
"""

import math
from typing import Dict, List, Tuple

import numpy as np
from scipy import stats


def calculate_wilson_ci(
    correct: int | float,
    total: int | float,
    confidence: float = 0.95,
) -> Tuple[float, float]:
    """
    Calculate Wilson score confidence interval for accuracy.

    The Wilson score interval is preferred over the normal approximation
    for binomial proportions, especially when p is near 0 or 1, or when
    sample size is small.

    Args:
        correct: Number of correct predictions
        total: Total number of predictions
        confidence: Confidence level (default: 0.95 for 95% CI)

    Returns:
        Tuple of (lower_bound, upper_bound)

    Raises:
        ValueError: If total <= 0 or correct > total or correct < 0

    Example:
        >>> ci = calculate_wilson_ci(850, 1000)
        >>> print(f"Accuracy: 85.0% (95% CI: [{ci[0]:.1%}, {ci[1]:.1%}])")
        Accuracy: 85.0% (95% CI: [82.7%, 87.1%])

    References:
        Wilson, E. B. (1927). "Probable inference, the law of succession,
        and statistical inference". Journal of the American Statistical
        Association, 22(158), 209-212.
    """
    if total <= 0:
        raise ValueError(f"Total must be positive, got {total}")
    if correct < 0:
        raise ValueError(f"Correct must be non-negative, got {correct}")
    if correct > total:
        raise ValueError(f"Correct ({correct}) cannot exceed total ({total})")

    # Handle edge cases
    if total == 0:
        return (0.0, 1.0)

    p = correct / total
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    z2 = z * z

    denominator = 1 + z2 / total
    center = (p + z2 / (2 * total)) / denominator
    margin = (z / denominator) * math.sqrt(p * (1 - p) / total + z2 / (4 * total * total))

    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)

    return (lower, upper)


def calculate_standard_error(correct: int | float, total: int | float) -> float:
    """
    Calculate standard error of a proportion.

    Args:
        correct: Number of correct predictions
        total: Total number of predictions

    Returns:
        Standard error as float

    Raises:
        ValueError: If total <= 0

    Example:
        >>> se = calculate_standard_error(850, 1000)
        >>> print(f"SE: {se:.4f}")
        SE: 0.0113
    """
    if total <= 0:
        raise ValueError(f"Total must be positive, got {total}")

    p = correct / total
    return math.sqrt(p * (1 - p) / total)


def bootstrap_confidence_interval(
    predictions: List[bool],
    n_bootstrap: int = 10000,
    confidence: float = 0.95,
    random_seed: int = 42,
) -> Tuple[float, float]:
    """
    Bootstrap confidence interval for non-parametric accuracy estimation.

    Preferred for small samples or when distribution assumptions are uncertain.

    Args:
        predictions: List of boolean predictions (True=correct, False=incorrect)
        n_bootstrap: Number of bootstrap samples (default: 10000)
        confidence: Confidence level (default: 0.95)
        random_seed: Random seed for reproducibility

    Returns:
        Tuple of (lower_bound, upper_bound)

    Raises:
        ValueError: If predictions is empty

    Example:
        >>> preds = [True] * 85 + [False] * 15
        >>> ci = bootstrap_confidence_interval(preds)
        >>> print(f"95% CI: [{ci[0]:.1%}, {ci[1]:.1%}]")

    References:
        Efron, B., & Tibshirani, R. J. (1993). "An introduction to the
        bootstrap". Chapman & Hall.
    """
    if len(predictions) == 0:
        raise ValueError("Predictions list cannot be empty")

    rng = np.random.default_rng(random_seed)
    predictions_array = np.array(predictions, dtype=float)
    n = len(predictions_array)

    bootstrap_accuracies = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        sample_indices = rng.integers(0, n, size=n)
        bootstrap_accuracies[i] = predictions_array[sample_indices].mean()

    alpha = 1 - confidence
    ci_lower = float(np.percentile(bootstrap_accuracies, alpha / 2 * 100))
    ci_upper = float(np.percentile(bootstrap_accuracies, (1 - alpha / 2) * 100))

    return (ci_lower, ci_upper)


def mcnemar_test(
    model_a_predictions: List[bool],
    model_b_predictions: List[bool],
    ground_truth: List[bool],
) -> Dict[str, object]:
    """
    McNemar's test for comparing two models on the same dataset.

    Tests whether two models have significantly different error rates.
    Null hypothesis: Both models have the same error rate.

    Args:
        model_a_predictions: List of booleans (True=correct for ground truth)
        model_b_predictions: List of booleans (True=correct for ground truth)
        ground_truth: List of booleans representing ground truth

    Returns:
        Dictionary with:
            - 'statistic': Chi-squared statistic
            - 'p_value': Two-tailed p-value
            - 'significant': Boolean (p < 0.05)
            - 'conclusion': Human-readable conclusion
            - 'contingency_table': Dict with a, b, c, d counts

    Raises:
        ValueError: If lists have different lengths

    Example:
        >>> model_a = [True] * 90 + [False] * 10
        >>> model_b = [True] * 70 + [False] * 30
        >>> truth = [True] * 100
        >>> result = mcnemar_test(model_a, model_b, truth)
        >>> print(f"p-value: {result['p_value']:.4f}")

    References:
        McNemar, Q. (1947). "Note on the sampling error of the difference
        between correlated proportions or percentages". Psychometrika,
        12(2), 153-157.
    """
    if len(model_a_predictions) != len(model_b_predictions):
        raise ValueError("Model predictions must have same length")
    if len(model_a_predictions) != len(ground_truth):
        raise ValueError("Predictions and ground truth must have same length")

    a_pred = np.array(model_a_predictions)
    b_pred = np.array(model_b_predictions)
    truth = np.array(ground_truth)

    # Determine correctness
    a_correct = a_pred == truth
    b_correct = b_pred == truth

    # Build contingency table
    # a: both correct
    # b: A correct, B wrong
    # c: A wrong, B correct
    # d: both wrong
    a_count = int(np.sum(a_correct & b_correct))
    b_count = int(np.sum(a_correct & ~b_correct))
    c_count = int(np.sum(~a_correct & b_correct))
    d_count = int(np.sum(~a_correct & ~b_correct))

    # McNemar statistic with continuity correction
    if b_count + c_count == 0:
        statistic = 0.0
        p_value = 1.0
    else:
        statistic = (abs(b_count - c_count) - 1) ** 2 / (b_count + c_count)
        p_value = 1 - stats.chi2.cdf(statistic, df=1)

    significant = p_value < 0.05

    if significant:
        if b_count > c_count:
            conclusion = "Model A significantly better than Model B"
        else:
            conclusion = "Model B significantly better than Model A"
    else:
        conclusion = "No significant difference between models"

    return {
        "statistic": statistic,
        "p_value": p_value,
        "significant": significant,
        "conclusion": conclusion,
        "contingency_table": {
            "both_correct": a_count,
            "a_correct_b_wrong": b_count,
            "a_wrong_b_correct": c_count,
            "both_wrong": d_count,
        },
    }


def cohens_h(p1: float, p2: float) -> Dict[str, object]:
    """
    Calculate Cohen's h effect size for difference between two proportions.

    Cohen's h is used to measure the difference between two proportions
    and is independent of sample size.

    Args:
        p1: First proportion (0 to 1)
        p2: Second proportion (0 to 1)

    Returns:
        Dictionary with:
            - 'h': Cohen's h value
            - 'magnitude': 'negligible', 'small', 'medium', or 'large'
            - 'interpretation': Human-readable interpretation

    Raises:
        ValueError: If proportions not in [0, 1]

    Example:
        >>> result = cohens_h(0.85, 0.70)
        >>> print(f"Effect size: {result['h']:.3f} ({result['magnitude']})")
        Effect size: 0.364 (small)

    References:
        Cohen, J. (1988). "Statistical power analysis for the behavioral
        sciences" (2nd ed.). Lawrence Erlbaum Associates.

    Thresholds (Cohen, 1988):
        - Small: |h| >= 0.2
        - Medium: |h| >= 0.5
        - Large: |h| >= 0.8
    """
    if not 0 <= p1 <= 1:
        raise ValueError(f"p1 must be between 0 and 1, got {p1}")
    if not 0 <= p2 <= 1:
        raise ValueError(f"p2 must be between 0 and 1, got {p2}")

    # Cohen's h formula: 2 * (arcsin(sqrt(p1)) - arcsin(sqrt(p2)))
    phi1 = 2 * math.asin(math.sqrt(p1))
    phi2 = 2 * math.asin(math.sqrt(p2))
    h = phi1 - phi2

    abs_h = abs(h)

    if abs_h >= 0.8:
        magnitude = "large"
    elif abs_h >= 0.5:
        magnitude = "medium"
    elif abs_h >= 0.2:
        magnitude = "small"
    else:
        magnitude = "negligible"

    if h > 0:
        direction = "higher"
    elif h < 0:
        direction = "lower"
    else:
        direction = "equal"

    interpretation = (
        f"The difference is {magnitude} (h={h:.3f}). "
        f"First proportion is {direction} than second."
    )

    return {
        "h": h,
        "magnitude": magnitude,
        "interpretation": interpretation,
    }


def paired_proportion_test(
    successes_a: int,
    successes_b: int,
    total: int,
    method: str = "exact",
) -> Dict[str, object]:
    """
    Test for significant difference between two proportions from same sample.

    Args:
        successes_a: Number of successes for model A
        successes_b: Number of successes for model B
        total: Total number of samples
        method: 'exact' (binomial) or 'normal' (z-test approximation)

    Returns:
        Dictionary with test results

    Example:
        >>> result = paired_proportion_test(850, 780, 1000)
        >>> print(f"Significant: {result['significant']} (p={result['p_value']:.4f})")
    """
    p_a = successes_a / total
    p_b = successes_b / total
    diff = p_a - p_b

    if method == "exact":
        # Use exact binomial test for difference
        # Under H0: both have same success rate
        pooled_p = (successes_a + successes_b) / (2 * total)
        pooled_se = math.sqrt(2 * pooled_p * (1 - pooled_p) / total)

        if pooled_se > 0:
            z_stat = diff / pooled_se
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        else:
            z_stat = 0.0
            p_value = 1.0
    else:
        # Normal approximation
        se_diff = math.sqrt((p_a * (1 - p_a) + p_b * (1 - p_b)) / total)
        if se_diff > 0:
            z_stat = diff / se_diff
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        else:
            z_stat = 0.0
            p_value = 1.0

    return {
        "difference": diff,
        "z_statistic": z_stat,
        "p_value": p_value,
        "significant": p_value < 0.05,
        "model_a_accuracy": p_a,
        "model_b_accuracy": p_b,
    }


def calculate_all_statistics(
    correct: int,
    total: int,
    predictions: List[bool] | None = None,
    confidence: float = 0.95,
) -> Dict[str, object]:
    """
    Calculate comprehensive statistics for a single evaluation.

    Convenience function that computes all relevant statistics at once.

    Args:
        correct: Number of correct predictions
        total: Total number of predictions
        predictions: Optional list of individual predictions for bootstrap
        confidence: Confidence level (default: 0.95)

    Returns:
        Dictionary with all computed statistics

    Example:
        >>> stats = calculate_all_statistics(850, 1000)
        >>> print(f"Accuracy: {stats['accuracy']:.1%}")
        >>> print(f"95% CI: [{stats['wilson_ci'][0]:.1%}, {stats['wilson_ci'][1]:.1%}]")
    """
    accuracy = correct / total if total > 0 else 0.0
    wilson_ci = calculate_wilson_ci(correct, total, confidence)
    se = calculate_standard_error(correct, total)

    result: Dict[str, object] = {
        "accuracy": accuracy,
        "correct": correct,
        "total": total,
        "wilson_ci": wilson_ci,
        "ci_lower": wilson_ci[0],
        "ci_upper": wilson_ci[1],
        "ci_width": wilson_ci[1] - wilson_ci[0],
        "standard_error": se,
        "confidence_level": confidence,
        "method": "wilson",
    }

    if predictions is not None and len(predictions) > 0:
        bootstrap_ci = bootstrap_confidence_interval(predictions, confidence=confidence)
        result["bootstrap_ci"] = bootstrap_ci
        result["bootstrap_ci_lower"] = bootstrap_ci[0]
        result["bootstrap_ci_upper"] = bootstrap_ci[1]

    return result
