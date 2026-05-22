import os
from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """
    EmbeddingGenerator handles generating vector representations of text using
    the SentenceTransformers 'all-MiniLM-L6-v2' model.
    The vectors generated have 384 dimensions and are excellent for semantic similarity.
    """
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initializes the SentenceTransformer model.
        On first run, this will download the model weights (~120MB) to the local cache.
        """
        self.model_name = model_name
        self.model = None

    def load_model(self, console=None):
        """
        Lazy loads the model. Provides feedback via Rich console if provided.
        """
        if self.model is not None:
            return
        
        message = f"Loading transformer model '{self.model_name}'..."
        if console:
            with console.status(f"[bold yellow]{message}[/bold yellow] (this may take a minute on first run)") as status:
                self.model = SentenceTransformer(self.model_name)
        else:
            print(message)
            self.model = SentenceTransformer(self.model_name)
        
        # Verify dimension
        self.dimension = self.model.get_sentence_embedding_dimension()
        if console:
            console.print(f"[bold green]✓[/bold green] Transformer loaded. Embedding dimension: [cyan]{self.dimension}[/cyan]")
        else:
            print(f"✓ Transformer loaded. Dimension: {self.dimension}")

    def generate_embeddings(self, texts, batch_size=32, console=None):
        """
        Generates dense vector embeddings for a list of strings.
        Args:
            texts (list of str): The text inputs to encode.
            batch_size (int): Size of batches.
            console: Rich console for drawing status.
        Returns:
            list of list of float: A list of embedded vectors.
        """
        self.load_model(console)
        
        # sentence-transformers encode returns a numpy array, we convert to list of floats for ChromaDB
        if isinstance(texts, str):
            texts = [texts]
            
        message = f"Generating embeddings for {len(texts)} texts..."
        if console:
            with console.status(f"[bold blue]{message}[/bold blue]") as status:
                embeddings = self.model.encode(texts, batch_size=batch_size, show_progress_bar=False)
        else:
            print(message)
            embeddings = self.model.encode(texts, batch_size=batch_size, show_progress_bar=False)
            
        return [emb.tolist() for emb in embeddings]

    def generate_query_embedding(self, query, console=None):
        """
        Encodes a single user query into a vector representation.
        Args:
            query (str): The search query.
            console: Rich console for drawing status.
        Returns:
            list of float: The vector embedding.
        """
        embeddings = self.generate_embeddings([query], console=console)
        return embeddings[0]

if __name__ == "__main__":
    # Diagnostics check
    print("[Embedding Generator] Initializing self-test...")
    generator = EmbeddingGenerator()
    generator.load_model()
    
    test_text = "Beautiful astrophotography capture of the Milky Way galaxy"
    vector = generator.generate_query_embedding(test_text)
    
    print(f"[Embedding Generator] Encoded: '{test_text}'")
    print(f"[Embedding Generator] Dimensions: {len(vector)}")
    print(f"[Embedding Generator] First 5 values: {vector[:5]}")
