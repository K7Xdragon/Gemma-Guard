#!/usr/bin/env python3
"""
Quick Ollama integration status check.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the path
sys.path.append(str(Path(__file__).parent))

def check_ollama_integration_status():
    """Check why Ollama integration might be disabled."""
    
    print("🔍 Ollama Integration Status Check")
    print("=" * 40)
    
    # Check 1: Environment variable
    ollama_enabled = os.getenv("ENABLE_OLLAMA_INTEGRATION", "false")
    print(f"📋 Environment Variable: ENABLE_OLLAMA_INTEGRATION = {ollama_enabled}")
    
    # Check 2: Ollama service health
    try:
        from private.llm_inference import check_ollama_health
        health_status = check_ollama_health()
        print(f"🏥 Ollama Health Status: {health_status}")
        
        if health_status["status"] == "healthy":
            print("✅ Ollama service is running")
            if health_status["gemma_available"]:
                print("✅ Gemma model is available")
                print(f"📦 Available models: {', '.join(health_status['available_models'])}")
            else:
                print("⚠️ Gemma model not found")
                print(f"📦 Available models: {', '.join(health_status['available_models'])}")
        else:
            print(f"❌ Ollama service issue: {health_status.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error checking Ollama health: {e}")
    
    # Check 3: .env file loading
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env file loading capability available")
    except ImportError:
        print("⚠️ python-dotenv not installed - .env file may not be loaded automatically")
    
    # Check 4: Recommend solutions
    print("\n🔧 Troubleshooting Recommendations:")
    
    if ollama_enabled.lower() != "true":
        print("1. Set ENABLE_OLLAMA_INTEGRATION=true in .env file")
    
    print("2. Install and start Ollama:")
    print("   - Download from https://ollama.ai")
    print("   - Run: ollama serve")
    
    print("3. Install Gemma model:")
    print("   - Run: ollama pull gemma:latest")
    
    print("4. Verify Ollama is running:")
    print("   - Check: http://localhost:11434")
    
    print("5. Install python-dotenv for .env loading:")
    print("   - Run: pip install python-dotenv")

if __name__ == "__main__":
    check_ollama_integration_status()
