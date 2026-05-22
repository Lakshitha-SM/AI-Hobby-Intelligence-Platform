import os
import pandas as pd

# Define paths relative to the project directory
DATASET_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DATASET_DIR, "hobby_dataset.csv")

def generate_default_dataset():
    """
    Generates a high-quality, diverse dataset of 25 items focusing on Calligraphy and Photography,
    including detailed visual descriptions and creative features.
    """
    data = [
        # --- CALLIGRAPHY STYLES ---
        {
            "image_name": "gothic_fraktur_script.jpg",
            "hobby": "Calligraphy",
            "style": "Gothic Fraktur",
            "category": "Traditional Script",
            "description": "A close-up photograph of a medieval Latin manuscript page hand-lettered in bold Gothic Fraktur script. The letters are written with dense, heavy strokes and dramatic angular flourishes using deep black iron gall ink on aged parchment. The capital letters feature intricate gold leaf gilding that catches the light.",
            "aesthetic_type": "Vintage Gothic",
            "color_tone": "Deep Black and Gold",
            "skill_level": "Advanced",
            "usage": "Historical Restorations & Fine Art"
        },
        {
            "image_name": "copperplate_wedding_invite.jpg",
            "hobby": "Calligraphy",
            "style": "Copperplate Script",
            "category": "Elegant Calligraphy",
            "description": "An elegant, flowing script written with a flexible pointed steel nib. The lettering features high contrast between fine hairline upstrokes and thick shaded downstrokes, executing delicate, sloped cursive on cream-colored handmade cardstock. Flourishes gracefully loop in symmetrical patterns around the text.",
            "aesthetic_type": "Elegant Classic",
            "color_tone": "Warm Monochrome & Cream",
            "skill_level": "Intermediate",
            "usage": "Wedding Invitations & Luxury Stationery"
        },
        {
            "image_name": "japanese_shodo_zen.jpg",
            "hobby": "Calligraphy",
            "style": "Shodo (Japanese Brush)",
            "category": "Eastern Calligraphy",
            "description": "A raw, spontaneous black sumi ink brush stroke depicting the ensō (Zen circle) on textured, fibrous white washi paper. The brush fibers are visible at the edges of the stroke, reflecting the energy, breath, and motion of the calligrapher in a single, focused gesture.",
            "aesthetic_type": "Zen Minimalist",
            "color_tone": "High-Contrast Black and Washi White",
            "skill_level": "Advanced",
            "usage": "Fine Art Prints & Meditation Decors"
        },
        {
            "image_name": "modern_brush_lettering.jpg",
            "hobby": "Calligraphy",
            "style": "Modern Brush Calligraphy",
            "category": "Modern Lettering",
            "description": "Playful and fluid hand lettering executed with flexible felt-tip brush pens. The script features a modern bounce lettering style with irregular baseline alignments and colorful gradient transitions, blending pastel pinks, purples, and blues into a cheerful, expressive greeting message.",
            "aesthetic_type": "Vibrant & Playful",
            "color_tone": "Pastel Rainbow & Neon Accents",
            "skill_level": "Beginner",
            "usage": "Greeting Cards & Social Media Graphics"
        },
        {
            "image_name": "faux_calligraphy_chalkboard.jpg",
            "hobby": "Calligraphy",
            "style": "Faux Calligraphy",
            "category": "Decorative Lettering",
            "description": "Hand-lettered quote drawn with white chalk ink pens on a rustic slate chalkboard. The downstrokes are manually thickened to simulate the thick-and-thin variations of a flexible nib. The text is surrounded by hand-drawn laurel wreaths, botanical twigs, and charming starburst details.",
            "aesthetic_type": "Rustic Cozy",
            "color_tone": "High-Contrast White on Slate Grey",
            "skill_level": "Beginner",
            "usage": "Café Signage & Home Décor"
        },
        {
            "image_name": "italic_hand_sonnet.jpg",
            "hobby": "Calligraphy",
            "style": "Italic Script",
            "category": "Classical Calligraphy",
            "description": "A clear, beautifully sloped Renaissance-style cursive written with a medium broad-edge metal nib. The writing displays the classic 5-degree slant, with crisp, elliptical letterforms executing a Shakespearean sonnet. The rich sepia ink flows smoothly over a textured ivory cotton sheet.",
            "aesthetic_type": "Renaissance Academic",
            "color_tone": "Sepia and Ivory Cream",
            "skill_level": "Intermediate",
            "usage": "Literary Portfolios & Historical Scrolls"
        },
        {
            "image_name": "uncial_celtic_monogram.jpg",
            "hobby": "Calligraphy",
            "style": "Uncial Script",
            "category": "Celtic Calligraphy",
            "description": "Rounded, majestic insular script inspired by historical 8th-century Irish monastic texts. The bold, wide letters are written in rich emerald green and bright crimson inks using a broad quill. Circular characters are prominent, and the margins feature intricate Celtic knotwork illustrations.",
            "aesthetic_type": "Celtic Mythical",
            "color_tone": "Emerald Green, Deep Crimson, and Gold",
            "skill_level": "Intermediate",
            "usage": "Monograms, Crests & Heritage Certificates"
        },
        {
            "image_name": "foundational_hand_scroll.jpg",
            "hobby": "Calligraphy",
            "style": "Foundational Hand",
            "category": "Broad-edge Calligraphy",
            "description": "Highly legible, circular, and clean script based on 10th-century English models. Executed with a steel broad-edge nib using rich indigo gouache on heavy hot-pressed paper. The letters exhibit generous, open counter spaces and robust, upright structure, perfect for formal academic citations.",
            "aesthetic_type": "Mid-Century Modern & Clean",
            "color_tone": "Indigo Blue and Stark White",
            "skill_level": "Beginner",
            "usage": "Formal Certificates, Diplomas & Declarations"
        },
        {
            "image_name": "illumination_initial_letter.jpg",
            "hobby": "Calligraphy",
            "style": "Illuminated Lettering",
            "category": "Medieval Art",
            "description": "A large, highly detailed historiated initial letter 'A' on a manuscript. The letter is surrounded by hand-drawn microscopic golden leaf filigree, deep lapis lazuli blue vine scrolls, and small crimson dragons climbing the shafts. The gold leaf glows brilliantly under a direct light beam.",
            "aesthetic_type": "Ornate Byzantine",
            "color_tone": "Royal Lapis Blue, Gold Foil, and Vermilion",
            "skill_level": "Advanced",
            "usage": "Historical Replicas & Premium Collectors Art"
        },
        {
            "image_name": "arabic_thuluth_panel.jpg",
            "hobby": "Calligraphy",
            "style": "Thuluth Script",
            "category": "Islamic Calligraphy",
            "description": "A monumental, sweeping panel of Arabic calligraphy hand-carved and painted on a dark wooden screen. The Thuluth script, known for its elegant curved vertical lines and interlacing letterforms, is rendered with absolute precision. The letters are highlighted in pale ochre, contrasting with deep walnut grain.",
            "aesthetic_type": "Majestic Sacred",
            "color_tone": "Ochre Yellow and Deep Walnut Brown",
            "skill_level": "Advanced",
            "usage": "Fine Wood Panels & Mosque Architecture"
        },
        {
            "image_name": "blackletter_graffiti_mural.jpg",
            "hobby": "Calligraphy",
            "style": "Calligraffiti",
            "category": "Urban Art",
            "description": "A massive urban mural blending aggressive, modernized Gothic blackletter calligraphic forms with vibrant street art. Bold black strokes are spray-painted over abstract splashes of neon yellow, cyan, and hot pink, featuring drips, splatters, and dynamic motion layers on a textured brick wall.",
            "aesthetic_type": "Gritty Contemporary",
            "color_tone": "Neon Yellow, Splash Cyan, and Asphalt Black",
            "skill_level": "Intermediate",
            "usage": "Streetwear Apparel Designs & Public Murals"
        },
        {
            "image_name": "spencerian_business_hand.jpg",
            "hobby": "Calligraphy",
            "style": "Spencerian Script",
            "category": "19th Century Cursive",
            "description": "Delicate, rapid cursive penmanship characterized by flowing lines, wide oval flourishes, and minimal shading. Written with an ultra-flexible gold fountain pen nib on ivory laid paper, the script forms elegant business correspondence of the late Victorian era, resembling wind-swept lace.",
            "aesthetic_type": "Vintage Americana",
            "color_tone": "Dark Walnut Brown on Ivory Cream",
            "skill_level": "Advanced",
            "usage": "Personal luxury correspondence & Custom Monograms"
        },
        # --- PHOTOGRAPHY STYLES ---
        {
            "image_name": "milky_way_long_exposure.jpg",
            "hobby": "Photography",
            "style": "Astrophotography",
            "category": "Night Landscape",
            "description": "A stunning 25-second long-exposure photograph capturing the bright galactic core of the Milky Way galaxy. The cosmic dust and colorful nebulae arch majestically over a silhouetted pine tree forest on a mountain peak. Pinpoint stars fill the clear, unpolluted night sky in deep detail.",
            "aesthetic_type": "Cosmic & Ethereal",
            "color_tone": "Deep Violet, Indigo Blue, and Starlight Silver",
            "skill_level": "Advanced",
            "usage": "Fine Art Gallery Prints & Astronomical Journals"
        },
        {
            "image_name": "macro_dew_dandelion.jpg",
            "hobby": "Photography",
            "style": "Macro Photography",
            "category": "Close-up Nature",
            "description": "An extreme close-up macro shot with a shallow depth of field, focusing on a single seed of a dandelion. A tiny water droplet clings to the seed's fine hairs, acting as a perfect spherical lens that refracts a miniature, inverted image of a field of wildflowers behind it in the morning light.",
            "aesthetic_type": "Organic Detail",
            "color_tone": "Soft Emerald Green and Dewdrop Silver",
            "skill_level": "Intermediate",
            "usage": "Nature Books, Wall Art & Scientific Exhibits"
        },
        {
            "image_name": "street_rain_tokyo.jpg",
            "hobby": "Photography",
            "style": "Street Photography",
            "category": "Candid Urban",
            "description": "A candid night shot on a wet street in Tokyo. A lone pedestrian holding a transparent vinyl umbrella walks past bright, neon-lit restaurant signs. The colorful pink, blue, and yellow neon lights reflect beautifully in the puddles on the wet asphalt, creating a cinematic, futuristic atmosphere.",
            "aesthetic_type": "Cyberpunk Noir",
            "color_tone": "Neon Magenta, Cyan Blue, and Asphalt Grey",
            "skill_level": "Intermediate",
            "usage": "Editorial Portfolios & Cyberpunk Artwork"
        },
        {
            "image_name": "landscape_golden_gate.jpg",
            "hobby": "Photography",
            "style": "Landscape Photography",
            "category": "Scenic Vista",
            "description": "A wide-angle scenic vista of the Golden Gate Bridge during sunrise. A thick, rolling bank of morning marine fog flows underneath the bridge, partially obscuring the water, while the tall orange towers pierce through the fog. The first rays of warm golden sunlight illuminate the bridge's cables.",
            "aesthetic_type": "Dreamy & Atmospheric",
            "color_tone": "Golden Hour Orange and Ocean Mist Grey",
            "skill_level": "Beginner",
            "usage": "Tourism Campaigns, Travel Guides & Calendars"
        },
        {
            "image_name": "portrait_wrinkles_elderly.jpg",
            "hobby": "Photography",
            "style": "Portrait Photography",
            "category": "Human Character",
            "description": "A highly detailed, tight close-up black and white portrait of an elderly carpenter in his workshop. The harsh side-lighting accentuates the deep wrinkles, weathered skin, and expressive eyes of the subject. Wood shavings and fine dust are visible in his beard, conveying a life of dedicated craft.",
            "aesthetic_type": "Authentic Realism",
            "color_tone": "High-Contrast Black & White",
            "skill_level": "Intermediate",
            "usage": "Humanity Documentary Exhibits & Editorial Features"
        },
        {
            "image_name": "wildlife_cheetah_chase.jpg",
            "hobby": "Photography",
            "style": "Wildlife Photography",
            "category": "Action Capture",
            "description": "An action-filled wildlife shot captured at a fast shutter speed of 1/2000s, freezing a cheetah in full sprint. The cheetah is suspended in mid-air, all four paws off the ground, eyes locked on target, with the golden grasses of the Serengeti savanna rendered into a soft, dynamic motion blur behind it.",
            "aesthetic_type": "High-Octane Action",
            "color_tone": "Golden Savannah Yellow and Dust Brown",
            "skill_level": "Advanced",
            "usage": "Nature Publications & Educational Documentaries"
        },
        {
            "image_name": "architectural_minimalist_stairs.jpg",
            "hobby": "Photography",
            "style": "Architectural Photography",
            "category": "Minimalist Structure",
            "description": "A top-down abstract photograph looking down a spiral concrete staircase. The steps form a perfect mathematical Fibonacci spiral that draws the eye toward the dark center. Subtle variations in concrete texture and sharp geometric shadows create a strong, clean graphic layout.",
            "aesthetic_type": "Geometric Abstraction",
            "color_tone": "Monochromatic Concrete Grey and Dark Charcoal",
            "skill_level": "Intermediate",
            "usage": "Architecture Portfolios & Interior Design Magazines"
        },
        {
            "image_name": "sports_basketball_dunk.jpg",
            "hobby": "Photography",
            "style": "Sports Photography",
            "category": "Action Sports",
            "description": "A low-angle, wide-angle shot capturing a basketball player rising above the rim for a powerful slam dunk. Captured with flash in a dark indoor arena, highlighting the player's tense muscles, droplets of sweat flying, and the dramatic, roaring, out-of-focus crowd in the background.",
            "aesthetic_type": "Dramatic Kinetic",
            "color_tone": "High-Saturation Arena Orange and Deep Shadow",
            "skill_level": "Intermediate",
            "usage": "Sports Marketing, Magazines & Athletic Branding"
        },
        {
            "image_name": "food_steaming_ramen.jpg",
            "hobby": "Photography",
            "style": "Food Photography",
            "category": "Culinary Art",
            "description": "A close-up, top-down styled food photograph of a steaming bowl of traditional Tonkotsu ramen. The shot showcases a perfect glistening soft-boiled egg cut in half, tender pork belly slices, bright green scallions, and delicate bamboo shoots, with wisps of rising hot steam catching a soft side light.",
            "aesthetic_type": "Warm & Savory",
            "color_tone": "Warm Umber Brown, Soy Amber, and Vibrant Green",
            "skill_level": "Beginner",
            "usage": "Restaurant Menu Design & Culinary Blogs"
        },
        {
            "image_name": "long_exposure_waterfall.jpg",
            "hobby": "Photography",
            "style": "Long-Exposure Landscape",
            "category": "Scenic Nature",
            "description": "A long-exposure landscape photo of a hidden waterfall cascading down a narrow basalt canyon. A 2.0-second shutter speed turns the falling water into a smooth, silky white ribbon, contrasting with the dark, wet volcanic rock walls and the brilliant, vibrant green moss coating the stream banks.",
            "aesthetic_type": "Serene & Calming",
            "color_tone": "Lush Forest Moss Green and Silk White",
            "skill_level": "Intermediate",
            "usage": "Spa/Wellness Wall Art & Environmental Calendars"
        },
        {
            "image_name": "fashion_neon_cyberpunk.jpg",
            "hobby": "Photography",
            "style": "Fashion Photography",
            "category": "Avant-Garde",
            "description": "An avant-garde fashion photograph set in a narrow brick alleyway. The model, wearing structured, metallic silver clothing that highly reflects light, is illuminated solely by the intense purple and blue neon tubes of a nearby storefront. Shadows are deep, and smoke adds an atmospheric haze.",
            "aesthetic_type": "Cyberpunk Neon & Futuristic",
            "color_tone": "Electric Violet, Neon Cyan, and Reflective Chrome",
            "skill_level": "Advanced",
            "usage": "High-Fashion Editorials & Conceptual Art"
        },
        {
            "image_name": "aerial_ocean_reef.jpg",
            "hobby": "Photography",
            "style": "Drone/Aerial Photography",
            "category": "Earth Views",
            "description": "A birds-eye-view aerial drone photograph looking straight down at an ocean coastline. Crystal-clear turquoise water waves break onto a vibrant coral reef, forming patterns of white sea foam. The sandy beach is a soft cream, with the shadows of tall palm trees projecting onto the sand.",
            "aesthetic_type": "Tropical Vibrance & Aerial Vista",
            "color_tone": "Turquoise Teal, Deep Azure Blue, and Coral Pink",
            "skill_level": "Beginner",
            "usage": "Travel Agencies, Beach Resort Portfolios & Wallpaper"
        },
        {
            "image_name": "macro_peacock_feather.jpg",
            "hobby": "Photography",
            "style": "Macro Photography",
            "category": "Abstract Pattern",
            "description": "An extreme close-up macro photograph showing the microscopic structure of a peacock feather. The focus is razor-sharp on the individual iridescent barbules, catching the light to display rich shimmering shades of electric blue, emerald green, and deep gold in a perfect repeating pattern.",
            "aesthetic_type": "Vibrant Iridescent & Abstract",
            "color_tone": "Electric Peacock Blue, Emerald Green, and Radiant Gold",
            "skill_level": "Intermediate",
            "usage": "Abstract Art Prints, Tech Wallpapers & Textiles"
        }
    ]
    
    # Ensure directory exists
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(CSV_PATH, index=False)
    print(f"[Dataset] Generated custom hobby dataset with {len(df)} records at: {CSV_PATH}")
    return df

