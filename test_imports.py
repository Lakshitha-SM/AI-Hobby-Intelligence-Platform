#!/usr/bin/env python
"""
Quick test to verify all imports and basic functionality
"""
import sys
import os

print("[TEST] Starting import diagnostics...")

try:
    print("[TEST] Importing dataset.loader...")
    from dataset.loader import load_dataset, create_documents, add_custom_entry
    print("[✓] dataset.loader imported successfully")
except Exception as e:
    print(f"[✗] Failed to import dataset.loader: {e}")
    sys.exit(1)

try:
    print("[TEST] Importing embeddings.generator...")
    from embeddings.generator import EmbeddingGenerator
    print("[✓] embeddings.generator imported successfully")
except Exception as e:
    print(f"[✗] Failed to import embeddings.generator: {e}")
    sys.exit(1)

try:
    print("[TEST] Importing vector_db...")
    from vector_db import HobbyVectorDB
    print("[✓] vector_db imported successfully")
except Exception as e:
    print(f"[✗] Failed to import vector_db: {e}")
    sys.exit(1)

try:
    print("[TEST] Importing llm_manager...")
    from llm_manager import GeminiLLMManager
    print("[✓] llm_manager imported successfully")
except Exception as e:
    print(f"[✗] Failed to import llm_manager: {e}")
    sys.exit(1)

try:
    print("[TEST] Checking Rich library...")
    from rich.console import Console
    from rich.panel import Panel
    print("[✓] Rich library imported successfully")
except Exception as e:
    print(f"[✗] Failed to import Rich: {e}")
    sys.exit(1)

try:
    print("[TEST] Loading dataset...")
    df = load_dataset()
    print(f"[✓] Dataset loaded successfully: {len(df)} records")
except Exception as e:
    print(f"[✗] Failed to load dataset: {e}")
    sys.exit(1)

try:
    print("[TEST] Creating documents...")
    docs = create_documents(df)
    print(f"[✓] Documents created successfully: {len(docs)} documents")
except Exception as e:
    print(f"[✗] Failed to create documents: {e}")
    sys.exit(1)

print("\n[✓✓✓] All imports and basic functionality verified successfully! ✓✓✓")
print("The project is ready to run.")
