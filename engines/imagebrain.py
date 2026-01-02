"""
ImageBrain - AI Still Image Generator
Powered by VLTRN / VISUALX

Multi-agent architecture for AI image generation:
- Demo Scout: Audience research and demographic analysis
- Vision Pro: Visual style analysis and recommendations
- Style Sage: Style refinement and consistency
- Prompt Oracle: Final prompt generation and optimization
"""

import os
import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


# ============================================================
# Enums and Types
# ============================================================

class ImageStyle(Enum):
    """Visual style categories."""
    CINEMATIC = "cinematic"
    PHOTOREALISTIC = "photorealistic"
    ARTISTIC = "artistic"
    ANIME = "anime"
    ILLUSTRATION = "illustration"
    VINTAGE = "vintage"
    NEON = "neon"
    MINIMALIST = "minimalist"
    SURREAL = "surreal"
    DARK_MOODY = "dark_moody"
    BRIGHT_VIBRANT = "bright_vibrant"
    ETHEREAL = "ethereal"


class AspectRatio(Enum):
    """Standard aspect ratios."""
    SQUARE = "1:1"
    PORTRAIT = "9:16"
    LANDSCAPE = "16:9"
    ULTRAWIDE = "21:9"
    STANDARD = "4:3"
    WIDESCREEN = "3:2"


class Platform(Enum):
    """Target platform for images."""
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    TWITTER = "twitter"
    SPOTIFY = "spotify"
    APPLE_MUSIC = "apple_music"
    WEBSITE = "website"
    PRINT = "print"


class ImagePurpose(Enum):
    """Purpose of the generated image."""
    ALBUM_COVER = "album_cover"
    SINGLE_ARTWORK = "single_artwork"
    SOCIAL_MEDIA = "social_media"
    PROMOTIONAL = "promotional"
    MUSIC_VIDEO_STILL = "music_video_still"
    TOUR_POSTER = "tour_poster"
    MERCHANDISE = "merchandise"
    LYRIC_VIDEO = "lyric_video"


# ============================================================
# Data Classes
# ============================================================

@dataclass
class AudienceProfile:
    """Target audience profile from research."""
    age_range: str
    primary_platforms: List[str]
    visual_preferences: List[str]
    color_preferences: List[str]
    aesthetic_keywords: List[str]
    reference_artists: List[str]
    engagement_patterns: Dict[str, Any]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class StyleRecommendation:
    """Style recommendation from Vision Pro."""
    primary_style: ImageStyle
    secondary_styles: List[ImageStyle]
    color_palette: List[str]
    lighting_mood: str
    composition_notes: str
    reference_images: List[str]
    confidence_score: float

    def to_dict(self) -> Dict:
        return {
            'primary_style': self.primary_style.value,
            'secondary_styles': [s.value for s in self.secondary_styles],
            'color_palette': self.color_palette,
            'lighting_mood': self.lighting_mood,
            'composition_notes': self.composition_notes,
            'reference_images': self.reference_images,
            'confidence_score': self.confidence_score
        }


@dataclass
class ImagePrompt:
    """Generated image prompt."""
    main_prompt: str
    negative_prompt: str
    style_modifiers: List[str]
    technical_params: Dict[str, Any]
    aspect_ratio: AspectRatio
    seed_suggestion: Optional[int]
    model_recommendation: str

    def to_dict(self) -> Dict:
        return {
            'main_prompt': self.main_prompt,
            'negative_prompt': self.negative_prompt,
            'style_modifiers': self.style_modifiers,
            'technical_params': self.technical_params,
            'aspect_ratio': self.aspect_ratio.value,
            'seed_suggestion': self.seed_suggestion,
            'model_recommendation': self.model_recommendation
        }

    def get_full_prompt(self) -> str:
        """Get the complete prompt with all modifiers."""
        parts = [self.main_prompt]
        if self.style_modifiers:
            parts.extend(self.style_modifiers)
        return ", ".join(parts)


# ============================================================
# Demo Scout Agent
# ============================================================