def load_dataset():
    """
    Loads the CSV dataset. If it doesn't exist, it generates the default dataset first.
    Returns:
        pd.DataFrame: The loaded dataset.
    """
    if not os.path.exists(CSV_PATH):
        return generate_default_dataset()
    
    try:
        df = pd.read_csv(CSV_PATH)
        # Validate columns
        required_cols = [
            "image_name", "hobby", "style", "category", 
            "description", "aesthetic_type", "color_tone", 
            "skill_level", "usage"
        ]
        for col in required_cols:
            if col not in df.columns:
                print(f"[Dataset WARNING] Missing column '{col}' in CSV. Re-generating...")
                return generate_default_dataset()
        
        return df
    except Exception as e:
        print(f"[Dataset ERROR] Failed to load dataset: {e}. Re-generating default dataset...")
        return generate_default_dataset()

def add_custom_entry(entry_dict):
    """
    Appends a new record to the CSV file.
    Args:
        entry_dict (dict): A dictionary representing the new row.
    """
    df = load_dataset()
    new_df = pd.concat([df, pd.DataFrame([entry_dict])], ignore_index=True)
    new_df.to_csv(CSV_PATH, index=False)
    print(f"[Dataset] Added custom entry: '{entry_dict.get('style')}' to {CSV_PATH}")
    return new_df

