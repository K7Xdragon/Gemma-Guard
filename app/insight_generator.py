# 🧠 Gemma Guard — Insight Generator
# Merges signal matching and inference text into a unified summary

def generate_insight(match_result: dict, inference_text: str) -> dict:
    """
    Combines signal-pattern match status with LLM-generated behavioral advisory.

    Parameters:
        match_result (dict): Output from matcher.match_signal_to_profile()
        inference_text (str): Advisory string from gemma_inference.run_inference()

    Returns:
        dict: Final insight package with summary and recommendation
    """
    status = match_result.get("status", "unknown")
    mismatches = match_result.get("mismatches", [])

    if status == "aligned":
        summary = "✅ Your biometric rhythm aligns well with behavioral traits today."
    else:
        summary = (
            f"⚠️ Misalignment Detected:\n"
            f"- Indicators: {', '.join(mismatches)}\n"
            "Consider adjusting mental pacing or stimulus exposure."
        )

    return {
        "summary": summary,
        "recommendation": inference_text
    }