class DemoScout:
    """
    Demo Scout - Audience Research Agent

    Analyzes target audience demographics, platform preferences,
    and visual tastes to inform image generation strategy.
    """

    # Genre-based audience profiles
    GENRE_DEMOGRAPHICS = {
        'hip-hop': {
            'age_range': '18-34',
            'primary_platforms': ['instagram', 'tiktok', 'twitter'],
            'visual_preferences': ['bold', 'urban', 'luxury', 'street'],
            'color_preferences': ['gold', 'black', 'red', 'purple'],
            'aesthetic_keywords': ['drip', 'flex', 'raw', 'authentic']
        },
        'electronic': {
            'age_range': '18-35',
            'primary_platforms': ['instagram', 'spotify', 'youtube'],
            'visual_preferences': ['neon', 'futuristic', 'abstract', 'geometric'],
            'color_preferences': ['cyan', 'magenta', 'purple', 'electric blue'],
            'aesthetic_keywords': ['vibe', 'energy', 'wave', 'minimal']
        },
        'r&b': {
            'age_range': '21-40',
            'primary_platforms': ['instagram', 'apple_music', 'twitter'],
            'visual_preferences': ['intimate', 'moody', 'sensual', 'sophisticated'],
            'color_preferences': ['burgundy', 'gold', 'navy', 'cream'],
            'aesthetic_keywords': ['smooth', 'vibe', 'mood', 'late night']
        },
        'rock': {
            'age_range': '18-45',
            'primary_platforms': ['youtube', 'instagram', 'spotify'],
            'visual_preferences': ['raw', 'gritty', 'powerful', 'authentic'],
            'color_preferences': ['black', 'red', 'silver', 'white'],
            'aesthetic_keywords': ['loud', 'raw', 'real', 'energy']
        },
        'pop': {
            'age_range': '13-35',
            'primary_platforms': ['tiktok', 'instagram', 'youtube'],
            'visual_preferences': ['bright', 'colorful', 'trendy', 'polished'],
            'color_preferences': ['pink', 'blue', 'yellow', 'pastel'],
            'aesthetic_keywords': ['fun', 'catchy', 'iconic', 'fresh']
        },
        'indie': {
            'age_range': '18-35',
            'primary_platforms': ['instagram', 'spotify', 'bandcamp'],
            'visual_preferences': ['artistic', 'vintage', 'authentic', 'unconventional'],
            'color_preferences': ['earth tones', 'muted', 'film grain', 'analog'],
            'aesthetic_keywords': ['authentic', 'unique', 'artsy', 'organic']
        },
        'ambient': {
            'age_range': '25-50',
            'primary_platforms': ['spotify', 'youtube', 'bandcamp'],
            'visual_preferences': ['ethereal', 'minimal', 'nature', 'abstract'],
            'color_preferences': ['soft blues', 'whites', 'grays', 'earth tones'],
            'aesthetic_keywords': ['peaceful', 'immersive', 'vast', 'serene']
        }
    }

    # Platform-specific recommendations
    PLATFORM_SPECS = {
        'instagram': {
            'ideal_aspect': AspectRatio.SQUARE,
            'alt_aspects': [AspectRatio.PORTRAIT],
            'style_notes': 'High contrast, scroll-stopping, text-friendly'
        },
        'tiktok': {
            'ideal_aspect': AspectRatio.PORTRAIT,
            'alt_aspects': [],
            'style_notes': 'Dynamic, bold, trend-aware, young aesthetic'
        },
        'youtube': {
            'ideal_aspect': AspectRatio.LANDSCAPE,
            'alt_aspects': [AspectRatio.WIDESCREEN],
            'style_notes': 'Thumbnail-friendly, clear focal point, readable text'
        },
        'spotify': {
            'ideal_aspect': AspectRatio.SQUARE,
            'alt_aspects': [],
            'style_notes': 'Works at small sizes, bold shapes, minimal text'
        },
        'twitter': {
            'ideal_aspect': AspectRatio.LANDSCAPE,
            'alt_aspects': [AspectRatio.SQUARE],
            'style_notes': 'Timeline-optimized, shareable, conversation-starting'
        }
    }

    def __init__(self):
        self.research_cache = {}

    def research_audience(self,
                         genre: str,
                         artist_description: Optional[str] = None,
                         target_platforms: Optional[List[str]] = None,
                         existing_fanbase: Optional[Dict] = None) -> AudienceProfile:
        """
        Research and profile the target audience.

        Args:
            genre: Music genre
            artist_description: Optional artist description for context
            target_platforms: Specific platforms to focus on
            existing_fanbase: Existing audience data if available

        Returns:
            AudienceProfile with demographics and preferences
        """
        # Get base profile from genre
        genre_lower = genre.lower()
        base_profile = self.GENRE_DEMOGRAPHICS.get(
            genre_lower,
            self.GENRE_DEMOGRAPHICS['pop']
        )

        # Determine platforms
        if target_platforms:
            platforms = target_platforms
        else:
            platforms = base_profile['primary_platforms']

        # Build reference artists based on genre
        reference_artists = self._get_reference_artists(genre_lower)

        # Analyze engagement patterns
        engagement = self._analyze_engagement_patterns(platforms, genre_lower)

        # Create profile
        profile = AudienceProfile(
            age_range=base_profile['age_range'],
            primary_platforms=platforms,
            visual_preferences=base_profile['visual_preferences'],
            color_preferences=base_profile['color_preferences'],
            aesthetic_keywords=base_profile['aesthetic_keywords'],
            reference_artists=reference_artists,
            engagement_patterns=engagement
        )

        return profile

    def _get_reference_artists(self, genre: str) -> List[str]:
        """Get reference artists for visual inspiration."""
        references = {
            'hip-hop': ['Travis Scott', 'Tyler the Creator', 'Kendrick Lamar', 'Drake'],
            'electronic': ['Daft Punk', 'Deadmau5', 'Porter Robinson', 'Skrillex'],
            'r&b': ['The Weeknd', 'Frank Ocean', 'SZA', 'Daniel Caesar'],
            'rock': ['Tame Impala', 'Arctic Monkeys', 'The 1975', 'Bring Me The Horizon'],
            'pop': ['Billie Eilish', 'Doja Cat', 'Harry Styles', 'Dua Lipa'],
            'indie': ['Bon Iver', 'Phoebe Bridgers', 'Mac DeMarco', 'Clairo'],
            'ambient': ['Brian Eno', 'Tycho', 'Bonobo', 'Khruangbin']
        }
        return references.get(genre, references['pop'])

    def _analyze_engagement_patterns(self, platforms: List[str], genre: str) -> Dict:
        """Analyze what content performs well."""
        return {
            'best_post_times': self._get_best_times(platforms),
            'content_types': self._get_content_types(genre),
            'hashtag_strategy': self._get_hashtags(genre),
            'visual_hooks': self._get_visual_hooks(genre)
        }

    def _get_best_times(self, platforms: List[str]) -> Dict:
        """Get optimal posting times by platform."""
        times = {
            'instagram': '11am-1pm, 7pm-9pm',
            'tiktok': '6am-9am, 7pm-11pm',
            'twitter': '12pm-3pm, 5pm-6pm',
            'youtube': '2pm-4pm, 9pm-11pm'
        }
        return {p: times.get(p, '12pm-3pm') for p in platforms}

    def _get_content_types(self, genre: str) -> List[str]:
        """Get recommended content types."""
        types = {
            'hip-hop': ['behind the scenes', 'studio sessions', 'lifestyle', 'performance'],
            'electronic': ['visuals', 'live sets', 'production tips', 'gear'],
            'r&b': ['intimate moments', 'aesthetic shots', 'mood pieces'],
            'rock': ['live energy', 'band dynamics', 'raw moments'],
            'pop': ['challenges', 'snippets', 'reactions', 'collabs']
        }
        return types.get(genre, types['pop'])

    def _get_hashtags(self, genre: str) -> List[str]:
        """Get relevant hashtags for the genre."""
        tags = {
            'hip-hop': ['#HipHop', '#NewMusic', '#Rap', '#Underground'],
            'electronic': ['#EDM', '#Electronic', '#Producer', '#Beats'],
            'r&b': ['#RnB', '#SoulMusic', '#Vibes', '#NewRnB'],
            'rock': ['#Rock', '#Alternative', '#IndieRock', '#LiveMusic'],
            'pop': ['#Pop', '#NewPop', '#MusicVibes', '#Trending']
        }
        return tags.get(genre, tags['pop'])

    def _get_visual_hooks(self, genre: str) -> List[str]:
        """Get visual elements that hook audiences."""
        hooks = {
            'hip-hop': ['contrast', 'luxury elements', 'urban texture', 'motion blur'],
            'electronic': ['light trails', 'geometric shapes', 'color gradients', 'symmetry'],
            'r&b': ['soft focus', 'intimate framing', 'warm tones', 'negative space'],
            'rock': ['high contrast', 'action shots', 'texture', 'dramatic lighting'],
            'pop': ['bright colors', 'clean composition', 'eye contact', 'movement']
        }
        return hooks.get(genre, hooks['pop'])


