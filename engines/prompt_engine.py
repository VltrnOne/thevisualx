class PromptEngine:
    def __init__(self):
        pass

    def generate_visual_description(self, song_title, genre, bpm, mood_tags):
        """
        Constructs a high-fidelity image prompt based on audio characteristics.
        In a real scenario, this could call an LLM to get creative.
        """
        
        base_quality = "Cinematic, 8k resolution, photorealistic, anamorphic lens, highly detailed texture, dramatic lighting, depth of field, Kodak Portra 400, movie still"
        
        mood_map = {
            "aggressive": "cyberpunk street, neon rain, dark alley, wet pavement, intense contrast",
            "chill": "sunset over ocean, golden hour, calm waves, soft focus, ethereal",
            "upbeat": "vibrant abstract colors, fast motion blur, geometric shapes, bright studio lighting",
            "dark": "gothic cathedral, fog, monochrome, mysterious shadows, noir style"
        }
        
        # Basic logic to pick a mood based on genre/tags (expandable)
        selected_mood = mood_map.get("aggressive", "abstract cinematic background") # Default
        if "lofi" in genre.lower():
            selected_mood = mood_map["chill"]
        elif "techno" in genre.lower() or "metal" in genre.lower():
            selected_mood = mood_map["aggressive"]
            
        final_prompt = f"{selected_mood}, visual representation of {genre} music, {song_title}. {base_quality}"
        return final_prompt

    def generate_motion_prompt(self, bpm):
        """
        Determines how the video should move based on tempo.
        """
        if bpm > 120:
            return "Fast camera movement, zoom in, intense action, rapid changes"
        else:
            return "Slow pan, smooth camera motion, floating, subtle movement"
