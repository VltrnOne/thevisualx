"""
ColorBrain™ - Grading Engine
Powered by VLTRN / VISUALX

Intelligent color grading system for mood-driven
visual consistency and cinematic look development.
"""

import os
import json
import colorsys
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

from visualx_agents import ColorPalette, EmotionalTone, TheColorist


# ============================================================
# Color Science Types
# ============================================================

class ColorSpace(Enum):
    """Color space specifications."""
    SRGB = "sRGB"
    REC709 = "Rec.709"
    REC2020 = "Rec.2020"
    DCI_P3 = "DCI-P3"
    ACES = "ACES"
    LOG = "Log"


class LookStyle(Enum):
    """Cinematic look styles."""
    BLOCKBUSTER = "blockbuster"      # Orange/teal, high contrast
    INDIE = "indie"                   # Muted, natural
    VINTAGE = "vintage"               # Warm, faded
    NEON = "neon"                     # Saturated, cyan/magenta
    NOIR = "noir"                     # High contrast B&W or desaturated
    NATURAL = "natural"               # Minimal grading
    DREAM = "dream"                   # Soft, ethereal
    GRITTY = "gritty"                 # Crushed blacks, grain
    PASTEL = "pastel"                 # Soft, lifted shadows
    MOODY = "moody"                   # Deep shadows, selective color


@dataclass
class ColorWheelAdjustment:
    """Adjustment for a color wheel region."""
    lift: Tuple[float, float, float]  # RGB -1 to 1
    gamma: Tuple[float, float, float]
    gain: Tuple[float, float, float]

    def to_dict(self) -> Dict:
        return {
            'lift': list(self.lift),
            'gamma': list(self.gamma),
            'gain': list(self.gain)
        }


@dataclass
class GradeSpec:
    """Complete color grade specification."""
    name: str
    look_style: LookStyle
    color_wheels: ColorWheelAdjustment
    saturation: float
    contrast: float
    temperature: float  # -100 (cool) to 100 (warm)
    tint: float  # -100 (green) to 100 (magenta)
    exposure: float  # EV adjustment
    highlights: float
    shadows: float
    whites: float
    blacks: float
    vibrance: float
    hue_shift: float
    film_grain: float
    vignette: float
    lut_reference: Optional[str]

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'look_style': self.look_style.value,
            'color_wheels': self.color_wheels.to_dict(),
            'saturation': self.saturation,
            'contrast': self.contrast,
            'temperature': self.temperature,
            'tint': self.tint,
            'exposure': self.exposure,
            'highlights': self.highlights,
            'shadows': self.shadows,
            'whites': self.whites,
            'blacks': self.blacks,
            'vibrance': self.vibrance,
            'hue_shift': self.hue_shift,
            'film_grain': self.film_grain,
            'vignette': self.vignette,
            'lut_reference': self.lut_reference
        }


# ============================================================
# Look Development Engine
# ============================================================