# ============================================================
# Vision Pro Agent
# ============================================================

class VisionPro:
    """
    Vision Pro - Visual Style Analysis Agent

    Analyzes visual trends, recommends styles, and determines
    the optimal aesthetic approach for image generation.
    """

    # Style associations by genre
    GENRE_STYLES = {
        'hip-hop': [ImageStyle.CINEMATIC, ImageStyle.DARK_MOODY, ImageStyle.NEON],
        'electronic': [ImageStyle.NEON, ImageStyle.SURREAL, ImageStyle.MINIMALIST],
        'r&b': [ImageStyle.CINEMATIC, ImageStyle.DARK_MOODY, ImageStyle.ARTISTIC],
        'rock': [ImageStyle.PHOTOREALISTIC, ImageStyle.DARK_MOODY, ImageStyle.VINTAGE],
        'pop': [ImageStyle.BRIGHT_VIBRANT, ImageStyle.ARTISTIC, ImageStyle.MINIMALIST],
        'indie': [ImageStyle.VINTAGE, ImageStyle.ARTISTIC, ImageStyle.ETHEREAL],
        'ambient': [ImageStyle.ETHEREAL, ImageStyle.MINIMALIST, ImageStyle.SURREAL]
    }

    # Mood to lighting map
    MOOD_LIGHTING = {
        'euphoric': 'high key, golden hour, warm backlight',
        'melancholic': 'low key, blue hour, soft shadows',
        'aggressive': 'hard contrast, dramatic shadows, rim lighting',
        'serene': 'soft diffused, even fill, natural light',
        'mysterious': 'silhouette, rim light, negative fill',
        'romantic': 'soft focus, warm tones, candle-like',
        'dark': 'minimal key, deep shadows, single source',
        'triumphant': 'heroic lighting, warm glow, uplighting'
    }

    # Color palettes by style
    STYLE_PALETTES = {
        ImageStyle.CINEMATIC: ['#1a1a2e', '#16213e', '#0f3460', '#e94560'],
        ImageStyle.NEON: ['#ff00ff', '#00ffff', '#ff0080', '#0080ff'],
        ImageStyle.VINTAGE: ['#d4a373', '#faedcd', '#ccd5ae', '#e9edc9'],
        ImageStyle.DARK_MOODY: ['#0d0d0d', '#1a1a1a', '#2d2d2d', '#4a0080'],
        ImageStyle.BRIGHT_VIBRANT: ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff'],
        ImageStyle.ETHEREAL: ['#e8d5b7', '#f5ebe0', '#d5bdaf', '#edede9'],
        ImageStyle.SURREAL: ['#7c3aed', '#a855f7', '#c084fc', '#ddd6fe'],
        ImageStyle.MINIMALIST: ['#ffffff', '#f5f5f5', '#333333', '#000000']
    }

    def __init__(self):
        self.analysis_cache = {}

    def analyze_style(self,
                     genre: str,
                     mood: str = 'serene',
                     purpose: ImagePurpose = ImagePurpose.ALBUM_COVER,
                     audience_profile: Optional[AudienceProfile] = None,
                     custom_preferences: Optional[Dict] = None) -> StyleRecommendation:
        """
        Analyze and recommend visual style.

        Args:
            genre: Music genre
            mood: Target emotional mood
            purpose: Image purpose (album cover, social, etc.)
            audience_profile: Audience data from Demo Scout
            custom_preferences: User's custom style preferences

        Returns:
            StyleRecommendation with full style spec
        """
        genre_lower = genre.lower()

        # Get base styles for genre
        base_styles = self.GENRE_STYLES.get(genre_lower, self.GENRE_STYLES['pop'])
        primary_style = base_styles[0]
        secondary_styles = base_styles[1:]

        # Override with custom preferences if provided
        if custom_preferences:
            if 'style' in custom_preferences:
                try:
                    primary_style = ImageStyle(custom_preferences['style'])
                except ValueError:
                    pass

        # Get color palette
        color_palette = self.STYLE_PALETTES.get(
            primary_style,
            self.STYLE_PALETTES[ImageStyle.CINEMATIC]
        )

        # Incorporate audience color preferences
        if audience_profile and audience_profile.color_preferences:
            color_palette = self._blend_palettes(
                color_palette,
                audience_profile.color_preferences
            )

        # Determine lighting
        lighting = self.MOOD_LIGHTING.get(mood.lower(), self.MOOD_LIGHTING['serene'])

        # Generate composition notes
        composition = self._get_composition_notes(purpose, primary_style)

        # Calculate confidence
        confidence = self._calculate_confidence(
            genre_lower, primary_style, audience_profile
        )

        return StyleRecommendation(
            primary_style=primary_style,
            secondary_styles=secondary_styles,
            color_palette=color_palette,
            lighting_mood=lighting,
            composition_notes=composition,
            reference_images=[],
            confidence_score=confidence
        )

    def _blend_palettes(self, base: List[str], preferences: List[str]) -> List[str]:
        """Blend color palettes with preferences."""
        # Simple blend: take first 2 from base, add up to 2 from preferences
        result = base[:2]
        for pref in preferences[:2]:
            if pref.startswith('#'):
                result.append(pref)
            else:
                # Convert color name to hex
                result.append(self._color_name_to_hex(pref))
        return result

    def _color_name_to_hex(self, name: str) -> str:
        """Convert color name to hex code."""
        color_map = {
            'gold': '#ffd700',
            'black': '#000000',
            'red': '#ff0000',
            'purple': '#7c3aed',
            'cyan': '#00ffff',
            'magenta': '#ff00ff',
            'blue': '#0066ff',
            'pink': '#ff69b4',
            'white': '#ffffff',
            'silver': '#c0c0c0',
            'burgundy': '#800020',
            'navy': '#000080',
            'cream': '#fffdd0'
        }
        return color_map.get(name.lower(), '#7c3aed')

    def _get_composition_notes(self, purpose: ImagePurpose, style: ImageStyle) -> str:
        """Get composition guidelines for the purpose."""
        notes = {
            ImagePurpose.ALBUM_COVER: "Strong central focal point, works at small sizes, memorable silhouette",
            ImagePurpose.SINGLE_ARTWORK: "Bold and immediate impact, clear visual hierarchy",
            ImagePurpose.SOCIAL_MEDIA: "Scroll-stopping, text-friendly margins, high contrast",
            ImagePurpose.PROMOTIONAL: "Space for text overlays, versatile cropping",
            ImagePurpose.MUSIC_VIDEO_STILL: "Cinematic framing, 16:9 safe zones, dynamic composition",
            ImagePurpose.TOUR_POSTER: "Vertical emphasis, bold typography zones, venue-flexible"
        }
        return notes.get(purpose, notes[ImagePurpose.ALBUM_COVER])

    def _calculate_confidence(self,
                             genre: str,
                             style: ImageStyle,
                             audience: Optional[AudienceProfile]) -> float:
        """Calculate confidence in style recommendation."""
        confidence = 0.7  # Base confidence

        # Boost if style matches genre defaults
        genre_styles = self.GENRE_STYLES.get(genre, [])
        if style in genre_styles:
            confidence += 0.15

        # Boost if we have audience data
        if audience:
            confidence += 0.1

        return min(1.0, confidence)


