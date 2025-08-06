"""
Gemma Guard - Behavioral Signal Monitoring & AI Insight System

A scientifically designed, privacy-respecting app for emotional and mental health 
reflection using behavioral prompts, Chrono-Signature personality analysis, 
and biometric signal simulations.
"""

__version__ = "1.0.0"
__author__ = "Syira"
__email__ = "syira.datasci@outlook.com"

# Package metadata
__title__ = "Gemma Guard"
__description__ = "Burnout Signal Awareness & AI Insight System"
__url__ = "https://github.com/syira/gemma-guard"
__license__ = "Proprietary"
__copyright__ = "© Syira, 2025"

# Import key components for easy access
try:
    from app.signal_engine import get_current_signal
    from app.pattern_mapper import map_traits_to_behavioral_pattern
    from app.matcher import match_signal_to_profile
    from app.gemma_inference import run_inference
    from app.insight_generator import generate_insight
    
    __all__ = [
        'get_current_signal',
        'map_traits_to_behavioral_pattern', 
        'match_signal_to_profile',
        'run_inference',
        'generate_insight'
    ]
except ImportError:
    # Handle import errors gracefully during development
    __all__ = []
