"""
Inference Engine: Combines behavioral pattern tags and biosignal data to generate burnout-related advisory prompts.
Built for compatibility with Gemma 3n via Ollama. Logging enabled for longitudinal analysis.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the real Ollama integration
import sys
sys.path.append(str(Path(__file__).parent.parent))
from private.llm_inference import generate_narrative, check_ollama_health

# Create necessary directories
Path("data").mkdir(exist_ok=True)
Path("prompts").mkdir(exist_ok=True)


def format_prompt(pattern_tags: List[str], signal_data: Dict[str, Any], template_path: str = "prompts/base_prompt.txt") -> str:
    """
    Formats a structured prompt by embedding behavioral and biosignal tags into the base template.
    Parameters:
        pattern_tags (List[str]): Tags from pattern_mapper.py
        signal_data (Dict[str, Any]): Live or simulated biosignal input
        template_path (str): Path to prompt template
    Returns:
        str: Finalized prompt for LLM
    """
    if not Path(template_path).exists():
        raise FileNotFoundError(f"Prompt template not found: {template_path}")

    with open(template_path, "r") as f:
        base_prompt = f.read()

    prompt = base_prompt.format(
        pattern_tags=", ".join(pattern_tags),
        skin_conductance=signal_data.get("skin_conductance", "N/A"),
        environmental_state=signal_data.get("environmental_state", "neutral")  # Updated from cosmic_state
    )

    return prompt


def run_inference(pattern_tags: List[str], signal_data: Dict[str, Any], save_to: str = "data/inference_log.json") -> Dict[str, Any]:
    """
    Executes prompt construction, sends to Gemma via Ollama, and logs advisory inference.
    Parameters:
        pattern_tags (List[str]): Behavior-linked tags
        signal_data (Dict[str, Any]): Biosignal readings
        save_to (str): Path to JSON log
    Returns:
        Dict[str, Any]: Inference package including prompt and timestamp
    """
    # Check if Ollama integration is enabled
    enable_ollama = os.getenv("ENABLE_OLLAMA_INTEGRATION", "false").lower() == "true"
    model = os.getenv("OLLAMA_MODEL", "gemma2:7b")
    
    prompt = format_prompt(pattern_tags, signal_data)

    if enable_ollama:
        # Use real Gemma via Ollama
        response = generate_narrative(prompt, model)
        llm_model = f"Gemma-3n-{model}"
        
        # Check Ollama health status
        health_status = check_ollama_health()
        if health_status["status"] != "healthy":
            response = f"🔧 Ollama Status: {health_status.get('error', 'Unknown error')}\n\nFallback: {simulate_gemma_response(prompt)}"
            llm_model = "Gemma-Fallback"
    else:
        # Use simulation for development
        response = simulate_gemma_response(prompt)
        llm_model = "Gemma-Simulated"

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pattern_tags": pattern_tags,
        "signal_data": signal_data,
        "prompt_used": prompt,
        "inference": response,
        "llm_model": llm_model
    }

    # Append inference result to log file
    try:
        with open(save_to, "r", encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    history.append(result)

    with open(save_to, "w", encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

    return result


def simulate_gemma_response(prompt: str) -> str:
    """
    Fallback simulator for development and when Ollama is unavailable.
    """
    if "reactive" in prompt and "volatile" in prompt:
        return (
            "🔬 Burnout Risk Insight: Elevated stress markers detected in behavioral patterns.\n"
            "🧘 Regulation Strategy: Prioritize low-stimulation tasks and reflective journaling. "
            "Avoid high-emotion meetings or conflict-heavy spaces today."
        )
    elif "creative" in prompt and ("stimulus-seeking" in prompt or "early-peak" in prompt):
        return (
            "🔬 Burnout Risk Insight: Cognitive expansion phase detected - monitor for overstimulation.\n"
            "🧘 Regulation Strategy: Leverage ideation timeframes for focused creative work. "
            "Set clear boundaries to prevent creative burnout."
        )
    else:
        return (
            "🔬 Burnout Risk Insight: Stable behavioral patterns observed.\n"
            "🧘 Regulation Strategy: Maintain consistency in pacing and reinforce familiar habits. "
            "Focus on controlled inputs and minimal cognitive overload."
        )