"""
The Creative Council - Multi-Agent Prompt Engineering System
Powered by VLTRN

A team of AI creative professionals that confer to generate unique,
cinema-quality prompts for every video. Never the same result twice.
"""

import os
import random
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class CreativeCouncil:
    """
    The Creative Council - A multi-agent system for generating cinematic prompts.

    Each session generates UNIQUE creative output by:
    - Randomizing visual elements, settings, and styles
    - Using song metadata as creative seeds
    - Integrating VISUALX brain modules when available
    - Supporting LLM-powered generation for maximum creativity
    """

    def __init__(self, engine="rules"):
        """
        Initialize the Creative Council.

        Args:
            engine: 'rules', 'llm' (auto), 'claude', or 'openai'
        """
        self.engine = engine
        self.agents = {
            "strategist": "Marketing & Culture Lead",
            "storyteller": "Lead Narrative Designer",
            "cinematographer": "Director of Photography (ASC)",
            "motion_designer": "Motion Designer",
            "director": "Executive Producer/Director",
            "narrator": "Project Narrator (Continuity Editor)",
            "colorist": "Senior Colorist (DI)",
            "vfx_supervisor": "VFX Supervisor"
        }

        # Creative element libraries for dynamic generation
        self._init_creative_libraries()

        # LLM Configuration
        self.llm_client = None
        self.llm_model = None
        self.llm_provider = None

        if engine in ["llm", "claude", "openai"]:
            self._init_llm(provider=engine if engine != "llm" else None)

    def _init_creative_libraries(self):
        """Initialize libraries of creative elements for variation."""

        self.settings = {
            "urban": [
                "rain-soaked Tokyo alleyway with holographic advertisements",
                "abandoned Detroit factory overtaken by bioluminescent plants",
                "Miami penthouse overlooking neon-lit Art Deco district",
                "underground Brooklyn subway station at 3AM",
                "rooftop helipad in Dubai with city lights below",
                "graffiti-covered Paris metro tunnel",
                "Shanghai skybridge between glass towers",
                "LA river channel under purple twilight",
                "Chicago elevated train platform in snow",
                "London warehouse rave with laser grids"
            ],
            "nature": [
                "bioluminescent forest with floating spores",
                "volcanic beach with black sand and crimson waves",
                "frozen waterfall in an ice cave",
                "desert oasis under a double sunset",
                "bamboo forest in dense morning fog",
                "northern lights over a mirror-still fjord",
                "cherry blossom storm in slow motion",
                "underwater kelp forest with light rays",
                "canyon at golden hour with dust particles",
                "ancient redwood forest with shafts of light"
            ],
            "surreal": [
                "infinite mirror maze reflecting alternate realities",
                "floating islands connected by light bridges",
                "clockwork cathedral with moving gears",
                "liquid mercury ocean under twin moons",
                "inverted city hanging from clouds",
                "crystal cave pulsing with inner light",
                "geometric void with impossible architecture",
                "garden where flowers are made of flame",
                "library with books that fly like birds",
                "staircase spiraling into fractal infinity"
            ],
            "luxury": [
                "private jet cabin at 40,000 feet during aurora",
                "Monaco yacht deck during fireworks",
                "Venetian masquerade ball in golden hall",
                "Japanese zen garden in minimalist mansion",
                "vintage Hollywood premiere with flashbulbs",
                "Swiss chalet overlooking alpine peaks",
                "Moroccan palace courtyard at dusk",
                "Manhattan penthouse gallery opening",
                "Santorini villa terrace at sunset",
                "Beverly Hills infinity pool at midnight"
            ],
            "abstract": [
                "void filled with floating geometric shapes",
                "paint explosion frozen in time",
                "sound waves visualized as light ribbons",
                "digital glitch reality fragmenting",
                "smoke and ink swirling in water",
                "prismatic light refracting through crystals",
                "neural network visualization pulsing",
                "quantum field with particle cascades",
                "emotional aura manifesting as color",
                "time dilation effect with motion trails"
            ]
        }

        self.subjects = {
            "cinematic": [
                "a mysterious figure in flowing dark robes",
                "twin dancers moving in perfect sync",
                "a lone traveler with glowing artifacts",
                "ethereal beings made of light and shadow",
                "a masked protagonist with chromatic armor",
                "silhouettes merging and separating",
                "hands reaching through dimensional tears",
                "a metamorphosing humanoid form",
                "spirits emerging from ancient symbols",
                "a figure dissolving into particles"
            ],
            "performance": [
                "the artist commanding the space with magnetic presence",
                "intense close-up capturing raw emotion",
                "artist in motion, clothing flowing dramatically",
                "powerful stance with dramatic backlighting",
                "artist emerging from shadows into spotlight",
                "multiple exposure of artist in motion",
                "artist reflected in shattered mirrors",
                "dramatic profile shot with rim lighting",
                "artist surrounded by symbolic elements",
                "overhead shot of artist reaching upward"
            ]
        }

        self.lighting_moods = [
            "neon-drenched with cyan and magenta",
            "golden hour warmth with long shadows",
            "harsh chiaroscuro with deep blacks",
            "ethereal diffused glow",
            "strobe-frozen moments in darkness",
            "bioluminescent ambient glow",
            "theatrical spotlight isolation",
            "sunset gradient from amber to purple",
            "cold blue moonlight with warm practicals",
            "RGB LED wash with color mixing"
        ]

        self.camera_styles = [
            "Shot on ARRI Alexa 65, Panavision Ultra Vista anamorphic",
            "Shot on RED Monstro 8K VV, Cooke S7/i primes",
            "Shot on Sony Venice 2, Zeiss Supreme primes",
            "Shot on Blackmagic URSA 12K, vintage Canon K35s",
            "Shot on ARRI ALEXA Mini LF, Master Anamorphic"
        ]

        self.visual_effects = [
            "with particle systems and volumetric fog",
            "with lens flares and chromatic aberration",
            "with speed ramping and motion blur",
            "with floating debris and dust motes",
            "with holographic overlays and glitch effects",
            "with reflection mapping and caustics",
            "with atmospheric haze and god rays",
            "with liquid simulations and ripples",
            "with fire and ember particles",
            "with electrical arcs and plasma"
        ]

        self.color_palettes = [
            ("teal and orange", "complementary blockbuster grade"),
            ("deep purple and gold", "royal luxury aesthetic"),
            ("desaturated with single color pop", "editorial fashion"),
            ("neon pink and electric blue", "cyberpunk aesthetic"),
            ("warm amber and cool shadow", "cinematic drama"),
            ("monochrome with subtle tint", "noir atmosphere"),
            ("pastel gradients", "dream-like softness"),
            ("high contrast black and white", "graphic impact"),
            ("earth tones with emerald accent", "organic luxury"),
            ("crimson and silver", "bold aggression")
        ]

    def _generate_seed(self, song_title, genre, bpm):
        """Generate a unique seed - different every single time."""
        # Use microseconds + random for guaranteed uniqueness
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        random_factor = random.randint(0, 999999)
        seed_string = f"{song_title}{genre}{bpm}{timestamp}{random_factor}"
        seed = int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        return seed

    def _init_llm(self, provider=None):
        """Initialize LLM client (Claude or GPT-4o)."""
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        use_anthropic = (provider == "claude") or (not provider and anthropic_key)
        use_openai = (provider == "openai") or (not provider and openai_key and not use_anthropic)

        if use_anthropic and anthropic_key:
            try:
                import anthropic
                self.llm_client = anthropic.Anthropic(api_key=anthropic_key)
                self.llm_model = "claude-sonnet-4-20250514"
                self.llm_provider = "anthropic"
                print("[Council] LLM Engine: Claude Sonnet 4 (Anthropic)")
            except ImportError:
                print("[Council] Warning: anthropic package not installed")

        elif use_openai and openai_key:
            try:
                import openai
                self.llm_client = openai.OpenAI(api_key=openai_key)
                self.llm_model = "gpt-4o"
                self.llm_provider = "openai"
                print("[Council] LLM Engine: GPT-4o (OpenAI)")
            except ImportError:
                print("[Council] Warning: openai package not installed")

        else:
            print(f"[Council] No LLM available, using enhanced rules engine")
            self.engine = "rules"

    def _call_llm(self, system_prompt, user_prompt):
        """Call the LLM with the given prompts."""
        if not self.llm_client:
            return None

        try:
            if self.llm_provider == "anthropic":
                response = self.llm_client.messages.create(
                    model=self.llm_model,
                    max_tokens=600,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return response.content[0].text

            elif self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.llm_model,
                    max_tokens=600,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.choices[0].message.content

        except Exception as e:
            print(f"[Council] LLM Error: {e}")
            return None

    def convene_council(self, song_title, genre, bpm, analysis_data, mode="cinematic",
                        artist_description=None, project_context=None):
        """
        Convene the creative council to generate unique prompts.

        Args:
            song_title: Title of the track
            genre: Music genre
            bpm: Beats per minute
            analysis_data: Additional audio analysis data
            mode: 'cinematic' or 'performance'
            artist_description: Description of the artist (for performance mode)
            project_context: Overall project context for narrative continuity

        Returns:
            Tuple of (final_image_prompt, motion_prompt)
        """
        print(f"\n{'='*60}")
        print(f"[CREATIVE COUNCIL] Convening for '{song_title}'")
        print(f"[CREATIVE COUNCIL] Genre: {genre} | BPM: {bpm} | Mode: {mode.upper()}")
        print(f"[CREATIVE COUNCIL] Engine: {self.engine.upper()}")
        print(f"{'='*60}")

        # Generate unique seed for this session
        seed = self._generate_seed(song_title, genre, bpm)
        print(f"[Council] Creative seed: {seed}")

        if self.engine in ["llm", "claude", "openai"]:
            return self._convene_council_llm(song_title, genre, bpm, analysis_data, mode,
                                            artist_description, project_context)
        else:
            return self._convene_council_rules(song_title, genre, bpm, analysis_data, mode,
                                               artist_description, project_context)

    def _convene_council_llm(self, song_title, genre, bpm, analysis_data, mode,
                             artist_description, project_context):
        """LLM-powered council generation - maximum creativity."""

        context = f"""
Song Title: "{song_title}"
Genre: {genre}
BPM: {bpm}
Mode: {mode}
Artist Description: {artist_description or "Create a compelling mysterious figure"}
Previous Clips Context: {project_context or "This is the first clip - establish a unique visual world"}
"""

        # Agent 1: Cultural Strategist
        strategist_system = """You are a cutting-edge Cultural Strategist for premium music videos.
Analyze the song and determine:
- The emotional journey this clip should evoke
- A UNIQUE aesthetic direction (be specific and original - avoid clichés)
- One unexpected visual metaphor that captures the song's essence

Be bold and specific. No generic descriptions. 2-3 sentences."""

        strategy = self._call_llm(strategist_system, f"Create a unique strategy for:\n{context}")
        if not strategy:
            strategy = self._consult_strategist_dynamic(genre, bpm, song_title)
        print(f"\n[Agent: {self.agents['strategist']}]\n  → {strategy}")

        # Agent 2: Narrative Designer
        storyteller_system = f"""You are an award-winning Narrative Designer for music videos.
Based on the strategy, create a VIVID, SPECIFIC micro-scene for a 5-second clip.
{"Focus on artist performance - their presence, attitude, movement, wardrobe." if mode == "performance" else "Create an atmospheric, surreal visual world - abstract or narrative."}

Requirements:
- Be extremely specific (colors, textures, materials, lighting)
- Include one UNEXPECTED visual element that surprises
- Make it DIFFERENT from typical music videos
- 2-3 sentences describing exactly what we see."""

        story = self._call_llm(storyteller_system, f"Strategy: {strategy}\n\n{context}")
        if not story:
            story = self._consult_storyteller_dynamic(strategy, song_title, mode, genre, bpm)
        print(f"\n[Agent: {self.agents['storyteller']}]\n  → {story}")

        # Agent 3: Director of Photography
        dp_system = """You are a legendary Director of Photography (ASC member).
Add technical specifications that enhance the scene's mood:
- Specific camera and lens (be exact)
- Lighting setup and quality
- Color temperature and contrast approach
- One signature visual technique

1-2 sentences. Start with "Shot on..."."""

        visuals = self._call_llm(dp_system, f"Scene: {story}\nGenre: {genre}\nMood: {strategy}")
        if not visuals:
            visuals = self._consult_cinematographer_dynamic(story, genre, mode, bpm)
        print(f"\n[Agent: {self.agents['cinematographer']}]\n  → {visuals}")

        # Agent 4: Colorist
        colorist_system = """You are a Senior Digital Colorist.
Define the color grade for this scene:
- Primary color palette (be specific - not just "warm" or "cool")
- Contrast approach
- Any special color treatments

1 sentence with specific colors and techniques."""

        color_grade = self._call_llm(colorist_system, f"Scene: {story}\nMood: {strategy}")
        if not color_grade:
            color_grade = self._consult_colorist_dynamic(strategy, genre)
        print(f"\n[Agent: {self.agents['colorist']}]\n  → {color_grade}")

        # Agent 5: Motion Designer
        motion_system = """You are a Motion Designer for premium music videos.
Based on BPM and mood, specify exact camera movement for 5 seconds:
- Movement type and direction
- Speed relative to beat
- Any special motion techniques

1 sentence, very specific."""

        motion = self._call_llm(motion_system, f"BPM: {bpm}\nScene: {story}\nMood: {strategy}")
        if not motion:
            motion = self._consult_motion_designer_dynamic(bpm, strategy, mode)
        print(f"\n[Agent: {self.agents['motion_designer']}]\n  → {motion}")

        # Agent 6: Director (Final Synthesis)
        director_system = """You are the Executive Director delivering the final image prompt.
Combine ALL elements into ONE cohesive, detailed prompt for AI image generation.
Include: subject, setting, lighting, camera specs, color grade, mood.

Output ONLY the final prompt. No explanations. Make it vivid and specific.
End with quality tags: "cinematic, 8k, photorealistic, award-winning cinematography"."""

        final_prompt = self._call_llm(director_system,
            f"Scene: {story}\nTechnical: {visuals}\nColor: {color_grade}\nMood: {strategy}")
        if not final_prompt:
            final_prompt = self._director_synthesis_dynamic(strategy, story, visuals, color_grade)

        print(f"\n[Agent: {self.agents['director']}] FINAL PROMPT:")
        print(f"  → {final_prompt}")
        print(f"\n[MOTION DIRECTIVE]:\n  → {motion}")

        return final_prompt, motion

    def _convene_council_rules(self, song_title, genre, bpm, analysis_data, mode,
                                artist_description, project_context):
        """Enhanced rule-based generation with randomization for unique output."""

        # 1. The Strategist - Dynamic analysis
        strategy = self._consult_strategist_dynamic(genre, bpm, song_title)
        print(f"\n[Agent: {self.agents['strategist']}]\n  → {strategy}")

        # 2. The Narrator - Continuity check
        narrative_guidance = self._consult_narrator_dynamic(project_context, strategy, mode)
        if narrative_guidance:
            print(f"\n[Agent: {self.agents['narrator']}]\n  → {narrative_guidance}")

        # 3. The Storyteller - Scene creation
        story = self._consult_storyteller_dynamic(strategy, song_title, mode, genre, bpm,
                                                   narrative_guidance, artist_description)
        print(f"\n[Agent: {self.agents['storyteller']}]\n  → {story}")

        # 4. The Cinematographer - Technical specs
        visuals = self._consult_cinematographer_dynamic(story, genre, mode, bpm)
        print(f"\n[Agent: {self.agents['cinematographer']}]\n  → {visuals}")

        # 5. The Colorist - Color grade
        color_grade = self._consult_colorist_dynamic(strategy, genre)
        print(f"\n[Agent: {self.agents['colorist']}]\n  → {color_grade}")

        # 6. The Motion Designer - Camera movement
        motion = self._consult_motion_designer_dynamic(bpm, strategy, mode)
        print(f"\n[Agent: {self.agents['motion_designer']}]\n  → {motion}")

        # 7. The Director - Final synthesis
        final_prompt = self._director_synthesis_dynamic(strategy, story, visuals, color_grade)
        print(f"\n[Agent: {self.agents['director']}] FINAL PROMPT:")
        print(f"  → {final_prompt}")
        print(f"\n[MOTION DIRECTIVE]:\n  → {motion}")

        return final_prompt, motion

    # ==================== DYNAMIC RULE-BASED AGENTS ====================

    def _consult_strategist_dynamic(self, genre, bpm, song_title):
        """Dynamic strategist that creates unique direction each time."""

        # Analyze genre for base direction
        genre_lower = genre.lower()

        emotions = {
            "high_energy": ["adrenaline", "euphoria", "power", "transcendence", "intensity"],
            "chill": ["nostalgia", "comfort", "intimacy", "reflection", "peace"],
            "dark": ["mystery", "tension", "danger", "seduction", "rebellion"],
            "uplifting": ["hope", "joy", "freedom", "triumph", "wonder"]
        }

        aesthetics = {
            "high_energy": ["cyber-industrial", "neon-punk", "rave-futurism", "chrome-minimalist", "digital-chaos"],
            "chill": ["analog-warmth", "vintage-film", "soft-focus-dream", "golden-hour", "intimate-noir"],
            "dark": ["shadow-play", "gothic-luxury", "neo-noir", "industrial-decay", "velvet-darkness"],
            "uplifting": ["ethereal-light", "cosmic-wonder", "nature-majesty", "crystalline-purity", "aurora-dreams"]
        }

        # Determine energy level from BPM and genre
        if bpm > 130 or any(g in genre_lower for g in ["techno", "house", "drum", "dubstep", "edm"]):
            energy = "high_energy"
        elif bpm < 80 or any(g in genre_lower for g in ["lofi", "ambient", "jazz", "soul", "ballad"]):
            energy = "chill"
        elif any(g in genre_lower for g in ["trap", "dark", "industrial", "metal", "goth"]):
            energy = "dark"
        else:
            energy = random.choice(["high_energy", "chill", "dark", "uplifting"])

        emotion = random.choice(emotions[energy])
        aesthetic = random.choice(aesthetics[energy])

        # Create unique strategy
        title_words = song_title.lower().split()
        if any(word in ["night", "dark", "shadow", "midnight"] for word in title_words):
            time_context = "nocturnal, shadow-drenched"
        elif any(word in ["sun", "light", "day", "bright", "gold"] for word in title_words):
            time_context = "luminous, radiant"
        elif any(word in ["dream", "sleep", "cloud", "float"] for word in title_words):
            time_context = "dreamlike, ethereal"
        else:
            time_context = random.choice(["twilight-liminal", "timeless-void", "dawn-emergence", "golden-suspended"])

        return f"Core emotion: {emotion}. Aesthetic: {aesthetic}, {time_context}. This clip must feel like nothing the viewer has seen before."

    def _consult_narrator_dynamic(self, project_context, strategy, mode):
        """Provides narrative guidance for continuity."""
        if not project_context:
            return "Establish a bold visual signature. Create intrigue from the first frame."

        progressions = [
            "Build on the previous energy - escalate the visual intensity",
            "Create contrast - shift the visual tone while maintaining thematic connection",
            "Reveal a new layer - introduce an unexpected element that recontextualizes what came before",
            "Deepen the world - explore a different angle of the established aesthetic"
        ]
        return random.choice(progressions)

    def _consult_storyteller_dynamic(self, strategy, song_title, mode, genre, bpm,
                                      narrative_guidance="", artist_description=None):
        """Creates unique micro-scenes with randomized elements."""

        # Determine setting category based on strategy
        if "cyber" in strategy.lower() or "digital" in strategy.lower() or "neon" in strategy.lower():
            setting_category = "urban"
        elif "nature" in strategy.lower() or "organic" in strategy.lower():
            setting_category = "nature"
        elif "luxury" in strategy.lower() or "golden" in strategy.lower():
            setting_category = "luxury"
        elif "dream" in strategy.lower() or "ethereal" in strategy.lower():
            setting_category = "surreal"
        else:
            setting_category = random.choice(list(self.settings.keys()))

        setting = random.choice(self.settings[setting_category])
        subject = random.choice(self.subjects[mode])
        vfx = random.choice(self.visual_effects)

        # Build the scene description
        if mode == "performance":
            if artist_description:
                subject = f"{artist_description}, {subject.split(',', 1)[-1] if ',' in subject else ''}"
            scene = f"{subject} in {setting}. {vfx.capitalize()}. Raw energy captured in a single powerful moment."
        else:
            scene = f"{subject} within {setting}. {vfx.capitalize()}. A frame that demands to be paused and studied."

        return scene

    def _consult_cinematographer_dynamic(self, story, genre, mode, bpm):
        """Dynamic technical specifications."""

        camera = random.choice(self.camera_styles)
        lighting = random.choice(self.lighting_moods)

        # Adjust based on energy
        if bpm > 120:
            technique = "fast shutter (45°) for staccato motion, handheld energy"
        elif bpm < 90:
            technique = "slow motion at 120fps, dreamy 180° shutter"
        else:
            technique = "smooth steadicam, cinematic 172.8° shutter"

        if mode == "performance":
            focus = "shallow depth of field f/1.4, focus on eyes and expression"
        else:
            focus = "deep focus with selective rack, environmental storytelling"

        return f"{camera}. {lighting}. {technique}. {focus}."

    def _consult_colorist_dynamic(self, strategy, genre):
        """Dynamic color grading decisions."""

        palette, description = random.choice(self.color_palettes)

        # Adjust based on strategy keywords
        if "dark" in strategy.lower() or "shadow" in strategy.lower():
            contrast = "crushed blacks, lifted shadows for detail"
        elif "dream" in strategy.lower() or "ethereal" in strategy.lower():
            contrast = "lifted blacks, soft rolloff, halation glow"
        else:
            contrast = "punchy midtones, controlled highlights"

        return f"{palette} palette, {description}. {contrast}."

    def _consult_motion_designer_dynamic(self, bpm, strategy, mode):
        """Dynamic camera movement based on BPM and mood."""

        if bpm > 140:
            movements = [
                "Rapid whip pan left to right on beat, camera shake on drops",
                "Aggressive push-in synchronized to kick drum, strobe timing",
                "360° rotation around subject at 2 seconds per revolution",
                "Dolly zoom (Vertigo effect) on impact moments"
            ]
        elif bpm > 110:
            movements = [
                "Smooth arc around subject, 90° over 5 seconds",
                "Slow push-in building tension, accelerating on beat",
                "Tracking shot parallel to movement, slight dutch angle",
                "Crane rise revealing environment, settling on subject"
            ]
        elif bpm > 80:
            movements = [
                "Gentle floating camera, subtle drift left",
                "Slow zoom out revealing context, contemplative pace",
                "Handheld with stabilization, breathing camera",
                "Circular tracking shot, hypnotic rhythm"
            ]
        else:
            movements = [
                "Near-static frame with subtle drift, meditative stillness",
                "Ultra-slow crane descent, 10 seconds of descent",
                "Imperceptible push-in, building intimacy",
                "Time-lapse movement, world moves around still subject"
            ]

        return random.choice(movements)

    def _director_synthesis_dynamic(self, strategy, story, visuals, color_grade):
        """Synthesize all elements into final prompt."""

        # Clean up and combine
        final = f"{story} {visuals} {color_grade}"

        # Add quality tags
        quality_tags = "cinematic composition, 8k resolution, photorealistic, award-winning cinematography, masterful lighting"

        return f"{final} {quality_tags} --v 6.0 --style raw"


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("CREATIVE COUNCIL - Uniqueness Test")
    print("=" * 60)

    council = CreativeCouncil(engine="rules")

    # Generate 3 prompts for the same song to show variation
    for i in range(3):
        print(f"\n\n{'='*60}")
        print(f"GENERATION {i+1}")
        print(f"{'='*60}")
        prompt, motion = council.convene_council(
            song_title="Midnight Drive",
            genre="Hip Hop",
            bpm=95,
            analysis_data=[],
            mode="cinematic"
        )
        print(f"\n[RESULT {i+1}]: {prompt[:200]}...")