# ============================================================
# Style Sage Agent
# ============================================================

class StyleSage:
    """
    Style Sage - Style Refinement Agent

    Refines and ensures consistency of visual style,
    handles style blending, and maintains artistic coherence.
    """

    # Style modifier templates
    STYLE_MODIFIERS = {
        ImageStyle.CINEMATIC: [
            "cinematic lighting",
            "film grain",
            "anamorphic lens flare",
            "professional color grading",
            "shallow depth of field",
            "dramatic shadows"
        ],
        ImageStyle.PHOTOREALISTIC: [
            "photorealistic",
            "8K resolution",
            "hyperdetailed",
            "professional photography",
            "DSLR quality",
            "natural lighting"
        ],
        ImageStyle.NEON: [
            "neon lights",
            "cyberpunk aesthetic",
            "glowing edges",
            "reflective surfaces",
            "urban night scene",
            "chromatic aberration"
        ],
        ImageStyle.VINTAGE: [
            "vintage film photography",
            "analog grain",
            "faded colors",
            "70s aesthetic",
            "nostalgic mood",
            "warm color cast"
        ],
        ImageStyle.DARK_MOODY: [
            "moody atmosphere",
            "dark and atmospheric",
            "low key lighting",
            "dramatic shadows",
            "noir aesthetic",
            "rich blacks"
        ],
        ImageStyle.ETHEREAL: [
            "ethereal and dreamy",
            "soft glow",
            "heavenly light",
            "gentle atmosphere",
            "floating elements",
            "otherworldly"
        ],
        ImageStyle.SURREAL: [
            "surrealist art",
            "dreamlike",
            "impossible geometry",
            "mind-bending",
            "abstract elements",
            "fantasy atmosphere"
        ],
        ImageStyle.MINIMALIST: [
            "minimalist composition",
            "clean lines",
            "negative space",
            "simple geometry",
            "uncluttered",
            "elegant simplicity"
        ]
    }

    # Quality boosters
    QUALITY_MODIFIERS = [
        "masterpiece",
        "best quality",
        "highly detailed",
        "professional",
        "award-winning",
        "trending on artstation"
    ]

    # Negative prompt templates
    NEGATIVE_TEMPLATES = {
        'general': [
            "blurry", "low quality", "amateur", "distorted",
            "watermark", "signature", "text", "logo",
            "bad anatomy", "deformed", "disfigured"
        ],
        'portrait': [
            "extra limbs", "mutated hands", "bad proportions",
            "cropped", "out of frame", "duplicate"
        ],
        'artistic': [
            "photo-realistic", "3d render", "cartoon",
            "oversaturated", "overexposed"
        ]
    }

    def __init__(self):
        self.style_history = []

    def refine_style(self,
                    style_rec: StyleRecommendation,
                    additional_keywords: Optional[List[str]] = None,
                    avoid_keywords: Optional[List[str]] = None,
                    quality_level: str = 'high') -> Dict[str, Any]:
        """
        Refine and enhance the style specification.

        Args:
            style_rec: Base style recommendation from Vision Pro
            additional_keywords: Extra keywords to include
            avoid_keywords: Keywords to specifically avoid
            quality_level: 'standard', 'high', or 'ultra'

        Returns:
            Refined style specification dict
        """
        # Get base modifiers
        modifiers = list(self.STYLE_MODIFIERS.get(
            style_rec.primary_style,
            self.STYLE_MODIFIERS[ImageStyle.CINEMATIC]
        ))

        # Add quality boosters based on level
        if quality_level in ['high', 'ultra']:
            modifiers.extend(self.QUALITY_MODIFIERS[:3])
        if quality_level == 'ultra':
            modifiers.extend(self.QUALITY_MODIFIERS[3:])

        # Add custom keywords
        if additional_keywords:
            modifiers.extend(additional_keywords)

        # Build negative prompt
        negatives = list(self.NEGATIVE_TEMPLATES['general'])
        if avoid_keywords:
            negatives.extend(avoid_keywords)

        # Remove any avoided keywords from modifiers
        if avoid_keywords:
            modifiers = [m for m in modifiers if m not in avoid_keywords]

        # Get recommended model
        model = self._recommend_model(style_rec.primary_style, quality_level)

        return {
            'style_modifiers': modifiers,
            'negative_prompt': ", ".join(negatives),
            'color_palette': style_rec.color_palette,
            'lighting': style_rec.lighting_mood,
            'composition': style_rec.composition_notes,
            'recommended_model': model,
            'quality_level': quality_level,
            'refined_at': datetime.utcnow().isoformat()
        }

    def _recommend_model(self, style: ImageStyle, quality: str) -> str:
        """Recommend the best AI model for the style."""
        # Model recommendations based on style
        models = {
            ImageStyle.PHOTOREALISTIC: 'FLUX.1-dev',
            ImageStyle.CINEMATIC: 'FLUX.1-dev',
            ImageStyle.ARTISTIC: 'Midjourney',
            ImageStyle.ANIME: 'Anything V5',
            ImageStyle.SURREAL: 'SDXL',
            ImageStyle.NEON: 'FLUX.1-dev',
            ImageStyle.VINTAGE: 'SDXL',
            ImageStyle.DARK_MOODY: 'FLUX.1-dev'
        }

        base_model = models.get(style, 'FLUX.1-dev')

        # Upgrade for ultra quality
        if quality == 'ultra' and 'FLUX' in base_model:
            return 'FLUX.1-pro'

        return base_model

    def ensure_consistency(self,
                          prompts: List[ImagePrompt],
                          style_spec: Dict) -> List[ImagePrompt]:
        """
        Ensure visual consistency across multiple prompts.

        Args:
            prompts: List of generated prompts
            style_spec: Refined style specification

        Returns:
            Prompts with consistent styling
        """
        consistent_prompts = []

        # Core style elements that must be present
        core_modifiers = style_spec['style_modifiers'][:4]

        for prompt in prompts:
            # Ensure core modifiers are present
            existing = set(prompt.style_modifiers)
            for mod in core_modifiers:
                if mod not in existing:
                    prompt.style_modifiers.append(mod)

            # Ensure consistent negative prompt
            if style_spec['negative_prompt'] not in prompt.negative_prompt:
                prompt.negative_prompt = style_spec['negative_prompt']

            consistent_prompts.append(prompt)

        return consistent_prompts


