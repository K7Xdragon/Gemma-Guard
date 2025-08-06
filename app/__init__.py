"""
App package - Core application modules for Gemma Guard.

Contains the main Streamlit interface, signal processing, pattern mapping,
matching logic, AI inference, and insight generation components.
"""

# Core app components
from .signal_engine import get_current_signal, simulate_skin_conductance
from .pattern_mapper import map_traits_to_behavioral_pattern, display_pattern_profile
from .matcher import match_signal_to_profile
from .gemma_inference import run_inference, format_prompt
from .insight_generator import generate_insight
from .utils import load_json, append_json_line, ensure_dir
from .utils_data import save_signal_data, append_signal_log
from .utils_format import format_eda_value, format_timestamp

__all__ = [
    # Signal processing
    'get_current_signal',
    'simulate_skin_conductance',
    
    # Pattern analysis
    'map_traits_to_behavioral_pattern',
    'display_pattern_profile',
    
    # Matching and inference
    'match_signal_to_profile',
    'run_inference',
    'format_prompt',
    'generate_insight',
    
    # Utilities
    'load_json',
    'append_json_line',
    'ensure_dir',
    'save_signal_data',
    'append_signal_log',
    'format_eda_value',
    'format_timestamp'
]
