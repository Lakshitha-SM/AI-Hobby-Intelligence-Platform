#!/usr/bin/env python
"""
Auto-execution test for the AI Hobby Intelligence Platform
This script tests all the core functionality without user interaction
"""
import sys
import os

print("=" * 70)
print("AI HOBBY INTELLIGENCE PLATFORM - AUTOMATED TEST")
print("=" * 70)

# Test imports
print("\n[TEST 1] Testing imports...")
try:
    from dataset.loader import load_dataset, create_documents
    from embeddings.generator import EmbeddingGenerator
    from vector_db import HobbyVectorDB
    from llm_manager import GeminiLLMManager
    print("✓ All modules imported successfully!")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test dataset loading
print("\n[TEST 2] Loading dataset...")
try:
    df = load_dataset()
    print(f"✓ Dataset loaded: {len(df)} records")
except Exception as e:
    print(f"✗ Dataset loading failed: {e}")
    sys.exit(1)

# Test document creation
print("\n[TEST 3] Creating documents...")
try:
    documents = create_documents(df)
    print(f"✓ Documents created: {len(documents)} documents")
    print(f"  Sample document ID: {documents[0]['id']}")
except Exception as e:
    print(f"✗ Document creation failed: {e}")
    sys.exit(1)

# Test vector DB initialization
print("\n[TEST 4] Initializing vector database...")
try:
    vector_db = HobbyVectorDB()
    vector_db.connect()
    doc_count = vector_db.get_document_count()
    print(f"✓ Vector DB initialized: {doc_count} documents in database")
except Exception as e:
    print(f"✗ Vector DB initialization failed: {e}")
    sys.exit(1)

# Test embedding generator
print("\n[TEST 5] Loading embedding model...")
try:
    embedding_gen = EmbeddingGenerator()
    embedding_gen.load_model()
    print(f"✓ Embedding model loaded with dimension: {embedding_gen.dimension}")
except Exception as e:
    print(f"✗ Embedding model loading failed: {e}")
    sys.exit(1)

# Test embedding generation and semantic search
print("\n[TEST 6] Testing semantic search...")
try:
    test_query = "beautiful photography with dark skies"
    query_embedding = embedding_gen.generate_query_embedding(test_query)
    results = vector_db.search_semantic(query_embedding, top_k=3)
    print(f"✓ Semantic search successful: Found {len(results)} results")
    if results:
        print(f"  Top match: {results[0]['metadata'].get('style')} (Similarity: {results[0]['similarity_score']}%)")
except Exception as e:
    print(f"✗ Semantic search failed: {e}")
    sys.exit(1)

# Test LLM manager
print("\n[TEST 7] Initializing LLM manager...")
try:
    llm_manager = GeminiLLMManager()
    api_initialized = llm_manager.initialize_client()
    mode = "Live API" if not llm_manager.is_simulated else "Simulation Mode"
    print(f"✓ LLM manager initialized in {mode}")
except Exception as e:
    print(f"✗ LLM manager initialization failed: {e}")
    sys.exit(1)

# Test RAG pipeline
print("\n[TEST 8] Testing RAG pipeline...")
try:
    test_query = "gothic calligraphy with gold details"
    query_embedding = embedding_gen.generate_query_embedding(test_query)
    retrieved = vector_db.search_semantic(query_embedding, top_k=2)
    
    if retrieved:
        result = llm_manager.query_pipeline(test_query, retrieved)
        print(f"✓ RAG pipeline successful")
        print(f"  Response tokens: {result['response_tokens']}")
        print(f"  Total tokens used: {result['total_tokens']}")
        print(f"  Response preview: {result['response_text'][:100]}...")
    else:
        print("⚠ No results retrieved for RAG pipeline test")
except Exception as e:
    print(f"✗ RAG pipeline test failed: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✓✓✓ ALL TESTS PASSED! ✓✓✓")
print("The AI Hobby Intelligence Platform is fully functional!")
print("=" * 70)
print("\nYou can now run the interactive platform with:")
print("  python main.py")
