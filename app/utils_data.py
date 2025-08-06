import json
import os
from datetime import datetime, timezone
import uuid

def save_signal_data(signal_packet: dict, filepath: str, include_metadata: bool = True):
    """
    Saves a single signal packet to a JSON file, optionally wrapped with metadata.
    Compatible with output from signal_engine.generate_signal_packet().
    """
    envelope = signal_packet.copy()

    if include_metadata:
        envelope["metadata"] = {
            "record_id": str(uuid.uuid4()),
            "saved_at_utc": datetime.now(timezone.utc).isoformat()
        }

    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(envelope, f, indent=4, ensure_ascii=False)

def append_signal_log(signal_entry: dict, filepath: str):
    """
    Appends signal entry to a historical JSON log file.
    Ensures robustness and traceability over time.
    """
    signal_entry["record_id"] = str(uuid.uuid4())
    signal_entry["logged_at_utc"] = datetime.now(timezone.utc).isoformat()

    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding='utf-8') as f:
                log_data = json.load(f)
        except json.JSONDecodeError:
            log_data = []
    else:
        log_data = []

    log_data.append(signal_entry)
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

def format_for_ollama_prompt(signal_entry: dict) -> str:
    """
    Translates signal packet into an LLM-compatible prompt for behavioral insight.
    Designed for Ollama use with human-like summarization.
    """
    return (
        f"At {signal_entry.get('timestamp_utc', '[unknown]')}, "
        f"electrodermal activity measured {signal_entry.get('skin_conductance', '[N/A]')} µS.\n"
        f"Stimulus classification: '{signal_entry.get('environmental_state', '[undefined]')}'.\n"
        f"Assess probable behavioral traits from this physiological pattern."
    )