# ============================================================
# Prompt Oracle Agent
# ============================================================

class PromptOracle:
    """
    Prompt Oracle - Final Prompt Generation Agent

    Synthesizes all research and style analysis into
    optimized, production-ready image generation prompts.
    """

    # Subject templates by purpose
    SUBJECT_TEMPLATES = {
        ImagePurpose.ALBUM_COVER: "{artist_vibe} {scene_description}, album cover art, iconic composition",
        ImagePurpose.SINGLE_ARTWORK: "{artist_vibe} {scene_description}, single artwork, bold visual statement",
        ImagePurpose.SOCIAL_MEDIA: "{artist_vibe} {scene_description}, social media content, engaging composition",
        ImagePurpose.PROMOTIONAL: "{artist_vibe} {scene_description}, promotional image, professional quality",
        ImagePurpose.MUSIC_VIDEO_STILL: "{artist_vibe} {scene_description}, music video still, cinematic frame"
    }

    # Technical parameter presets
    TECH_PRESETS = {
        'standard': {
            'steps': 30,
            'cfg_scale': 7.0,
            'sampler': 'DPM++ 2M Karras'
        },
        'high': {
            'steps': 50,
            'cfg_scale': 7.5,
            'sampler': 'DPM++ 2M Karras'
        },
        'ultra': {
            'steps': 80,
            'cfg_scale': 8.0,
            'sampler': 'DPM++ 3M SDE Karras'
        }
    }

    def __init__(self):
        self.prompts_generated = []

    def generate_prompt(self,
                       concept: str,
                       purpose: ImagePurpose,
                       style_spec: Dict,
                       audience: Optional[AudienceProfile] = None,
                       aspect_ratio: AspectRatio = AspectRatio.SQUARE,
                       quality: str = 'high') -> ImagePrompt:
        """
        Generate the final optimized prompt.

        Args:
            concept: The core visual concept description
            purpose: Image purpose
            style_spec: Refined style from Style Sage
            audience: Audience profile from Demo Scout
            aspect_ratio: Target aspect ratio
            quality: Quality level

        Returns:
            Complete ImagePrompt ready for generation
        """
        # Build main prompt
        main_parts = [concept]

        # Add style modifiers
        main_parts.extend(style_spec.get('style_modifiers', [])[:5])

        # Add lighting
        if 'lighting' in style_spec:
            main_parts.append(style_spec['lighting'])

        # Add composition notes
        if 'composition' in style_spec:
            main_parts.append(style_spec['composition'])

        # Incorporate audience-specific elements
        if audience:
            hooks = audience.engagement_patterns.get('visual_hooks', [])
            if hooks:
                main_parts.append(hooks[0])

        # Build the main prompt string
        main_prompt = ", ".join(main_parts)

        # Get technical params
        tech_params = dict(self.TECH_PRESETS.get(quality, self.TECH_PRESETS['high']))

        # Add resolution based on aspect ratio
        resolutions = {
            AspectRatio.SQUARE: (1024, 1024),
            AspectRatio.PORTRAIT: (768, 1344),
            AspectRatio.LANDSCAPE: (1344, 768),
            AspectRatio.ULTRAWIDE: (1536, 640),
            AspectRatio.STANDARD: (1024, 768),
            AspectRatio.WIDESCREEN: (1216, 832)
        }
        tech_params['width'], tech_params['height'] = resolutions.get(
            aspect_ratio, (1024, 1024)
        )

        # Create the prompt
        prompt = ImagePrompt(
            main_prompt=main_prompt,
            negative_prompt=style_spec.get('negative_prompt', ''),
            style_modifiers=style_spec.get('style_modifiers', []),
            technical_params=tech_params,
            aspect_ratio=aspect_ratio,
            seed_suggestion=None,
            model_recommendation=style_spec.get('recommended_model', 'FLUX.1-dev')
        )

        self.prompts_generated.append(prompt)
        return prompt

    def generate_batch(self,
                      concepts: List[str],
                      purpose: ImagePurpose,
                      style_spec: Dict,
                      audience: Optional[AudienceProfile] = None,
                      aspect_ratio: AspectRatio = AspectRatio.SQUARE,
                      quality: str = 'high') -> List[ImagePrompt]:
        """
        Generate a batch of consistent prompts.

        Args:
            concepts: List of visual concepts
            purpose: Image purpose
            style_spec: Refined style spec
            audience: Audience profile
            aspect_ratio: Target aspect ratio
            quality: Quality level

        Returns:
            List of ImagePrompts
        """
        prompts = []

        for concept in concepts:
            prompt = self.generate_prompt(
                concept=concept,
                purpose=purpose,
                style_spec=style_spec,
                audience=audience,
                aspect_ratio=aspect_ratio,
                quality=quality
            )
            prompts.append(prompt)

        return prompts

    def optimize_for_model(self, prompt: ImagePrompt, model: str) -> ImagePrompt:
        """
        Optimize a prompt for a specific AI model.

        Args:
            prompt: The base prompt
            model: Target model name

        Returns:
            Optimized prompt for the model
        """
        # Model-specific optimizations
        if 'FLUX' in model:
            # FLUX prefers more detailed, natural language prompts
            prompt.main_prompt = self._expand_prompt(prompt.main_prompt)
            prompt.technical_params['cfg_scale'] = 3.5  # FLUX uses lower CFG
        elif 'Midjourney' in model:
            # Midjourney prefers specific syntax
            prompt.main_prompt = f"{prompt.main_prompt} --v 6 --ar {prompt.aspect_ratio.value}"
        elif 'SDXL' in model:
            # SDXL works well with specific keywords
            prompt.style_modifiers.append("SDXL style")

        prompt.model_recommendation = model
        return prompt

    def _expand_prompt(self, prompt: str) -> str:
        """Expand prompt for models that prefer detailed descriptions."""
        # Add natural language flow
        expanded = prompt.replace(", ", ". The image features ")
        expanded = f"A stunning image of {expanded}"
        return expanded


