#!/usr/bin/env python
"""
Fix and run the AI Hobby Intelligence Platform
"""
import subprocess
import sys
import os

print("=" * 70)
print("AI HOBBY INTELLIGENCE PLATFORM - SETUP & EXECUTION")
print("=" * 70)

# Step 1: Fix requirements.txt
print("\n[STEP 1] Fixing requirements.txt...")
requirements_content = """pandas>=2.0.0
sentence-transformers>=2.2.0
chromadb>=0.4.0
google-generativeai>=0.3.0
rich>=13.0.0
python-dotenv>=1.0.0
"""

with open("requirements.txt", "w") as f:
    f.write(requirements_content)
print("✓ requirements.txt fixed!")

# Step 2: Install dependencies
print("\n[STEP 2] Installing dependencies...")
print("This may take a few minutes on first run...")

packages = [
    "pandas>=2.0.0",
    "sentence-transformers>=2.2.0",
    "chromadb>=0.4.0",
    "google-generativeai>=0.3.0",
    "rich>=13.0.0",
    "python-dotenv>=1.0.0"
]

for package in packages:
    print(f"  Installing {package}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", package],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"  ⚠ Warning: {package} - {result.stderr[:100]}")
    else:
        print(f"  ✓ {package} installed")

print("✓ All dependencies installed!")

# Step 3: Run the application
print("\n[STEP 3] Starting AI Hobby Intelligence Platform...")
print("=" * 70)
print()

# Run the main application
result = subprocess.run([sys.executable, "main.py"])
sys.exit(result.returncode)
