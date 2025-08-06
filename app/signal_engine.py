# 📡 Gemma Guard — Signal Engine
# Simulates scientific biometrics and behavioral stimulus context for inference modeling

import random
from datetime import datetime, timezone
import uuid

def simulate_skin_conductance():
    """
    Simulates electrodermal activity (EDA) in microsiemens (µS).
    Range derived from psychophysiological baseline: 0.5 – 6.0 µS.
    """
    return round(random.uniform(0.5, 6.0), 2)

def simulate_environmental_state():
    """
    Simulates environmental rhythm index based on abstract stimulus exposure.
    Designed to reflect behavioral load in scientific language.
    """
    return random.choice(["expansive", "restrictive", "neutral", "charged"])

def get_current_signal():
    """
    Generates a unified signal snapshot for inference and logging.
    Output is formatted for Gemma inference and Ollama prompt wrapping.
    """
    return {
        "signal_id": str(uuid.uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "skin_conductance": simulate_skin_conductance(),
        "environmental_state": simulate_environmental_state()
    }

def format_for_ollama_prompt(signal_data: dict) -> str:
    """
    Builds a structured prompt for Ollama LLM based on signal metrics.
    Used for behavioral trait inference and response generation.
    """
    return (
        f"At {signal_data.get('timestamp_utc')}, "
        f"electrodermal activity was recorded at {signal_data.get('skin_conductance')} µS.\n"
        f"Environmental stimulus context classified as '{signal_data.get('environmental_state')}'.\n"
        f"Please assess likely behavioral traits arising from this pattern."
    )