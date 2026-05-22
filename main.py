import os
import sys
import time
from dotenv import load_dotenv

# Import our modular components
from dataset.loader import load_dataset, create_documents, add_custom_entry
from embeddings.generator import EmbeddingGenerator
from vector_db import HobbyVectorDB
from llm_manager import GeminiLLMManager

# Import Rich library for advanced and professional terminal layouts, styling, panels, and menus
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.markdown import Markdown
    from rich.prompt import Prompt, IntPrompt
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn
    from rich.box import ROUNDED, HEAVY
    from rich.columns import Columns
except ImportError:
    print("Error: 'rich' library is not fully installed yet. Please wait for requirements to install completely.")
    sys.exit(1)

# Load environment variables from .env file if it exists
load_dotenv()

# Initialize Rich Console
console = Console()

class AIHobbyPlatformCLI:
    """
    Main controller class for the AI Hobby Intelligence Platform CLI.
    """
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.vector_db = HobbyVectorDB()
        self.llm_manager = GeminiLLMManager()
        self.df = None
        self.documents = None

    def display_banner(self):
        """
        Draws a stunning ASCII banner for a premium first impression.
        """
        banner_text = (
            "   ___   ____                  __   __            __  __         \n"
            "  / _ | /  _/  /__ ___  ______/ /  / /_  __ __   / / / /__  ___ _\n"
            " / __ |_/ /   / _ / _ \\/ __/ _  /  / _ \\/ // /  / _ /  _ \\/ _ `/\n"
            "/_/ |_/___/  /___/_//_/__/\\_,_/  /_.__/\\_, /  /_//_\\___/\\_, / \n"
            "   I N T E L L I G E N C E   P L A T F O R M   /___/        /___/  \n"
        )
        colored_banner = Text(banner_text, style="bold cyan")
        
        banner_panel = Panel(
            colored_banner,
            title="[bold white]v1.0.0 Production-Ready Release[/bold white]",
            subtitle="[dim yellow]RAG-Optimized Semantic Search & Generative AI Analysis[/dim yellow]",
            border_style="cyan",
            box=HEAVY,
            padding=(0, 2)
        )
        console.print(banner_panel)

    def verify_api_key(self):
        """
        Checks for the Gemini API Key. If missing, allows the user to paste it dynamically
        or fall back gracefully to offline Simulation Mode.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            console.print(Panel(
            "[bold yellow]Google Gemini API Key Missing[/bold yellow]\n\n"
            "The platform will run in [bold cyan]Simulation Mode[/bold cyan] out-of-the-box.\n"
            "To enable [bold green]Live AI Synthesis[/bold green] via Google's Gemini 1.5 Flash model:\n"
            "1. Visit https://aistudio.google.com/ to obtain a free API key.\n"
            "2. Paste it below to run with real-time LLM integration (saved locally in .env).\n"
            "3. Or, press [bold green]ENTER[/bold green] to proceed in simulated mode.",
            title="[bold red]Security & Connection Config[/bold red]",
            border_style="yellow",
            box=ROUNDED
        ))
        
        pasted_key = Prompt.ask("[bold green]Paste your GEMINI_API_KEY (optional)[/bold green]", password=True).strip()
        if pasted_key:
            # Save to .env file for future runs
            with open(".env", "a+") as f:
                f.write(f"\nGEMINI_API_KEY={pasted_key}\n")
            os.environ["GEMINI_API_KEY"] = pasted_key
            self.llm_manager.api_key = pasted_key
            console.print("[bold green]✓ API Key loaded and cached in .env file![/bold green]\n")
        else:
            console.print("[bold yellow]⚠ Proceeding in offline Simulation Mode.[/bold yellow]\n")

    def run_bootstrap_diagnostics(self):
        """
        Runs startup validation checks:
        1. Loads/generates the CSV dataset.
        2. Validates vector database connection.
        3. Initializes embeddings and indexes records if database is empty.
        4. Initializes Gemini LLM manager.
        """
        console.print(Panel(
            "[bold white]Running System Diagnostics & Component Synchronization...[/bold white]",
            border_style="dim white",
            box=ROUNDED
        ))
        
        # 1. Dataset Initialization
        with console.status("[bold blue]Checking CSV dataset...[/bold blue]") as status:
            self.df = load_dataset()
            self.documents = create_documents(self.df)
            time.sleep(0.5)
        console.print(f"[bold green]✓[/bold green] CSV Knowledge Base loaded. Found [cyan]{len(self.df)}[/cyan] visual asset records.")
        
        # 2. Vector DB connection
        self.vector_db.connect(console)
        
        # 3. Model Loading & Ingest
        db_count = self.vector_db.get_document_count()
        if db_count == 0:
            console.print(Panel(
                "[bold yellow]Vector DB Empty! Beginning Auto-Embedding & Indexing Pipeline...[/bold yellow]\n"
                "The SentenceTransformer '[cyan]all-MiniLM-L6-v2[/cyan]' will encode your structured database features "
                "into [green]384-dimensional dense vectors[/green] and index them in persistent ChromaDB storage.",
                border_style="yellow", box=ROUNDED
            ))
            
            # Load transformer model (may download on first run)
            self.embedding_generator.load_model(console)
            
            # Extract texts to embed
            texts_to_embed = [doc["text"] for doc in self.documents]
            
            # Progress bar for encoding and database storage
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(bar_width=40),
                MofNCompleteColumn(),
                TextColumn("[bold green]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                # We show batch-wise encoding progress
                task = progress.add_task("Indexing records in ChromaDB...", total=len(texts_to_embed))
                
                embeddings = []
                batch_size = 8
                for i in range(0, len(texts_to_embed), batch_size):
                    batch_texts = texts_to_embed[i:i+batch_size]
                    batch_embs = self.embedding_generator.generate_embeddings(batch_texts, batch_size=batch_size)
                    embeddings.extend(batch_embs)
                    progress.update(task, advance=len(batch_texts))
                    
            # Ingest to DB
            self.vector_db.store_documents(self.documents, embeddings, console)
        else:
            console.print(f"[bold green]✓[/bold green] Persistent Vector Storage verified. Indexed documents: [cyan]{db_count}[/cyan].")
            
        # 4. LLM Client setup
        self.llm_manager.initialize_client(console)
        console.print("[bold green]✓ Platform successfully bootstrapped and ready![/bold green]\n")

    def run_menu_loop(self):
        """
        Interactive loop driving the CLI.
        """
        while True:
            console.print("\n" + "=" * 65)
            console.print("[bold cyan]MAIN MENU - AI HOBBY INTELLIGENCE PLATFORM[/bold cyan]")
            console.print("=" * 65)
            
            console.print("[bold yellow]1.[/bold yellow] Explore Visual Asset Database (Pandas Viewer)")
            console.print("[bold yellow]2.[/bold yellow] Direct Semantic Search Engine (Vector DB retrieve-only)")
            console.print("[bold yellow]3.[/bold yellow] AI-Powered Creative Assistant (Full RAG Pipeline)")
            console.print("[bold yellow]4.[/bold yellow] Personal Hobby Profile Matching Wizard (Premium)")
            console.print("[bold yellow]5.[/bold yellow] Register & Index New Hobby Asset (Real-time updates)")
            console.print("[bold yellow]6.[/bold yellow] View RAG Concepts & Architecture Diagnostics")
            console.print("[bold yellow]7.[/bold yellow] Exit Platform")
            console.print("-" * 65)
            
            choice = Prompt.ask(
                "[bold green]Select Option (1-7)[/bold green]",
                choices=["1", "2", "3", "4", "5", "6", "7"],
                default="3"
            )
            
            if choice == "1":
                self.option_explore_database()
            elif choice == "2":
                self.option_semantic_search()
            elif choice == "3":
                self.option_rag_assistant()
            elif choice == "4":
                self.option_hobby_wizard()
            elif choice == "5":
                self.option_register_asset()
            elif choice == "6":
                self.option_show_diagnostics()
            elif choice == "7":
                console.print(Panel(
                    "[bold green]Thank you for using the AI Hobby Intelligence Platform![/bold green]\n"
                    "Keep capturing light, shaping letters, and expanding your creative horizons.",
                    border_style="cyan", box=ROUNDED
                ))
                break

    def option_explore_database(self):
        """
        Displays a structured, highly legible grid of the CSV records.
        Allows filtering by Hobby (Photography vs Calligraphy) to keep exploration tight.
        """
        console.print(Panel(
            "[bold white]Explore Asset Database[/bold white]\n"
            "Browse the underlying CSV knowledge base containing creative records, visual features, and metadata.",
            border_style="cyan", box=ROUNDED
        ))
        
        filter_hobby = Prompt.ask(
            "Filter by Hobby?",
            choices=["All", "Calligraphy", "Photography"],
            default="All"
        )
        
        df_to_show = self.df
        if filter_hobby != "All":
            df_to_show = self.df[self.df["hobby"] == filter_hobby]
            
        table = Table(
            title=f"Knowledge Base Records - {filter_hobby}",
            title_style="bold magenta",
            border_style="dim white",
            header_style="bold cyan",
            box=ROUNDED,
            show_lines=True
        )
        
        table.add_column("Hobby", style="yellow")
        table.add_column("Style Name", style="bold white")
        table.add_column("Category", style="cyan")
        table.add_column("Color Tone Palette", style="magenta")
        table.add_column("Skill", style="green")
        table.add_column("Typical Usage / Application", style="dim white")
        
        for _, row in df_to_show.iterrows():
            table.add_row(
                str(row["hobby"]),
                str(row["style"]),
                str(row["category"]),
                str(row["color_tone"]),
                str(row["skill_level"]),
                str(row["usage"])
            )
            
        console.print(table)
        console.print(f"[dim]Total records displayed: {len(df_to_show)}[/dim]")

    def option_semantic_search(self):
        """
        Direct Vector retrieval demonstration, showcasing similarity scores, indices, and distances.
        """
        console.print(Panel(
            "[bold white]Direct Semantic Search Engine (Vector DB retrieve-only)[/bold white]\n"
            "Calculates dense vectors using the SentenceTransformer model and queries ChromaDB via Cosine Similarity.",
            border_style="cyan", box=ROUNDED
        ))
        
        query = Prompt.ask("[bold green]Enter your conceptual search query[/bold green] (e.g. 'dark sky pine forest' or 'medieval wedding script')").strip()
        if not query:
            return
            
        top_k = IntPrompt.ask("[bold green]Set Top-K nearest neighbors to retrieve[/bold green]", default=3)
        
        # 1. Embed query
        query_vector = self.embedding_generator.generate_query_embedding(query, console)
        
        # 2. Retrieve
        with console.status("[bold magenta]Querying ChromaDB vector index...[/bold magenta]") as status:
            results = self.vector_db.search_semantic(query_vector, top_k=top_k)
            time.sleep(0.3)
            
        if not results:
            console.print("[bold red]No matching records found.[/bold red]")
            return
            
        # Display retrieved vectors in a neat Table
        table = Table(
            title=f"ChromaDB Query Results for: '{query}'",
            title_style="bold magenta",
            border_style="cyan",
            header_style="bold white",
            box=ROUNDED,
            show_lines=True
        )
        
        table.add_column("Rank", justify="center", style="yellow")
        table.add_column("Document ID", style="cyan")
        table.add_column("Similarity Score", justify="right", style="bold green")
        table.add_column("Hobby", style="yellow")
        table.add_column("Style Name", style="bold white")
        table.add_column("Description Snippet", style="dim white", width=50)
        
        for rank, res in enumerate(results):
            desc = res["metadata"].get("description", "")
            desc_snippet = (desc[:140] + "...") if desc else "N/A"
            table.add_row(
                str(rank + 1),
                res["id"],
                f"{res['similarity_score']}%",
                res["metadata"].get("hobby"),
                res["metadata"].get("style"),
                desc_snippet
            )
            
        console.print(table)
        console.print("[dim]Note: Similarity is scaled from Cosine Distance: Score = (1 - Distance) * 100[/dim]")

    def option_rag_assistant(self):
        """
        The flagship feature: Complete RAG Pipeline showing context diagnostics and token analysis.
        """
        console.print(Panel(
            "[bold white]AI-Powered Creative Assistant (RAG Pipeline)[/bold white]\n"
            "Performs semantic similarity retrieval, prints the context window configuration, "
            "optimizes prompt layout, passes inputs to the Gemini LLM, and prints token statistics.",
            border_style="cyan", box=ROUNDED
        ))
        
        query = Prompt.ask("[bold green]Ask the AI anything about Calligraphy or Photography[/bold green]").strip()
        if not query:
            return
            
        # Pipeline step-by-step
        
        # Step A: Vector search
        query_vector = self.embedding_generator.generate_query_embedding(query, console)
        
        with console.status("[bold magenta]Retrieving relevant visual context...[/bold magenta]") as status:
            retrieved_docs = self.vector_db.search_semantic(query_vector, top_k=3)
            time.sleep(0.3)
            
        # Step B: PRINT retrieved context explicitly BEFORE generation
        console.print("\n" + "=" * 65)
        console.print("[bold yellow]🔍 DEBUG: RETRIEVED CONTEXT (BEFORE LLM SYNTHESIS)[/bold yellow]")
        console.print("=" * 65)
        
        for i, doc in enumerate(retrieved_docs):
            console.print(Panel(
                f"[bold cyan]Rank {i+1} Match | ID: {doc['id']} | Similarity Score: [green]{doc['similarity_score']}%[/green][/bold cyan]\n"
                f"[bold yellow]Metadata:[/bold yellow] Hobby: {doc['metadata'].get('hobby')} | Style: {doc['metadata'].get('style')} | Skill: {doc['metadata'].get('skill_level')} | Usage: {doc['metadata'].get('usage')}\n\n"
                f"{doc['text']}",
                border_style="dim cyan",
                box=ROUNDED
            ))
            
        # Step C: RAG Pipeline Generation
        pipeline_results = self.llm_manager.query_pipeline(query, retrieved_docs, console)
        
        # Step D: Print response
        console.print("\n" + "=" * 65)
        console.print("[bold green]🤖 AI GENERATION: CREATIVE ADVICE & RECOMMENDATIONS[/bold green]")
        console.print("=" * 65)
        
        md_content = Markdown(pipeline_results["response_text"])
        console.print(Panel(
            md_content,
            border_style="green",
            box=ROUNDED,
            padding=(1, 2)
        ))
        
        # Step E: Print Token and Context statistics Banner
        self.display_token_statistics(pipeline_results)

    def display_token_statistics(self, stats):
        """
        Prints highly detailed, placement-ready token counters and processing stats.
        """
        mode = "Offline Simulation Mode" if self.llm_manager.is_simulated else "Live Google Gemini 1.5 Flash"
        mode_style = "yellow" if self.llm_manager.is_simulated else "bold green"
        
        # Calculate percentage of context limit used
        limit = self.llm_manager.max_context_tokens
        pct_used = (stats["prompt_tokens"] / limit) * 100.0
        
        stats_table = Table(
            title="📊 RAG Token & Context Window Analytics",
            title_style="bold magenta",
            border_style="magenta",
            header_style="bold cyan",
            box=ROUNDED
        )
        
        stats_table.add_column("Metric Name", style="white")
        stats_table.add_column("Value / Details", style="bold yellow")
        stats_table.add_column("Context Budget & Optimization", style="dim white")
        
        stats_table.add_row(
            "AI Synthesis Engine", 
            Text(mode, style=mode_style), 
            f"Model name: {self.llm_manager.model_name}"
        )
        stats_table.add_row(
            "Prompt (Input Context) Tokens", 
            f"{stats['prompt_tokens']} tokens", 
            f"{pct_used:.1f}% of context window budget used"
        )
        stats_table.add_row(
            "Response (Output Generated) Tokens", 
            f"{stats['response_tokens']} tokens", 
            "Heuristic calculated" if self.llm_manager.is_simulated else "Native model tokenizer"
        )
        stats_table.add_row(
            "Total Pipeline Token Cost", 
            f"{stats['total_tokens']} tokens", 
            f"Budget limit constraint: {limit} tokens"
        )
        stats_table.add_row(
            "Context Truncation Filter", 
            "ACTIVE" if stats["context_optimized"] else "INACTIVE", 
            "Drops matches if prompt exceeds token limits"
        )
        
        console.print("\n")
        console.print(stats_table)
        console.print("\n")

    def option_hobby_wizard(self):
        """
        Premium Profile Matching Wizard. Mapped into full dynamic RAG query.
        """
        console.print(Panel(
            "[bold magenta]🎨 Creative Personality Profile Matching Wizard[/bold magenta]\n"
            "Complete a quick wizard describing your time, physical environment, and color goals.\n"
            "The platform will formulate an optimized multidimensional search query and synthesise "
            "a bespoke hobby blueprint.",
            border_style="magenta", box=ROUNDED
        ))
        
        hobby_choice = Prompt.ask(
            "Which medium appeals to you most?",
            choices=["Calligraphy (Ink & Pen)", "Photography (Light & Lenses)", "Either (Explore both!)"],
            default="Either (Explore both!)"
        )
        
        skill = Prompt.ask(
            "What is your creative comfort level?",
            choices=["Beginner", "Intermediate", "Advanced"],
            default="Beginner"
        )
        
        vibe = Prompt.ask(
            "Describe your visual vibe or preferred aesthetic (e.g. 'cozy and rustic', 'sleek cyberpunk', 'sacred symmetry', 'moody shadows')"
        ).strip()
        
        time_commit = Prompt.ask(
            "How much time can you practice weekly?",
            choices=["Under 2 hours (Quick sessions)", "2 to 8 hours (Deep focuses)", "Unlimited"],
            default="2 to 8 hours (Deep focuses)"
        )
        
        # Build multidimensional semantic prompt
        synthesized_query = (
            f"Recommend a {skill} level {hobby_choice} style fitting a '{vibe}' visual aesthetic. "
            f"I have a time commitment of {time_commit}."
        )
        
        console.print(f"\n[bold blue]Generated Multidimensional Query:[/bold blue] [italic white]'{synthesized_query}'[/italic white]")
        
        # Run semantic search
        query_vector = self.embedding_generator.generate_query_embedding(synthesized_query, console)
        
        with console.status("[bold magenta]Consulting knowledge bases...[/bold magenta]") as status:
            retrieved_docs = self.vector_db.search_semantic(query_vector, top_k=3)
            time.sleep(0.3)
            
        if not retrieved_docs:
            console.print("[bold red]No matching records found for your profile. Please try different settings.[/bold red]")
            return
            
        # Display Retrieved Context Summary Panel
        console.print(Panel(
            f"[bold cyan]🔍 Top Match Retrieved for Personality Matrix:[/bold cyan]\n"
            f"[bold yellow]Style Mapped:[/bold yellow] [white]{retrieved_docs[0]['metadata'].get('style')}[/white] (Relevance: [green]{retrieved_docs[0]['similarity_score']}%[/green])\n"
            f"[bold yellow]Visual Palette:[/bold yellow] {retrieved_docs[0]['metadata'].get('color_tone')}\n"
            f"[bold yellow]Ideal Applications:[/bold yellow] {retrieved_docs[0]['metadata'].get('usage')}",
            border_style="magenta", box=ROUNDED
        ))
        
        # LLM Synthesis
        pipeline_results = self.llm_manager.query_pipeline(synthesized_query, retrieved_docs, console)
        
        # Markdown Output
        console.print("\n" + "=" * 65)
        console.print("[bold magenta]✨ YOUR TAILORED CREATIVE HOBBY BLUEPRINT[/bold magenta]")
        console.print("=" * 65)
        console.print(Panel(Markdown(pipeline_results["response_text"]), border_style="magenta", box=ROUNDED, padding=(1,2)))
        
        self.display_token_statistics(pipeline_results)

    def option_register_asset(self):
        """
        Dynamically adds a custom entry into the CSV and immediately updates/indexes ChromaDB vector DB.
        """
        console.print(Panel(
            "[bold white]Register & Index New Hobby Asset[/bold white]\n"
            "This implements live dataset updating and immediate vector re-indexing.\n"
            "Once submitted, the new record will be searchable via semantic search immediately!",
            border_style="cyan", box=ROUNDED
        ))
        
        hobby = Prompt.ask("Hobby Type", choices=["Calligraphy", "Photography"])
        style = Prompt.ask("Specific Style Name (e.g., 'Modern Gothic Graffiti')").strip()
        category = Prompt.ask("Broader Category Name (e.g., 'Urban Lettering')").strip()
        description = Prompt.ask("Detailed Visual Description (1-3 sentences outlining visual features)").strip()
        aesthetic_type = Prompt.ask("Aesthetic Type / Vibe (e.g., 'Cyberpunk Grunge')").strip()
        color_tone = Prompt.ask("Curated Color Tone Palette (e.g., 'Acid Green & Matt Black')").strip()
        skill_level = Prompt.ask("Required Skill Level", choices=["Beginner", "Intermediate", "Advanced"])
        usage = Prompt.ask("Typical Usage/Application (e.g., 'Streetwear apparel graphics')").strip()
        
        if not style or not description:
            console.print("[bold red]Error: Style name and Description are required! Registration aborted.[/bold red]")
            return
            
        image_name = style.lower().replace(" ", "_") + ".jpg"
        
        new_entry = {
            "image_name": image_name,
            "hobby": hobby,
            "style": style,
            "category": category,
            "description": description,
            "aesthetic_type": aesthetic_type,
            "color_tone": color_tone,
            "skill_level": skill_level,
            "usage": usage
        }
        
        # 1. Update CSV
        with console.status("[bold green]Saving new entry to CSV dataset...[/bold green]") as status:
            self.df = add_custom_entry(new_entry)
            # Recreate docs list to match DataFrame index
            self.documents = create_documents(self.df)
            time.sleep(0.3)
            
        # 2. Get text representation of our newly added doc
        # It will be the last item in the newly generated documents list
        new_doc = self.documents[-1]
        
        # 3. Generate embedding for this new document
        new_emb = self.embedding_generator.generate_query_embedding(new_doc["text"], console)
        
        # 4. Insert into ChromaDB
        self.vector_db.add_single_document(
            doc_id=new_doc["id"],
            text=new_doc["text"],
            metadata=new_doc["metadata"],
            embedding=new_emb,
            console=console
        )
        
        console.print(Panel(
            f"[bold green]✓ Live Indexing Complete![/bold green]\n"
            f"Successfully added [bold cyan]'{style}'[/bold cyan] and synchronized persistent Vector Space.\n"
            f"You can now query this style immediately using options 2 or 3!",
            border_style="green", box=ROUNDED
        ))

    def option_show_diagnostics(self):
        """
        Displays a structured explanation of the internal RAG pipeline, LLM parameters,
        and provides future architectural recommendations. Satisfies placement-level theoretical expectations.
        """
        r_text = (
            "### How Retrieval-Augmented Generation (RAG) Works:\n"
            "Instead of fine-tuning or training heavy models on new private data, RAG connects the LLM directly "
            "to a verified knowledge source (like our structured CSV dataset):\n"
            "1. **Vector Indexing**: Documents are passed through `all-MiniLM-L6-v2` generating 384-dimensional floating point vectors "
            "that represent semantic concepts. These are stored alongside visual metadata in `ChromaDB`.\n"
            "2. **Semantic Retrieval**: A user query is embedded into the same vector space. ChromaDB performs a Cosine Similarity "
            "search, returning the top-k closest database records.\n"
            "3. **Context Construction**: The closest matching text snippets are packed into a prompt along with strict rules.\n"
            "4. **Augmented Generation**: The prompt is processed by Google's `Gemini 1.5 Flash` model, synthesizing highly customized "
            "recommendations grounded directly in facts.\n\n"
            "--- \n"
            "### AI Concepts Mapped in this System:\n"
            "* **Embeddings**: Mathematical vectors mapping text to dense coordinates where related ideas sit close together.\n"
            "* **ChromaDB**: An AI-native vector database storing coordinate dimensions to retrieve records in microseconds.\n"
            "* **Token Counting**: Tracking prompt weight to optimize speed and API costs.\n"
            "* **Context Window**: The memory ceiling of an LLM. Our system optimizes this by dropping irrelevant results if they threaten to overflow our limits.\n\n"
            "--- \n"
            "### Future Architectural Enhancements:\n"
            "1. **Hybrid Keyword Search (BM25 + Dense Vectors)**: Combines strict keyword matching (for unique camera lens models) with semantic concepts.\n"
            "2. **Agentic Query Rewriting**: Utilizes a pre-step where Gemini cleans raw user inputs (e.g. converting typos or slang) to maximize search efficiency.\n"
            "3. **Multi-Modal Vector Ingestion**: Index actual images directly into vector spaces using models like CLIP, enabling users to upload photos for calligraphy or photography critique."
        )
        
        console.print("\n")
        console.print(Panel(
            Markdown(r_text),
            title="[bold yellow]📖 RAG Technical Mechanics & Future Blueprints[/bold yellow]",
            border_style="yellow",
            box=ROUNDED,
            padding=(1,2)
        ))

def main():
    # Set console title
    if sys.platform.startswith("win"):
        os.system("title AI Hobby Intelligence Platform")
        
    cli = AIHobbyPlatformCLI()
    cli.display_banner()
    cli.verify_api_key()
    cli.run_bootstrap_diagnostics()
    cli.run_menu_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]✗ Platform execution interrupted. Exiting...[/bold red]")
        sys.exit(0)
