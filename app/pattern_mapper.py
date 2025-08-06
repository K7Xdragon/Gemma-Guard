"""
Trait Mapping Module — Translates user trait inputs into behavioral tags and rationale for pattern analytics.
Supports both signal matching and AI feedback interfaces.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from private.core_logic_real import get_chrono_signature_profile


def map_traits_to_behavioral_pattern(dob: str) -> dict:
    """
    Maps user's date of birth to a Chrono-Signature profile.
    Parameters:
        dob (str): User's date of birth in "YYYY-MM-DD" format.
    Returns:
        dict: Chrono-Signature profile including tags and rationale.
    """
    return get_chrono_signature_profile(dob)


def display_pattern_profile(profile_data: dict) -> str:
    """
    Generates a human-readable summary of the user's behavioral profile.
    Parameters:
        profile_data (dict): Output from get_chrono_signature_profile()
    Returns:
        str: Formatted overview string
    """
    tags = profile_data.get("pattern_tags", [])
    rationale_lines = profile_data.get("rationale", [])

    summary = "📊 Chrono-Signature Profile\n"
    summary += "Tags: " + ", ".join(tags) + "\n\n"
    summary += "Rationale:\n"
    summary += "\n".join(f"- {line}" for line in rationale_lines)

    return summary