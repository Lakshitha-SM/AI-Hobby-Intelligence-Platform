#!/usr/bin/env python
"""
Simple inline test without Rich - shows raw output
"""
import sys
import os

os.chdir("c:\\Users\\Lakshitha SM\\Desktop\\AI Hobby Intelligence Platform")
sys.path.insert(0, os.getcwd())

print("\n" + "=" * 70)
print("AI HOBBY INTELLIGENCE PLATFORM - INLINE EXECUTION TEST")
print("=" * 70 + "\n")

# Test 1: Imports
print("[TEST 1] Testing imports...")
try:
    print("  → Importing dataset.loader...")
    from dataset.loader import load_dataset, create_documents
    print("    ✓ dataset.loader imported")
    
    print("  → Importing embeddings.generator...")
    from embeddings.generator import EmbeddingGenerator
    print("    ✓ embeddings.generator imported")
    
    print("  → Importing vector_db...")
    from vector_db import HobbyVectorDB
    print("    ✓ vector_db imported")
    
    print("  → Importing llm_manager...")
    from llm_manager import GeminiLLMManager
    print("    ✓ llm_manager imported")
    
    print("  → Importing Rich console...")
    from rich.console import Console
    print("    ✓ Rich imported")
    
    print("\n✓ All imports successful!\n")
except Exception as e:
    print(f"\n✗ Import failed: {e}\n")
    sys.exit(1)

# Test 2: Load dataset
print("[TEST 2] Loading dataset...")
try:
    df = load_dataset()
    print(f"  ✓ Dataset loaded: {len(df)} records\n")
    print("  Sample records:")
    for idx, row in df.head(3).iterrows():
        print(f"    • {row['hobby']:15} | {row['style']:25} | {row['skill_level']}")
    print()
except Exception as e:
    print(f"✗ Dataset loading failed: {e}\n")
    sys.exit(1)

# Test 3: Create documents
print("[TEST 3] Creating documents...")
try:
    documents = create_documents(df)
    print(f"  ✓ Documents created: {len(documents)} documents\n")
except Exception as e:
    print(f"✗ Document creation failed: {e}\n")
    sys.exit(1)

# Test 4: Vector DB
print("[TEST 4] Initializing vector database...")
try:
    vector_db = HobbyVectorDB()
    vector_db.connect()
    doc_count = vector_db.get_document_count()
    print(f"  ✓ Vector DB connected: {doc_count} documents indexed\n")
except Exception as e:
    print(f"✗ Vector DB failed: {e}\n")
    sys.exit(1)

# Test 5: Embeddings
print("[TEST 5] Loading embedding model...")
try:
    print("  (This will download the model on first run - ~120MB)")
    embedding_gen = EmbeddingGenerator()
    embedding_gen.load_model()
    print(f"  ✓ Model loaded with dimension: {embedding_gen.dimension}\n")
except Exception as e:
    print(f"✗ Embedding model failed: {e}\n")
    sys.exit(1)

# Test 6: Semantic search
print("[TEST 6] Testing semantic search...")
try:
    test_query = "beautiful dark sky photography"
    query_embedding = embedding_gen.generate_query_embedding(test_query)
    results = vector_db.search_semantic(query_embedding, top_k=3)
    print(f"  Query: '{test_query}'")
    print(f"  ✓ Found {len(results)} results:\n")
    for i, res in enumerate(results, 1):
        print(f"    {i}. {res['metadata'].get('style'):30} (Similarity: {res['similarity_score']}%)")
    print()
except Exception as e:
    print(f"✗ Semantic search failed: {e}\n")
    sys.exit(1)

# Test 7: LLM Manager
print("[TEST 7] Initializing LLM manager...")
try:
    llm_manager = GeminiLLMManager()
    api_initialized = llm_manager.initialize_client()
    mode = "Live Gemini API" if not llm_manager.is_simulated else "Simulation Mode"
    print(f"  ✓ LLM manager initialized in: {mode}\n")
except Exception as e:
    print(f"✗ LLM manager failed: {e}\n")
    sys.exit(1)

# Test 8: RAG Pipeline
print("[TEST 8] Testing RAG pipeline...")
try:
    test_query = "gothic calligraphy with gold"
    query_embedding = embedding_gen.generate_query_embedding(test_query)
    retrieved = vector_db.search_semantic(query_embedding, top_k=2)
    
    if retrieved:
        print(f"  Query: '{test_query}'")
        print(f"  Retrieved context:")
        for i, doc in enumerate(retrieved, 1):
            print(f"    {i}. {doc['metadata'].get('style')} - {doc['metadata'].get('usage')}")
        
        result = llm_manager.query_pipeline(test_query, retrieved)
        print(f"\n  ✓ RAG pipeline successful!")
        print(f"    - Prompt tokens: {result['prompt_tokens']}")
        print(f"    - Response tokens: {result['response_tokens']}")
        print(f"    - Total tokens: {result['total_tokens']}")
        print(f"    - Mode: {mode}\n")
    else:
        print("  ⚠ No results retrieved\n")
except Exception as e:
    print(f"✗ RAG pipeline failed: {e}\n")
    sys.exit(1)

print("=" * 70)
print("✓✓✓ ALL TESTS PASSED! ✓✓✓")
print("=" * 70)
print("\nThe platform is fully functional and ready!")
print("\nTo run the interactive platform, execute:")
print("  python main.py")
print()