def create_documents(df):
    """
    Converts a pandas DataFrame into a structured document representation for embeddings,
    along with a neat metadata dictionary for database filtering.
    Args:
        df (pd.DataFrame): The input dataframe.
    Returns:
        list of dict: List of documents containing 'id', 'text', and 'metadata'.
    """
    documents = []
    for idx, row in df.iterrows():
        doc_id = f"doc_{idx}"
        
        # Build a highly structured visual and contextual text block to embed.
        # This formatting maximizes RAG semantic retrieval accuracy.
        text_representation = (
            f"Hobby Area: {row['hobby']}\n"
            f"Aesthetic Style: {row['style']} ({row['category']})\n"
            f"Visual Description: {row['description']}\n"
            f"Aesthetic Type: {row['aesthetic_type']}\n"
            f"Color Tone Palette: {row['color_tone']}\n"
            f"Difficulty Skill Level: {row['skill_level']}\n"
            f"Typical Usage: {row['usage']}"
        )
        
        metadata = {
            "image_name": str(row["image_name"]),
            "hobby": str(row["hobby"]),
            "style": str(row["style"]),
            "category": str(row["category"]),
            "aesthetic_type": str(row["aesthetic_type"]),
            "color_tone": str(row["color_tone"]),
            "skill_level": str(row["skill_level"]),
            "usage": str(row["usage"])
        }
        
        documents.append({
            "id": doc_id,
            "text": text_representation,
            "metadata": metadata
        })
    return documents

if __name__ == "__main__":
    # Self-test code
    print("[Dataset Loader] Performing diagnostics...")
    test_df = load_dataset()
    docs = create_documents(test_df)
    print(f"[Dataset Loader] Loaded {len(test_df)} records.")
    print(f"[Dataset Loader] Generated {len(docs)} document representations.")
    print("[Dataset Loader] Sample Document:")
    print("-" * 50)
    print(docs[0]["text"])
    print("-" * 50)
    print("Metadata:", docs[0]["metadata"])
