# 🎯 Gemma Guard — Trait Matcher Module
# Analyzes biometric signal alignment against behavioral trait patterns

def match_signal_to_profile(signal: dict, pattern_tags: list) -> dict:
    """
    Evaluates alignment between signal input and mapped behavioral traits.
    Identifies mismatch markers and returns status classification.

    Parameters:
        signal (dict): Signal packet from signal_engine.get_current_signal()
        pattern_tags (list): Trait-based pattern tags from pattern_mapper.py

    Returns:
        dict: Match evaluation including status and mismatch descriptors
    """
    mismatches = []

    # Introvert-aligned users may show overstimulation if EDA is too high
    if "introvert-aligned" in pattern_tags and signal.get("skin_conductance", 0) > 4.5:
        mismatches.append("overstimulated_response")

    # Morning-energy profiles underperform with low EDA early in the day
    if "early-peak" in pattern_tags and signal.get("skin_conductance", 0) < 1.5:
        mismatches.append("underactive_morning")

    # Restrictive environmental states + reactive traits may signal burnout pressure
    if "reactive" in pattern_tags and signal.get("environmental_state") == "restrictive":
        mismatches.append("emotional_constraint")

    status = "aligned" if not mismatches else "misaligned"

    return {
        "status": status,
        "mismatches": mismatches
    }