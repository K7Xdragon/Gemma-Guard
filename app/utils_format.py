from datetime import datetime

def format_eda_value(eda):
    """
    Formats electrodermal activity for scientific display.
    Adds unit and precision standardization.
    """
    try:
        return f"{float(eda):.2f} µS"
    except (ValueError, TypeError):
        return "[invalid EDA]"

def format_timestamp(ts):
    """
    Converts ISO timestamp to human-readable format.
    """
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return "[invalid timestamp]"

def summarize_signal_packet(signal_packet):
    """
    Produces a summary string of the signal packet for UI or logs.
    """
    readable_ts = format_timestamp(signal_packet.get("timestamp_utc"))
    eda_formatted = format_eda_value(signal_packet.get("skin_conductance"))
    stimulus = signal_packet.get("environmental_state", "[undefined]")

    return (
        f"📡 Signal Summary:\n"
        f"- Time: {readable_ts}\n"
        f"- EDA Level: {eda_formatted}\n"
        f"- Stimulus Classification: {stimulus}"
    )

def highlight_behavioral_trait(trait_str):
    """
    Prepares a behavioral trait descriptor with emphasis for dashboard view or LLM output.
    """
    return f"🧠 Behavioral Insight: {trait_str.capitalize()}"

def clean_identifier(record_id):
    """
    Truncates and prettifies UUID for display.
    """
    if not isinstance(record_id, str):
        return "[invalid ID]"
    return f"ID#{record_id[:8]}"