class LookDevelopment:
    """
    Develops cinematic looks based on mood and genre.
    """

    # Preset look recipes
    LOOK_RECIPES = {
        LookStyle.BLOCKBUSTER: {
            'color_wheels': ColorWheelAdjustment(
                lift=(0.0, -0.05, 0.1),      # Blue shadows
                gamma=(1.02, 0.98, 0.95),    # Slight warm midtones
                gain=(1.1, 0.95, 0.85)       # Orange highlights
            ),
            'saturation': 1.15,
            'contrast': 1.2,
            'temperature': 15,
            'tint': 0,
            'highlights': 10,
            'shadows': -15,
            'blacks': -5,
            'vibrance': 1.1,
            'film_grain': 0.1,
            'vignette': 0.15
        },
        LookStyle.INDIE: {
            'color_wheels': ColorWheelAdjustment(
                lift=(0.02, 0.01, -0.02),
                gamma=(0.98, 1.0, 1.02),
                gain=(0.95, 1.0, 1.02)
            ),
            'saturation': 0.85,
            'contrast': 0.95,
            'temperature': -5,
            'tint': 5,
            'highlights': -5,
            'shadows': 10,
            'blacks': 5,
            'vibrance': 0.9,
            'film_grain': 0.2,
            'vignette': 0.1
        },
        LookStyle.VINTAGE: {
            'color_wheels': ColorWheelAdjustment(
                lift=(0.05, 0.02, -0.03),
                gamma=(1.05, 1.0, 0.92),
                gain=(1.1, 1.0, 0.85)
            ),
            'saturation': 0.8,
            'contrast': 0.9,
            'temperature': 25,
            'tint': 5,
            'highlights': -10,
            'shadows': 15,
            'blacks': 10,
            'vibrance': 0.85,
            'film_grain': 0.35,
            'vignette': 0.25
        },
        LookStyle.NEON: {
            'color_wheels': ColorWheelAdjustment(
                lift=(0.0, 0.02, 0.1),       # Cyan shadows
                gamma=(1.0, 0.95, 1.05),
                gain=(1.1, 0.9, 1.15)        # Magenta/cyan highlights
            ),
            'saturation': 1.4,
            'contrast': 1.3,
            'temperature': -10,
            'tint': 10,
            'highlights': 15,
            'shadows': -20,
            'blacks': -15,
            'vibrance': 1.3,
            'film_grain': 0.05,
            'vignette': 0.2
        },
        LookStyle.NOIR: {
            'color_wheels': ColorWheelAdjustment(
                lift=(0.0, 0.0, 0.02),
                gamma=(0.98, 0.98, 1.0),
                gain=(1.0, 1.0, 1.02)
            ),
            'saturation': 0.15,
            'contrast': 1.4,
            'temperature': -5,
            'tint': 0,
            'highlights': 20,
            'shadows': -30,
            'blacks': -20,
            'vibrance': 0.5,
            'film_grain': 0.25,
            'vignette': 0.35
        },
        LookStyle.NATURAL: {
            'color_wheels': ColorWheelAdjustment(
                lift=(0.0, 0.0, 0.0),
                gamma=(1.0, 1.0, 1.0),
                gain=(1.0, 1.0, 1.0)
            ),
            'saturation': 1.0,
            'contrast': 1.05,
            'temperature': 0,
            'tint': 0,
            'highlights': 0,
            'shadows': 0,
            'blacks': 0,
            'vibrance': 1.0,
            'film_grain': 0.0,
            'vignette': 0.0
        },
        LookStyle.DREAM: {
            'color_wheels': ColorWheelAdjustment(
                lift=(0.08, 0.05, 0.1),
                gamma=(1.02, 1.0, 1.05),
                gain=(1.0, 0.98, 1.1)
            ),
            'saturation': 0.9,
            'contrast': 0.85,
            'temperature': 5,
            'tint': 5,
            'highlights': -15,
            'shadows': 25,
            'blacks': 20,
            'vibrance': 0.95,
            'film_grain': 0.15,
            'vignette': 0.2
        },
        LookStyle.GRITTY: {
            'color_wheels': ColorWheelAdjustment(
                lift=(-0.02, -0.02, 0.0),
                gamma=(0.95, 0.95, 0.98),
                gain=(1.05, 1.0, 0.95)
            ),
            'saturation': 0.9,
            'contrast': 1.35,
            'temperature': 5,
            'tint': -5,
            'highlights': 5,
            'shadows': -25,
            'blacks': -20,
            'vibrance': 0.95,
            'film_grain': 0.4,
            'vignette': 0.25
        },
        LookStyle.PASTEL: {
            'color_wheels': ColorWheelAdjustment(
                lift=(0.1, 0.08, 0.12),
                gamma=(1.05, 1.02, 1.08),
                gain=(0.95, 0.95, 1.0)
            ),
            'saturation': 0.7,
            'contrast': 0.8,
            'temperature': 10,
            'tint': 5,
            'highlights': -20,
            'shadows': 30,
            'blacks': 25,
            'vibrance': 0.85,
            'film_grain': 0.1,
            'vignette': 0.1
        },
        LookStyle.MOODY: {
            'color_wheels': ColorWheelAdjustment(
                lift=(-0.03, 0.0, 0.05),
                gamma=(0.95, 0.98, 1.02),
                gain=(1.05, 1.0, 1.1)
            ),
            'saturation': 0.85,
            'contrast': 1.2,
            'temperature': -15,
            'tint': 5,
            'highlights': 0,
            'shadows': -20,
            'blacks': -10,
            'vibrance': 0.9,
            'film_grain': 0.2,
            'vignette': 0.3
        }
    }

    # Genre to look mapping
    GENRE_LOOKS = {
        'hip-hop': [LookStyle.BLOCKBUSTER, LookStyle.NEON, LookStyle.GRITTY],
        'electronic': [LookStyle.NEON, LookStyle.BLOCKBUSTER, LookStyle.MOODY],
        'r&b': [LookStyle.MOODY, LookStyle.DREAM, LookStyle.NATURAL],
        'rock': [LookStyle.GRITTY, LookStyle.BLOCKBUSTER, LookStyle.NOIR],
        'pop': [LookStyle.BLOCKBUSTER, LookStyle.PASTEL, LookStyle.NATURAL],
        'ambient': [LookStyle.DREAM, LookStyle.NATURAL, LookStyle.PASTEL],
        'indie': [LookStyle.INDIE, LookStyle.VINTAGE, LookStyle.NATURAL]
    }

    # Emotion to look mapping
    EMOTION_LOOKS = {
        EmotionalTone.EUPHORIC: [LookStyle.BLOCKBUSTER, LookStyle.NEON],
        EmotionalTone.MELANCHOLIC: [LookStyle.MOODY, LookStyle.INDIE],
        EmotionalTone.AGGRESSIVE: [LookStyle.GRITTY, LookStyle.NOIR],
        EmotionalTone.SERENE: [LookStyle.DREAM, LookStyle.PASTEL],
        EmotionalTone.MYSTERIOUS: [LookStyle.MOODY, LookStyle.NOIR],
        EmotionalTone.ROMANTIC: [LookStyle.DREAM, LookStyle.VINTAGE],
        EmotionalTone.DARK: [LookStyle.NOIR, LookStyle.GRITTY],
        EmotionalTone.TRIUMPHANT: [LookStyle.BLOCKBUSTER, LookStyle.NATURAL],
        EmotionalTone.ANXIOUS: [LookStyle.GRITTY, LookStyle.MOODY],
        EmotionalTone.NOSTALGIC: [LookStyle.VINTAGE, LookStyle.PASTEL]
    }

    @classmethod
    def get_look_for_context(cls, genre: str, emotion: EmotionalTone) -> LookStyle:
        """Get recommended look based on genre and emotion."""
        genre_looks = set(cls.GENRE_LOOKS.get(genre.lower(), [LookStyle.NATURAL]))
        emotion_looks = set(cls.EMOTION_LOOKS.get(emotion, [LookStyle.NATURAL]))

        # Find intersection
        common = genre_looks.intersection(emotion_looks)
        if common:
            return list(common)[0]

        # Fall back to emotion preference
        return cls.EMOTION_LOOKS.get(emotion, [LookStyle.NATURAL])[0]

    @classmethod
    def get_recipe(cls, look_style: LookStyle) -> Dict:
        """Get the grading recipe for a look style."""
        return cls.LOOK_RECIPES.get(look_style, cls.LOOK_RECIPES[LookStyle.NATURAL])