# ============================================================
# ImageBrain Main Class
# ============================================================

@dataclass
class ImageBrainOutput:
    """Complete output from ImageBrain pipeline."""
    audience_profile: AudienceProfile
    style_recommendation: StyleRecommendation
    style_spec: Dict
    prompts: List[ImagePrompt]
    metadata: Dict

    def to_dict(self) -> Dict:
        return {
            'audience_profile': self.audience_profile.to_dict(),
            'style_recommendation': self.style_recommendation.to_dict(),
            'style_spec': self.style_spec,
            'prompts': [p.to_dict() for p in self.prompts],
            'metadata': self.metadata
        }


class ImageBrain:
    """
    ImageBrain - AI Still Image Generator

    Orchestrates the full agent pipeline:
    1. Demo Scout - Audience research
    2. Vision Pro - Style analysis
    3. Style Sage - Style refinement
    4. Prompt Oracle - Prompt generation
    """

    def __init__(self, genre: str = "electronic"):
        self.genre = genre.lower()

        # Initialize agents
        self.demo_scout = DemoScout()
        self.vision_pro = VisionPro()
        self.style_sage = StyleSage()
        self.prompt_oracle = PromptOracle()

        # State
        self.current_audience: Optional[AudienceProfile] = None
        self.current_style: Optional[StyleRecommendation] = None
        self.current_spec: Optional[Dict] = None

    def research(self,
                artist_description: Optional[str] = None,
                target_platforms: Optional[List[str]] = None,
                existing_data: Optional[Dict] = None) -> Dict:
        """
        Phase 1: Research audience and visual preferences.

        Args:
            artist_description: Description of the artist/project
            target_platforms: Target social platforms
            existing_data: Any existing audience data

        Returns:
            Research results dict
        """
        # Demo Scout research
        audience = self.demo_scout.research_audience(
            genre=self.genre,
            artist_description=artist_description,
            target_platforms=target_platforms,
            existing_fanbase=existing_data
        )
        self.current_audience = audience

        # Vision Pro initial analysis
        style_rec = self.vision_pro.analyze_style(
            genre=self.genre,
            mood='serene',
            audience_profile=audience
        )
        self.current_style = style_rec

        return {
            'success': True,
            'audience_profile': audience.to_dict(),
            'initial_style': style_rec.to_dict(),
            'recommendations': {
                'platforms': audience.primary_platforms,
                'visual_hooks': audience.engagement_patterns.get('visual_hooks', []),
                'color_palette': style_rec.color_palette,
                'suggested_style': style_rec.primary_style.value
            }
        }

    def generate(self,
                concepts: List[str],
                purpose: str = 'album_cover',
                mood: str = 'serene',
                aspect_ratio: str = '1:1',
                quality: str = 'high',
                custom_style: Optional[str] = None,
                additional_keywords: Optional[List[str]] = None) -> Dict:
        """
        Phase 2: Generate image prompts.

        Args:
            concepts: List of visual concepts to generate
            purpose: Image purpose (album_cover, social_media, etc.)
            mood: Emotional mood
            aspect_ratio: Target aspect ratio
            quality: Quality level (standard, high, ultra)
            custom_style: Override style
            additional_keywords: Extra keywords to include

        Returns:
            Generation results with prompts
        """
        # Parse purpose
        purpose_map = {
            'album_cover': ImagePurpose.ALBUM_COVER,
            'single_artwork': ImagePurpose.SINGLE_ARTWORK,
            'social_media': ImagePurpose.SOCIAL_MEDIA,
            'promotional': ImagePurpose.PROMOTIONAL,
            'music_video_still': ImagePurpose.MUSIC_VIDEO_STILL
        }
        img_purpose = purpose_map.get(purpose.lower(), ImagePurpose.ALBUM_COVER)

        # Parse aspect ratio
        ar_map = {
            '1:1': AspectRatio.SQUARE,
            '9:16': AspectRatio.PORTRAIT,
            '16:9': AspectRatio.LANDSCAPE,
            '21:9': AspectRatio.ULTRAWIDE,
            '4:3': AspectRatio.STANDARD
        }
        ar = ar_map.get(aspect_ratio, AspectRatio.SQUARE)

        # Run research if not done yet
        if not self.current_audience:
            self.research()

        # Vision Pro analysis with custom preferences
        custom_prefs = {'style': custom_style} if custom_style else None
        style_rec = self.vision_pro.analyze_style(
            genre=self.genre,
            mood=mood,
            purpose=img_purpose,
            audience_profile=self.current_audience,
            custom_preferences=custom_prefs
        )
        self.current_style = style_rec

        # Style Sage refinement
        style_spec = self.style_sage.refine_style(
            style_rec=style_rec,
            additional_keywords=additional_keywords,
            quality_level=quality
        )
        self.current_spec = style_spec

        # Prompt Oracle generation
        prompts = self.prompt_oracle.generate_batch(
            concepts=concepts,
            purpose=img_purpose,
            style_spec=style_spec,
            audience=self.current_audience,
            aspect_ratio=ar,
            quality=quality
        )

        # Ensure consistency
        prompts = self.style_sage.ensure_consistency(prompts, style_spec)

        return {
            'success': True,
            'prompts': [p.to_dict() for p in prompts],
            'style': style_rec.to_dict(),
            'style_spec': style_spec,
            'generation_settings': {
                'purpose': img_purpose.value,
                'aspect_ratio': ar.value,
                'quality': quality,
                'model': style_spec.get('recommended_model', 'FLUX.1-dev')
            }
        }

    def full_pipeline(self,
                     concepts: List[str],
                     artist_description: Optional[str] = None,
                     purpose: str = 'album_cover',
                     mood: str = 'serene',
                     aspect_ratio: str = '1:1',
                     quality: str = 'high',
                     target_platforms: Optional[List[str]] = None) -> ImageBrainOutput:
        """
        Run the complete ImageBrain pipeline.

        Args:
            concepts: Visual concepts to generate
            artist_description: Artist/project description
            purpose: Image purpose
            mood: Emotional mood
            aspect_ratio: Target aspect ratio
            quality: Quality level
            target_platforms: Target platforms

        Returns:
            Complete ImageBrainOutput
        """
        # Phase 1: Research
        self.research(
            artist_description=artist_description,
            target_platforms=target_platforms
        )

        # Phase 2: Generate
        result = self.generate(
            concepts=concepts,
            purpose=purpose,
            mood=mood,
            aspect_ratio=aspect_ratio,
            quality=quality
        )

        # Build output
        output = ImageBrainOutput(
            audience_profile=self.current_audience,
            style_recommendation=self.current_style,
            style_spec=self.current_spec,
            prompts=[self.prompt_oracle.prompts_generated[-len(concepts):]],
            metadata={
                'genre': self.genre,
                'purpose': purpose,
                'mood': mood,
                'quality': quality,
                'generated_at': datetime.utcnow().isoformat()
            }
        )

        return output
