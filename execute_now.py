#!/usr/bin/env python
"""
Quick runner - Install and test the platform
"""
import subprocess
import sys
import os

# Change to project directory
os.chdir("c:\\Users\\Lakshitha SM\\Desktop\\AI Hobby Intelligence Platform")

print("=" * 70)
print("RUNNING AI HOBBY INTELLIGENCE PLATFORM")
print("=" * 70)

# Quick dependency check
print("\n[STEP 1] Checking/Installing dependencies...")
packages = ["pandas", "sentence-transformers", "chromadb", "google-generativeai", "rich", "python-dotenv"]

for pkg in packages:
    print(f"  Installing {pkg}...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], capture_output=True)

print("✓ Dependencies ready!\n")

# Run test diagnostics
print("[STEP 2] Running diagnostics...")
result = subprocess.run([sys.executable, "test_all.py"])

if result.returncode == 0:
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED - LAUNCHING PLATFORM")
    print("=" * 70 + "\n")
    # Run the main platform
    subprocess.run([sys.executable, "main.py"])
else:
    print("\n✗ Some tests failed")
    sys.exit(1)
