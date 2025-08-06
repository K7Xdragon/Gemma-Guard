#!/usr/bin/env python3
"""
Gemma Guard Startup Script
Run this from the project root directory.
"""

import sys
import os
from pathlib import Path

# Ensure we're in the right directory
project_root = Path(__file__).parent
os.chdir(project_root)

# Add project root to Python path
sys.path.insert(0, str(project_root))

# Set environment variables for Streamlit
os.environ['PYTHONPATH'] = str(project_root)

# Import and run the main app
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "app/main.py"]
    sys.exit(stcli.main())