# ============================================================
# Color Harmony Engine
# ============================================================

class ColorHarmony:
    """
    Color theory and harmony calculations.
    """

    @staticmethod
    def hex_to_hsl(hex_color: str) -> Tuple[float, float, float]:
        """Convert hex color to HSL."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return colorsys.rgb_to_hls(r, g, b)

    @staticmethod
    def hsl_to_hex(h: float, s: float, l: float) -> str:
        """Convert HSL to hex color."""
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    @classmethod
    def get_complementary(cls, hex_color: str) -> str:
        """Get complementary color."""
        h, l, s = cls.hex_to_hsl(hex_color)
        comp_h = (h + 0.5) % 1.0
        return cls.hsl_to_hex(comp_h, s, l)

    @classmethod
    def get_analogous(cls, hex_color: str) -> Tuple[str, str]:
        """Get analogous colors (±30 degrees)."""
        h, l, s = cls.hex_to_hsl(hex_color)
        analog1 = (h + 1/12) % 1.0
        analog2 = (h - 1/12) % 1.0
        return cls.hsl_to_hex(analog1, s, l), cls.hsl_to_hex(analog2, s, l)

    @classmethod
    def get_triadic(cls, hex_color: str) -> Tuple[str, str]:
        """Get triadic colors (±120 degrees)."""
        h, l, s = cls.hex_to_hsl(hex_color)
        triad1 = (h + 1/3) % 1.0
        triad2 = (h + 2/3) % 1.0
        return cls.hsl_to_hex(triad1, s, l), cls.hsl_to_hex(triad2, s, l)

    @classmethod
    def get_split_complementary(cls, hex_color: str) -> Tuple[str, str]:
        """Get split-complementary colors."""
        h, l, s = cls.hex_to_hsl(hex_color)
        split1 = (h + 5/12) % 1.0
        split2 = (h + 7/12) % 1.0
        return cls.hsl_to_hex(split1, s, l), cls.hsl_to_hex(split2, s, l)


# ============================================================
# ColorBrain Main Class
# ============================================================

class ColorBrain:
    """
    ColorBrain™ - Intelligent Color Grading Engine

    Creates mood-driven color grades using:
    - Genre-appropriate look development
    - Emotional color psychology
    - Scene-to-scene consistency
    - Professional color science
    """

    def __init__(self, genre: str = "electronic"):
        self.genre = genre.lower()
        self.colorist = TheColorist(genre=genre)
        self.look_dev = LookDevelopment()
        self.harmony = ColorHarmony()
        self.master_grade: Optional[GradeSpec] = None
        self.shot_grades: Dict[int, GradeSpec] = {}

    def develop_master_look(self,
                           emotion: EmotionalTone,
                           custom_style: Optional[LookStyle] = None,
                           key_color: Optional[str] = None) -> GradeSpec:
        """
        Develop the master look for the project.

        Args:
            emotion: Primary emotional tone
            custom_style: Override automatic style selection
            key_color: Key color hex (optional)

        Returns:
            GradeSpec for the master look
        """
        # Determine look style
        if custom_style:
            look_style = custom_style
        else:
            look_style = self.look_dev.get_look_for_context(self.genre, emotion)

        # Get recipe
        recipe = self.look_dev.get_recipe(look_style)

        # Adjust based on key color if provided
        if key_color:
            recipe = self._adjust_for_key_color(recipe, key_color)

        # Create grade spec
        self.master_grade = GradeSpec(
            name=f"Master_{look_style.value}_{self.genre}",
            look_style=look_style,
            color_wheels=recipe['color_wheels'],
            saturation=recipe['saturation'],
            contrast=recipe['contrast'],
            temperature=recipe['temperature'],
            tint=recipe['tint'],
            exposure=0.0,
            highlights=recipe['highlights'],
            shadows=recipe['shadows'],
            whites=0,
            blacks=recipe['blacks'],
            vibrance=recipe['vibrance'],
            hue_shift=0,
            film_grain=recipe['film_grain'],
            vignette=recipe['vignette'],
            lut_reference=None
        )

        return self.master_grade

    def _adjust_for_key_color(self, recipe: Dict, key_color: str) -> Dict:
        """Adjust recipe to incorporate key color."""
        h, l, s = self.harmony.hex_to_hsl(key_color)

        # Adjust gain to push highlights toward key color
        hue_factor = h * 0.1  # Subtle shift

        adjusted = recipe.copy()
        # Slight color wheel adjustment based on key color hue
        original_wheels = recipe['color_wheels']
        adjusted['color_wheels'] = ColorWheelAdjustment(
            lift=original_wheels.lift,
            gamma=original_wheels.gamma,
            gain=(
                original_wheels.gain[0] + hue_factor if h < 0.33 else original_wheels.gain[0],
                original_wheels.gain[1] + hue_factor if 0.33 <= h < 0.66 else original_wheels.gain[1],
                original_wheels.gain[2] + hue_factor if h >= 0.66 else original_wheels.gain[2]
            )
        )

        return adjusted

    def grade_shot(self,
                  shot_index: int,
                  shot_emotion: EmotionalTone,
                  energy_level: float,
                  adjustment_strength: float = 0.3) -> GradeSpec:
        """
        Create a shot-specific grade variation.

        Args:
            shot_index: Index of the shot
            shot_emotion: Emotion for this specific shot
            energy_level: Energy level 0-1
            adjustment_strength: How much to deviate from master (0-1)

        Returns:
            GradeSpec for the shot
        """
        if not self.master_grade:
            self.develop_master_look(shot_emotion)

        # Start with master values
        shot_grade = GradeSpec(
            name=f"Shot_{shot_index:03d}_{shot_emotion.value}",
            look_style=self.master_grade.look_style,
            color_wheels=self.master_grade.color_wheels,
            saturation=self.master_grade.saturation,
            contrast=self.master_grade.contrast,
            temperature=self.master_grade.temperature,
            tint=self.master_grade.tint,
            exposure=self.master_grade.exposure,
            highlights=self.master_grade.highlights,
            shadows=self.master_grade.shadows,
            whites=self.master_grade.whites,
            blacks=self.master_grade.blacks,
            vibrance=self.master_grade.vibrance,
            hue_shift=self.master_grade.hue_shift,
            film_grain=self.master_grade.film_grain,
            vignette=self.master_grade.vignette,
            lut_reference=self.master_grade.lut_reference
        )

        # Adjust based on shot emotion
        emotion_recipe = self.look_dev.get_recipe(
            self.look_dev.get_look_for_context(self.genre, shot_emotion)
        )

        # Blend with master (using adjustment_strength)
        shot_grade.saturation = self._blend(
            self.master_grade.saturation,
            emotion_recipe['saturation'],
            adjustment_strength
        )
        shot_grade.contrast = self._blend(
            self.master_grade.contrast,
            emotion_recipe['contrast'],
            adjustment_strength
        )
        shot_grade.temperature = self._blend(
            self.master_grade.temperature,
            emotion_recipe['temperature'],
            adjustment_strength
        )

        # Energy-based adjustments
        if energy_level > 0.7:
            shot_grade.contrast *= 1.05
            shot_grade.vibrance *= 1.1
        elif energy_level < 0.3:
            shot_grade.contrast *= 0.95
            shot_grade.saturation *= 0.95

        self.shot_grades[shot_index] = shot_grade
        return shot_grade

    def _blend(self, a: float, b: float, factor: float) -> float:
        """Blend two values by factor."""
        return a + (b - a) * factor

    def get_color_palette(self, num_colors: int = 5) -> List[str]:
        """Get a harmonious color palette based on master grade."""
        if not self.master_grade:
            return ["#333333", "#666666", "#999999", "#cccccc", "#ffffff"]

        # Base color from temperature
        if self.master_grade.temperature > 0:
            base = "#ffa07a"  # Warm
        else:
            base = "#6495ed"  # Cool

        # Build palette
        palette = [base]
        comp = self.harmony.get_complementary(base)
        palette.append(comp)

        analog1, analog2 = self.harmony.get_analogous(base)
        palette.extend([analog1, analog2])

        if num_colors >= 5:
            triad1, _ = self.harmony.get_triadic(base)
            palette.append(triad1)

        return palette[:num_colors]

    def export_davinci_xml(self, output_path: str) -> str:
        """Export grade as DaVinci Resolve compatible XML."""
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<ColorCorrection>\n'

        if self.master_grade:
            xml_content += f'  <Name>{self.master_grade.name}</Name>\n'
            xml_content += '  <LiftOffset>\n'
            cw = self.master_grade.color_wheels
            xml_content += f'    <R>{cw.lift[0]:.4f}</R>\n'
            xml_content += f'    <G>{cw.lift[1]:.4f}</G>\n'
            xml_content += f'    <B>{cw.lift[2]:.4f}</B>\n'
            xml_content += '  </LiftOffset>\n'
            xml_content += '  <GammaOffset>\n'
            xml_content += f'    <R>{cw.gamma[0]:.4f}</R>\n'
            xml_content += f'    <G>{cw.gamma[1]:.4f}</G>\n'
            xml_content += f'    <B>{cw.gamma[2]:.4f}</B>\n'
            xml_content += '  </GammaOffset>\n'
            xml_content += '  <GainOffset>\n'
            xml_content += f'    <R>{cw.gain[0]:.4f}</R>\n'
            xml_content += f'    <G>{cw.gain[1]:.4f}</G>\n'
            xml_content += f'    <B>{cw.gain[2]:.4f}</B>\n'
            xml_content += '  </GainOffset>\n'
            xml_content += f'  <Saturation>{self.master_grade.saturation:.4f}</Saturation>\n'
            xml_content += f'  <Contrast>{self.master_grade.contrast:.4f}</Contrast>\n'

        xml_content += '</ColorCorrection>\n'

        with open(output_path, 'w') as f:
            f.write(xml_content)

        return output_path

    def export_grades_json(self, output_path: str) -> str:
        """Export all grades as JSON."""
        grades = {
            'master_grade': self.master_grade.to_dict() if self.master_grade else None,
            'shot_grades': {
                str(k): v.to_dict() for k, v in self.shot_grades.items()
            },
            'genre': self.genre,
            'color_palette': self.get_color_palette(),
            'exported_at': datetime.utcnow().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(grades, f, indent=2)

        return output_path

    def get_ffmpeg_color_args(self, grade: Optional[GradeSpec] = None) -> str:
        """Generate FFmpeg color correction arguments."""
        g = grade or self.master_grade
        if not g:
            return ""

        # Build filter chain
        filters = []

        # Contrast and saturation
        filters.append(f"eq=contrast={g.contrast}:saturation={g.saturation}")

        # Color temperature (approximate with colorbalance)
        if g.temperature != 0:
            r_shift = g.temperature / 200  # Normalize to -0.5 to 0.5
            b_shift = -r_shift
            filters.append(f"colorbalance=rs={r_shift}:bs={b_shift}")

        # Film grain (using noise filter)
        if g.film_grain > 0:
            strength = int(g.film_grain * 20)
            filters.append(f"noise=alls={strength}:allf=t")

        # Vignette
        if g.vignette > 0:
            filters.append(f"vignette=PI/{4 - g.vignette * 2}")

        return ",".join(filters)

    def generate_prompt_color_hints(self, grade: Optional[GradeSpec] = None) -> str:
        """Generate color hints for AI image generation prompts."""
        g = grade or self.master_grade
        if not g:
            return ""

        hints = []

        # Look style
        style_hints = {
            LookStyle.BLOCKBUSTER: "cinematic orange and teal color grading, high contrast",
            LookStyle.INDIE: "muted natural colors, soft contrast, film-like",
            LookStyle.VINTAGE: "warm vintage tones, faded look, golden hues",
            LookStyle.NEON: "vibrant neon colors, cyan and magenta, high saturation",
            LookStyle.NOIR: "black and white or desaturated, high contrast, dramatic shadows",
            LookStyle.NATURAL: "natural colors, neutral grading",
            LookStyle.DREAM: "soft ethereal glow, lifted shadows, pastel tones",
            LookStyle.GRITTY: "harsh contrast, crushed blacks, film grain, raw look",
            LookStyle.PASTEL: "soft pastel colors, low contrast, lifted blacks",
            LookStyle.MOODY: "deep shadows, selective desaturation, atmospheric"
        }
        hints.append(style_hints.get(g.look_style, ""))

        # Temperature
        if g.temperature > 10:
            hints.append("warm color temperature, golden hour light")
        elif g.temperature < -10:
            hints.append("cool color temperature, blue hour light")

        # Film grain
        if g.film_grain > 0.2:
            hints.append("visible film grain, analog texture")

        return ", ".join(filter(None, hints))
