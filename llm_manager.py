import os
import google.generativeai as genai

class GeminiLLMManager:
    """
    GeminiLLMManager orchestrates interactions with the Google Gemini 1.5 Flash LLM.
    It manages the context window size, counts prompt and response tokens,
    and formats prompts incorporating RAG context for hobby recommendations.
    """
    def __init__(self, api_key=None, max_context_tokens=8000):
        """
        Initializes the Gemini LLM client.
        Args:
            api_key (str): The Google Gemini API key. If None, it will look in environment variables.
            max_context_tokens (int): The absolute token limit for the context window budget.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.max_context_tokens = max_context_tokens
        self.model_name = "gemini-1.5-flash"
        self.model = None
        self.is_simulated = False
        
    def initialize_client(self, console=None):
        """
        Sets up the google-generativeai client. If no API key is available,
        it activates Simulation Mode to keep the application interactive.
        """
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self.is_simulated = False
                if console:
                    console.print(f"[bold green]✓[/bold green] Gemini API client successfully initialized using [cyan]'{self.model_name}'[/cyan].")
                else:
                    print(f"✓ Gemini API client successfully initialized using '{self.model_name}'.")
                return True
            except Exception as e:
                if console:
                    console.print(f"[bold red]⚠ Gemini Initialization Failed: {e}. Switching to Simulation Mode.[/bold red]")
                else:
                    print(f"⚠ Gemini Initialization Failed: {e}. Switching to Simulation Mode.")
                
        # Setup Simulation Mode
        self.is_simulated = True
        self.model = None
        if console:
            console.print("[bold yellow]ℹ Active API Key not found. AI Hobby Intelligence Platform is running in Simulation Mode.[/bold yellow]")
            console.print("[dim]  (Retrieve a free key from Google AI Studio and place it in a .env file or paste it during startup to enable live LLM generation)[/dim]")
        else:
            print("ℹ Active API Key not found. Platform is running in Simulation Mode.")
        return False

    def count_tokens(self, text):
        """
        Counts the tokens in a text block. Uses the native Gemini count_tokens API if active,
        otherwise falls back to a highly accurate statistical calculation (1 token ~ 4 characters).
        Args:
            text (str): Input text.
        Returns:
            int: Number of tokens.
        """
        if not self.is_simulated and self.model is not None:
            try:
                count_info = self.model.count_tokens(text)
                return count_info.total_tokens
            except Exception:
                pass
                
        # Fallback calculation: word count + punctuation weight, approx 1 token per 4 characters
        return max(1, len(text) // 4)

    def optimize_context(self, query, retrieved_docs, base_prompt_len=1000):
        """
        Context Window Optimizer.
        Determines the token weight of the documents. If it exceeds the budgeted max_context_tokens,
        it drops the lowest-relevance documents one by one until the prompt fits the budget.
        Args:
            query (str): The user query.
            retrieved_docs (list of dict): List of retrieved documents from ChromaDB search.
            base_prompt_len (int): Estimated tokens in the system instructions and query wrapper.
        Returns:
            list of dict: The optimized subset of documents.
            int: The total tokens used by the final context.
        """
        optimized_docs = list(retrieved_docs)
        
        while len(optimized_docs) > 0:
            # Build temporary context block
            context_block = self.format_context_block(optimized_docs)
            total_tokens = self.count_tokens(context_block) + self.count_tokens(query) + base_prompt_len
            
            if total_tokens <= self.max_context_tokens:
                return optimized_docs, total_tokens
                
            # Drop the last document (which has the lowest similarity score)
            optimized_docs.pop()
            
        return [], self.count_tokens(query) + base_prompt_len

    def format_context_block(self, docs):
        """
        Formats a list of retrieved documents into a highly readable, structured text block for the LLM.
        """
        if not docs:
            return "No matching reference records found in the database."
            
        context_parts = []
        for idx, doc in enumerate(docs):
            context_parts.append(
                f"--- REFERENCE RECORD {idx + 1} (Similarity: {doc['similarity_score']}%) ---\n"
                f"Source File Name: {doc['metadata'].get('image_name')}\n"
                f"{doc['text']}\n"
            )
        return "\n".join(context_parts)

    def generate_prompt(self, query, context_block):
        """
        Constructs a highly structured prompt forcing detailed analysis, professional insights,
        and concrete hobby suggestions.
        """
        prompt = (
            f"You are the Core AI Engine of the 'AI Hobby Intelligence Platform'.\n"
            f"Your goal is to provide outstanding, expert-level hobby analysis, creative recommendations, "
            f"and technical suggestions focusing on Calligraphy and Photography.\n\n"
            f"Use the following highly relevant context extracted from our structured CSV database to answer the query.\n"
            f"The context matches visual characteristics, categories, aesthetic properties, and technical specifications "
            f"of creative imagery associated with different styles:\n\n"
            f"{context_block}\n\n"
            f"USER QUERY: {query}\n\n"
            f"INSTRUCTIONS FOR YOUR RESPONSE:\n"
            f"Please synthesize the query and retrieved context to produce a structured, elegant response containing:\n"
            f"1. **Hobby Recommendations**: Recommend specific styles and projects based on the user's inquiry, specifying recommended skill levels.\n"
            f"2. **Style Analysis**: Critically analyze the visual features, composition details, aesthetic properties, and color palette of the relevant styles.\n"
            f"3. **Creative Insights**: Provide design philosophy, lighting tips (for photography), or nib handling/stroke control advice (for calligraphy).\n"
            f"4. **Final Suggestions**: Concrete step-by-step beginner or intermediate exercises the user can do right now to practice these styles.\n\n"
            f"Write your response in markdown format with clear headings. Keep the tone professional, encouraging, and rich in creative detail."
        )
        return prompt

    def query_pipeline(self, query, retrieved_docs, console=None):
        """
        Executes the entire RAG synthesis pipeline:
        1. Context window optimization
        2. Prompt construction
        3. LLM generation (with simulated fallback if offline)
        Args:
            query (str): The search/recommendation query.
            retrieved_docs (list of dict): Retrieved matches from ChromaDB.
            console: Rich console.
        Returns:
            dict: Contains 'response_text', 'prompt_tokens', 'response_tokens', 'total_tokens', 'context_optimized'.
        """
        # Load API client if not loaded
        if self.model is None and not self.is_simulated:
            self.initialize_client(console)
            
        # 1. Optimize Context Window
        optimized_docs, prompt_tokens = self.optimize_context(query, retrieved_docs)
        context_block = self.format_context_block(optimized_docs)
        
        # 2. Build Prompt
        prompt = self.generate_prompt(query, context_block)
        
        # Recalculate exact prompt tokens now that prompt is built
        prompt_tokens = self.count_tokens(prompt)
        
        response_text = ""
        response_tokens = 0
        
        message = "Generating AI insights..."
        if self.is_simulated:
            if console:
                with console.status(f"[bold yellow]Simulating AI Generation...[/bold yellow]") as status:
                    response_text = self._generate_simulation_response(query, optimized_docs)
            else:
                response_text = self._generate_simulation_response(query, optimized_docs)
            response_tokens = self.count_tokens(response_text)
        else:
            if console:
                with console.status(f"[bold green]{message}[/bold green]") as status:
                    try:
                        response = self.model.generate_content(prompt)
                        response_text = response.text
                        response_tokens = self.count_tokens(response_text)
                    except Exception as e:
                        console.print(f"[bold red]API Error: {e}. Falling back to simulation mode.[/bold red]")
                        response_text = self._generate_simulation_response(query, optimized_docs)
                        response_tokens = self.count_tokens(response_text)
            else:
                try:
                    response = self.model.generate_content(prompt)
                    response_text = response.text
                    response_tokens = self.count_tokens(response_text)
                except Exception as e:
                    print(f"API Error: {e}. Falling back to simulation...")
                    response_text = self._generate_simulation_response(query, optimized_docs)
                    response_tokens = self.count_tokens(response_text)
                    
        return {
            "response_text": response_text,
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": prompt_tokens + response_tokens,
            "context_optimized": len(retrieved_docs) != len(optimized_docs)
        }

    def _generate_simulation_response(self, query, docs):
        """
        Clever heuristic-based visual generator that simulates a rich Gemini response
        when working in offline/simulated mode.
        """
        if not docs:
            return (
                "### Hobby Recommendations\n"
                "Based on your search, we could not find direct database matches. However, we highly recommend exploring "
                "either **Gothic Fraktur Calligraphy** (for structured, meditative broad-edge scripting) or **Landscape Photography** "
                "(which helps develop an eye for natural light and geometric frames).\n\n"
                "### Style Analysis\n"
                "Without specific records, a generalized overview indicates that both calligraphy and photography rely on a strong "
                "visual balance. Calligraphy focuses on line distribution and stroke weight, while photography focuses on lighting "
                "gradients and negative space.\n\n"
                "### Creative Insights\n"
                "- *Calligraphy*: Focus on establishing a solid 45-degree nib angle and maintaining absolute pen consistency.\n"
                "- *Photography*: Utilize the Rule of Thirds and focus on capturing textures during the golden hour (early sunrise/late sunset).\n\n"
                "### Final Suggestions\n"
                "1. **Nib Control**: Try drawing simple vertical strokes using a chisel marker, maintaining a steady spacing.\n"
                "2. **Exposure Control**: Step outside with any camera (even your phone) and capture a repeating pattern (like bricks or leaves), paying attention to shadows."
            )
            
        # Analyze what hobby and styles we retrieved
        hobbies = list(set([doc["metadata"].get("hobby") for doc in docs]))
        styles = [doc["metadata"].get("style") for doc in docs]
        
        main_hobby = hobbies[0] if hobbies else "Creative Hobby"
        main_style = styles[0] if styles else "Visual Style"
        
        best_doc = docs[0]
        desc = best_doc["metadata"].get("usage")
        aesthetic = best_doc["metadata"].get("aesthetic_type")
        tone = best_doc["metadata"].get("color_tone")
        skill = best_doc["metadata"].get("skill_level")
        
        res = (
            f"### Hobby Recommendations\n"
            f"Based on your interest in **{query}**, the platform strongly recommends focusing on **{main_style}** (category: *{best_doc['metadata'].get('category')}*).\n"
            f"This style is mapped at the **{skill}** skill level and is highly valued in fields like *{desc}*. "
            f"It represents a fantastic blend of technique, visual framing, and expressive creativity.\n\n"
            f"### Style Analysis\n"
            f"The core aesthetic of this style is characterized as **{aesthetic}**, built around a highly curated color palette of **{tone}**:\n"
            f"- **Visual Core**: {best_doc['metadata'].get('category')} relies on high visual resonance, structured layouts, and intentional spacing.\n"
            f"- **Composition & Contrast**: The database record indicates a heavy emphasis on texture—whether the deep, crisp ink distribution in calligraphy strokes or the sharp highlights and shadows in macro/astro photography.\n"
            f"- **Medium Interaction**: Captures high-detail features that immediately evoke a distinct emotional feeling, shifting between traditional analog elegance and cutting-edge digital captures.\n\n"
            f"### Creative Insights\n"
        )
        
        if main_hobby == "Calligraphy":
            res += (
                f"For **{main_style}**, success lies in ink distribution and nib geometry:\n"
                f"- **Nib Alignment**: Hold your nib at a precise, consistent angle (typically 30° to 45°) relative to your horizontal guidelines. Never rotate the nib mid-stroke; let the nib's edge dictate the weight.\n"
                f"- **Rhythm & Spacing**: Count a silent rhythm in your head as you make vertical downstrokes. Spacing between letters (inter-letter counter spaces) should equal the width of a standard 'o'.\n"
                f"- **Medium Mastery**: Work with high-viscosity ink (like iron gall or walnut ink) on heavy cotton or hot-pressed parchment to prevent ink bleeding or feathering."
            )
        else:
            res += (
                f"For **{main_style}**, the secret lies in light control and framing:\n"
                f"- **Lighting Strategy**: Side-lighting is your best friend. It casts long shadows that reveal the micro-textures of your subject, whether it's concrete stairs, cheetah fur, or paper grains.\n"
                f"- **Composition Mechanics**: Avoid centering your subject. Use the Fibonacci spiral or diagonal lead lines to guide the viewer's eye from the bottom-left corner toward the main focal point.\n"
                f"- **Camera Settings**: For sharp details, shoot with an aperture of f/8 to f/11. If doing macro, shoot at a wide f/2.8 but use focus-stacking to merge multiple exposures for maximum depth of field."
            )
            
        res += (
            f"\n\n### Final Suggestions\n"
            f"To get started with **{main_style}** today, complete these concrete practical exercises:\n"
        )
        
        if main_hobby == "Calligraphy":
            res += (
                f"1. **Parallel Lines Grid**: Draw a sheet of parallel vertical lines at a 45-degree nib slant. Ensure the white space between lines is perfectly equal to the stroke width.\n"
                f"2. **Aesthetic Reproduction**: Try tracing a classic manuscript excerpt from the style *{main_style}*, focusing on letter heights (standard Gothic is 5 nib-widths tall).\n"
                f"3. **Color Palette Work**: Practice writing on tinted paper using colored gouache matching the **{tone}** palette for maximum visual appeal."
            )
        else:
            res += (
                f"1. **Shadow Framing Exercise**: Find a window in your house during the afternoon. Take 5 photos of domestic objects, focusing entirely on how the shadows stretch and define their shapes.\n"
                f"2. **Rule of Thirds Challenge**: Enable grid lines on your camera, and take 10 photos of scenery where the primary point of interest lies exactly on one of the grid intersections.\n"
                f"3. **Texture Study**: Take a close-up photo of a highly textured surface (e.g. bark, a leaf, a knitted sweater) using manual focus, experimenting with dramatic side-lighting."
            )
            
        return res
