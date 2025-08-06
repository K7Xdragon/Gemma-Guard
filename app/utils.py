"""
Utility functions for Gemma Guard application.
Provides common functionality for data loading, saving, and directory management.
"""

import json
import os
from typing import Any, List, Dict
from pathlib import Path


def load_json(filepath: str, default: Any = None) -> Any:
    """
    Load JSON data from file with optional default value.
    
    Args:
        filepath (str): Path to the JSON file
        default (Any): Default value to return if file doesn't exist or is invalid
        
    Returns:
        Any: Loaded JSON data or default value
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return default if default is not None else {}
    except (json.JSONDecodeError, IOError, UnicodeDecodeError):
        return default if default is not None else {}


def append_json_line(data: Dict[str, Any], filepath: str) -> None:
    """
    Append a new entry to a JSON array file.
    Creates the file if it doesn't exist.
    
    Args:
        data (Dict[str, Any]): Data to append
        filepath (str): Path to the JSON file
    """
    try:
        # Load existing data
        existing_data = load_json(filepath, default=[])
        
        # Ensure it's a list
        if not isinstance(existing_data, list):
            existing_data = []
        
        # Append new data
        existing_data.append(data)
        
        # Save back to file
        ensure_dir(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error appending to JSON file {filepath}: {e}")


def ensure_dir(directory: str) -> None:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory (str): Directory path to create
    """
    if directory:  # Only if directory is not empty
        Path(directory).mkdir(parents=True, exist_ok=True)


def save_json(data: Any, filepath: str) -> None:
    """
    Save data to JSON file.
    
    Args:
        data (Any): Data to save
        filepath (str): Path to the JSON file
    """
    try:
        ensure_dir(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving JSON file {filepath}: {e}")


def read_text_file(filepath: str) -> str:
    """
    Read text content from file.
    
    Args:
        filepath (str): Path to the text file
        
    Returns:
        str: File content or empty string if error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""


def write_text_file(content: str, filepath: str) -> None:
    """
    Write text content to file.
    
    Args:
        content (str): Content to write
        filepath (str): Path to the text file
    """
    try:
        ensure_dir(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing text file {filepath}: {e}")
