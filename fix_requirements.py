#!/usr/bin/env python
"""Fix the requirements.txt file"""
import os

# The correct requirements content
correct_requirements = """pandas>=2.0.0
sentence-transformers>=2.2.0
chromadb>=0.4.0
google-generativeai>=0.3.0
rich>=13.0.0
python-dotenv>=1.0.0"""

# Write the fixed file
try:
    with open("requirements.txt", "w", encoding='utf-8') as f:
        f.write(correct_requirements)
    print("✓ requirements.txt has been fixed!")
    
    # Verify
    with open("requirements.txt", "r", encoding='utf-8') as f:
        content = f.read()
        lines = content.strip().split('\n')
        print(f"✓ File now contains {len(lines)} packages:")
        for i, line in enumerate(lines, 1):
            print(f"  {i}. {line}")
except Exception as e:
    print(f"✗ Error fixing requirements.txt: {e}")
    exit(1)
