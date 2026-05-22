import os
import chromadb
from chromadb.config import Settings

class HobbyVectorDB:
    """
    HobbyVectorDB manages persistent storage and retrieval of vector embeddings 
    and associated metadata using ChromaDB.
    """
    def __init__(self, db_dir=None, collection_name="hobby_intelligence"):
        """
        Initializes the ChromaDB persistent client.
        Args:
            db_dir (str): Path to persistent storage directory.
            collection_name (str): Name of the ChromaDB collection.
        """
        if db_dir is None:
            # Set default path relative to this script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_dir = os.path.join(base_dir, "chroma_storage")
            
        self.db_dir = db_dir
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        
    def connect(self, console=None):
        """
        Establish a connection to the persistent ChromaDB.
        """
        if self.collection is not None:
            return
            
        message = f"Connecting to persistent ChromaDB at '{self.db_dir}'..."
        if console:
            with console.status(f"[bold yellow]{message}[/bold yellow]") as status:
                self.client = chromadb.PersistentClient(path=self.db_dir)
                # Configure metadata to use cosine similarity space
                self.collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
            console.print(f"[bold green]✓[/bold green] Connected to ChromaDB. Collection: [cyan]'{self.collection_name}'[/cyan] (Cosine Similarity)")
        else:
            print(message)
            self.client = chromadb.PersistentClient(path=self.db_dir)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"✓ Connected to ChromaDB. Collection: '{self.collection_name}'")

    def get_document_count(self):
        """
        Returns the number of documents currently stored in the collection.
        """
        if self.collection is None:
            self.connect()
        return self.collection.count()

    def store_documents(self, documents_list, embeddings_list, console=None):
        """
        Upserts a batch of documents and their corresponding pre-computed embeddings into ChromaDB.
        Args:
            documents_list (list of dict): List of document dicts with 'id', 'text', and 'metadata'.
            embeddings_list (list of list of float): List of embeddings matching document index.
            console: Rich console for drawing status.
        """
        if self.collection is None:
            self.connect(console)
            
        ids = [doc["id"] for doc in documents_list]
        texts = [doc["text"] for doc in documents_list]
        metadatas = [doc["metadata"] for doc in documents_list]
        
        message = f"Storing {len(documents_list)} documents in vector database..."
        if console:
            with console.status(f"[bold magenta]{message}[/bold magenta]") as status:
                self.collection.upsert(
                    ids=ids,
                    embeddings=embeddings_list,
                    documents=texts,
                    metadatas=metadatas
                )
            console.print(f"[bold green]✓[/bold green] Success. Vector Database synchronized with [cyan]{len(ids)}[/cyan] records.")
        else:
            print(message)
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings_list,
                documents=texts,
                metadatas=metadatas
            )
            print(f"✓ Success. Synchronized {len(ids)} records in vector database.")

    def add_single_document(self, doc_id, text, metadata, embedding, console=None):
        """
        Adds a single new document to ChromaDB. Excellent for showing real-time updates.
        """
        if self.collection is None:
            self.connect(console)
            
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )
        if console:
            console.print(f"[bold green]✓[/bold green] Document [cyan]'{doc_id}'[/cyan] successfully indexed into vector database.")
        else:
            print(f"✓ Document '{doc_id}' indexed.")

    def search_semantic(self, query_embedding, top_k=3, console=None):
        """
        Performs vector similarity search against the collection using a pre-computed query embedding.
        Args:
            query_embedding (list of float): Vector embedding of the search query.
            top_k (int): Number of nearest documents to return.
            console: Rich console.
        Returns:
            list of dict: Structured search results sorted by relevance.
        """
        if self.collection is None:
            self.connect(console)
            
        # If database is empty, return empty list
        if self.get_document_count() == 0:
            return []
            
        # Bound top_k by database size
        actual_k = min(top_k, self.get_document_count())
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=actual_k,
            include=["documents", "metadatas", "distances"]
        )
        
        parsed_results = []
        if not results or not results["ids"] or len(results["ids"][0]) == 0:
            return parsed_results
            
        # ChromaDB query returns arrays. We extract the first element since we passed a single query.
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0] # for cosine space: cosine distance = 1 - cosine_similarity
        
        for i in range(len(ids)):
            # Convert cosine distance to standard similarity percentage: (1 - distance) * 100
            cosine_dist = distances[i]
            similarity_score = (1.0 - cosine_dist) * 100.0
            
            parsed_results.append({
                "id": ids[i],
                "text": documents[i],
                "metadata": metadatas[i],
                "distance": cosine_dist,
                "similarity_score": round(similarity_score, 2)
            })
            
        return parsed_results

    def clear_collection(self, console=None):
        """
        Removes all documents from the current collection to force a rebuild.
        """
        if self.collection is None:
            self.connect(console)
        try:
            count = self.get_document_count()
            if count > 0:
                # Delete all by query/ids
                all_ids = self.collection.get()["ids"]
                if all_ids:
                    self.collection.delete(ids=all_ids)
                if console:
                    console.print(f"[bold red]✗[/bold red] Cleared [yellow]{count}[/yellow] items from the ChromaDB collection.")
                else:
                    print(f"✗ Cleared {count} items from ChromaDB collection.")
        except Exception as e:
            if console:
                console.print(f"[bold red]Error clearing collection: {e}[/bold red]")
            else:
                print(f"Error clearing collection: {e}")

if __name__ == "__main__":
    # Diagnostics check
    print("[Vector DB] Initializing self-test...")
    db = HobbyVectorDB()
    db.connect()
    print(f"[Vector DB] Document count: {db.get_document_count()}")
