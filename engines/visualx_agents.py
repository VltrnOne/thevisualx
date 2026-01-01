"""
VISUALX Multi-Agent Architecture
Powered by VLTRN

The 5 Core Creative Agents:
- THE CINEMATOGRAPHER™ - Visual intelligence, shot design, camera psychology
- THE EDITOR™ - Pacing, rhythm, narrative assembly
- THE COLORIST™ - Color grading, mood, visual consistency
- THE STORYBOARD ARTIST™ - Scene visualization, composition planning
- THE DELIVERY ENGINEER™ - Platform optimization, format compliance
"""

import os
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime

# ============================================================
# Enums and Types
# ============================================================

class ShotType(Enum):
    EXTREME_WIDE = "extreme_wide"
    WIDE = "wide"
    MEDIUM_WIDE = "medium_wide"
    MEDIUM = "medium"
    MEDIUM_CLOSE = "medium_close"
    CLOSE_UP = "close_up"
    EXTREME_CLOSE = "extreme_close"
    INSERT = "insert"
    POV = "pov"
    OVER_SHOULDER = "over_shoulder"


class CameraMovement(Enum):
    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    DOLLY_IN = "dolly_in"
    DOLLY_OUT = "dolly_out"
    TRUCK_LEFT = "truck_left"
    TRUCK_RIGHT = "truck_right"
    CRANE_UP = "crane_up"
    CRANE_DOWN = "crane_down"
    HANDHELD = "handheld"
    STEADICAM = "steadicam"
    DRONE = "drone"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"


class EmotionalTone(Enum):
    EUPHORIC = "euphoric"
    MELANCHOLIC = "melancholic"
    AGGRESSIVE = "aggressive"
    SERENE = "serene"
    MYSTERIOUS = "mysterious"
    ROMANTIC = "romantic"
    DARK = "dark"
    TRIUMPHANT = "triumphant"
    ANXIOUS = "anxious"
    NOSTALGIC = "nostalgic"


class Platform(Enum):
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    YOUTUBE_SHORTS = "youtube_shorts"
    INSTAGRAM_REELS = "instagram_reels"
    INSTAGRAM_FEED = "instagram_feed"
    THEATRICAL = "theatrical"
    STREAMING_4K = "streaming_4k"
    BROADCAST = "broadcast"


# ============================================================
# Data Classes
# ============================================================

@dataclass
class ShotSpec:
    """Specification for a single shot."""
    shot_type: ShotType
    camera_movement: CameraMovement
    duration: float  # seconds
    description: str
    emotional_tone: EmotionalTone
    lighting_notes: str = ""
    composition_notes: str = ""
    focal_length: str = "50mm"
    depth_of_field: str = "medium"

    def to_dict(self) -> Dict:
        return {
            'shot_type': self.shot_type.value,
            'camera_movement': self.camera_movement.value,
            'duration': self.duration,
            'description': self.description,
            'emotional_tone': self.emotional_tone.value,
            'lighting_notes': self.lighting_notes,
            'composition_notes': self.composition_notes,
            'focal_length': self.focal_length,
            'depth_of_field': self.depth_of_field
        }


@dataclass
class ColorPalette:
    """Color grading specifications."""
    primary_hue: str
    secondary_hue: str
    shadow_color: str = "#1a1a2e"
    highlight_color: str = "#ffeaa7"
    saturation: float = 1.0
    contrast: float = 1.0
    temperature: str = "neutral"  # warm, cool, neutral
    style: str = "cinematic"  # cinematic, vintage, modern, neon, natural

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EditDecision:
    """Edit decision for a cut point."""
    timestamp: float
    cut_type: str  # cut, dissolve, fade, wipe, match_cut
    duration: float = 0.0  # for transitions
    motivation: str = ""
    beat_aligned: bool = True

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DeliverySpec:
    """Platform-specific delivery specifications."""
    platform: Platform
    resolution: Tuple[int, int]
    fps: int
    codec: str
    bitrate: str
    aspect_ratio: str
    max_duration: Optional[int] = None
    safe_zones: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'platform': self.platform.value,
            'resolution': list(self.resolution),
            'fps': self.fps,
            'codec': self.codec,
            'bitrate': self.bitrate,
            'aspect_ratio': self.aspect_ratio,
            'max_duration': self.max_duration,
            'safe_zones': self.safe_zones
        }


# ============================================================
# THE CINEMATOGRAPHER™
# ============================================================

class TheCinematographer:
    """
    THE CINEMATOGRAPHER™ - Visual Intelligence Agent

    Responsibilities:
    - Shot design and camera movement planning
    - Visual storytelling through framing
    - Lighting direction and mood
    - Lens selection and depth of field
    """

    GENRE_SHOT_PROFILES = {
        'hip-hop': {
            'preferred_shots': [ShotType.MEDIUM, ShotType.CLOSE_UP, ShotType.WIDE],
            'camera_style': [CameraMovement.HANDHELD, CameraMovement.DOLLY_IN, CameraMovement.TRUCK_LEFT],
            'pacing': 'fast',
            'avg_shot_duration': 2.5
        },
        'electronic': {
            'preferred_shots': [ShotType.EXTREME_WIDE, ShotType.EXTREME_CLOSE, ShotType.MEDIUM],
            'camera_style': [CameraMovement.STEADICAM, CameraMovement.DRONE, CameraMovement.ZOOM_IN],
            'pacing': 'synced',
            'avg_shot_duration': 3.0
        },
        'r&b': {
            'preferred_shots': [ShotType.CLOSE_UP, ShotType.MEDIUM_CLOSE, ShotType.OVER_SHOULDER],
            'camera_style': [CameraMovement.DOLLY_IN, CameraMovement.CRANE_UP, CameraMovement.STEADICAM],
            'pacing': 'smooth',
            'avg_shot_duration': 4.0
        },
        'rock': {
            'preferred_shots': [ShotType.WIDE, ShotType.MEDIUM, ShotType.INSERT],
            'camera_style': [CameraMovement.HANDHELD, CameraMovement.PAN_LEFT, CameraMovement.CRANE_DOWN],
            'pacing': 'energetic',
            'avg_shot_duration': 2.0
        },
        'pop': {
            'preferred_shots': [ShotType.MEDIUM, ShotType.CLOSE_UP, ShotType.WIDE],
            'camera_style': [CameraMovement.STEADICAM, CameraMovement.DOLLY_IN, CameraMovement.TILT_UP],
            'pacing': 'dynamic',
            'avg_shot_duration': 3.0
        },
        'ambient': {
            'preferred_shots': [ShotType.EXTREME_WIDE, ShotType.WIDE, ShotType.INSERT],
            'camera_style': [CameraMovement.STATIC, CameraMovement.DRONE, CameraMovement.CRANE_UP],
            'pacing': 'contemplative',
            'avg_shot_duration': 6.0
        }
    }

    ENERGY_TO_TONE = {
        'high': [EmotionalTone.EUPHORIC, EmotionalTone.AGGRESSIVE, EmotionalTone.TRIUMPHANT],
        'medium': [EmotionalTone.MYSTERIOUS, EmotionalTone.ROMANTIC, EmotionalTone.NOSTALGIC],
        'low': [EmotionalTone.MELANCHOLIC, EmotionalTone.SERENE, EmotionalTone.DARK]
    }

    def __init__(self, genre: str = "electronic", style: str = "cinematic"):
        self.genre = genre.lower()
        self.style = style
        self.shot_history: List[ShotSpec] = []

    def design_shot(self,
                    energy_level: float,
                    beat_position: str,  # verse, chorus, bridge, drop, intro, outro
                    duration: float = 5.0,
                    context: str = "") -> ShotSpec:
        """Design a shot based on musical and narrative context."""

        profile = self.GENRE_SHOT_PROFILES.get(self.genre, self.GENRE_SHOT_PROFILES['pop'])

        # Select shot type based on beat position
        if beat_position in ['chorus', 'drop']:
            shot_type = profile['preferred_shots'][0]  # Wide for impact
        elif beat_position in ['verse']:
            shot_type = profile['preferred_shots'][1]  # Medium/Close for intimacy
        else:
            shot_type = profile['preferred_shots'][-1]  # Variety for transitions

        # Select camera movement based on energy
        if energy_level > 0.7:
            movement = profile['camera_style'][0]
        elif energy_level > 0.4:
            movement = profile['camera_style'][1]
        else:
            movement = CameraMovement.STATIC

        # Determine emotional tone
        if energy_level > 0.7:
            tone = self.ENERGY_TO_TONE['high'][0]
        elif energy_level > 0.4:
            tone = self.ENERGY_TO_TONE['medium'][0]
        else:
            tone = self.ENERGY_TO_TONE['low'][0]

        # Generate description
        description = self._generate_shot_description(shot_type, movement, tone, context)

        # Determine technical specs
        focal_length = self._select_focal_length(shot_type, tone)
        dof = "shallow" if shot_type in [ShotType.CLOSE_UP, ShotType.EXTREME_CLOSE] else "medium"

        shot = ShotSpec(
            shot_type=shot_type,
            camera_movement=movement,
            duration=duration,
            description=description,
            emotional_tone=tone,
            lighting_notes=self._generate_lighting_notes(tone, energy_level),
            composition_notes=self._generate_composition_notes(shot_type),
            focal_length=focal_length,
            depth_of_field=dof
        )

        self.shot_history.append(shot)
        return shot

    def _generate_shot_description(self, shot_type: ShotType, movement: CameraMovement,
                                   tone: EmotionalTone, context: str) -> str:
        """Generate a cinematic shot description."""
        templates = {
            ShotType.EXTREME_WIDE: "Vast landscape establishing scale and atmosphere",
            ShotType.WIDE: "Wide composition capturing the full scene",
            ShotType.MEDIUM: "Medium framing balancing subject and environment",
            ShotType.CLOSE_UP: "Intimate close-up revealing emotion and detail",
            ShotType.EXTREME_CLOSE: "Extreme close-up abstracting form and texture",
            ShotType.INSERT: "Detail insert emphasizing symbolic element"
        }

        base = templates.get(shot_type, "Composed shot")
        movement_desc = movement.value.replace('_', ' ')

        return f"{base}, {movement_desc} movement, {tone.value} mood. {context}"

    def _select_focal_length(self, shot_type: ShotType, tone: EmotionalTone) -> str:
        """Select appropriate focal length for the shot."""
        focal_map = {
            ShotType.EXTREME_WIDE: "16mm",
            ShotType.WIDE: "24mm",
            ShotType.MEDIUM_WIDE: "35mm",
            ShotType.MEDIUM: "50mm",
            ShotType.MEDIUM_CLOSE: "85mm",
            ShotType.CLOSE_UP: "100mm",
            ShotType.EXTREME_CLOSE: "135mm"
        }
        return focal_map.get(shot_type, "50mm")

    def _generate_lighting_notes(self, tone: EmotionalTone, energy: float) -> str:
        """Generate lighting direction notes."""
        lighting_styles = {
            EmotionalTone.EUPHORIC: "High key, motivated practical sources, golden hour warmth",
            EmotionalTone.MELANCHOLIC: "Low key, soft shadows, blue hour tones",
            EmotionalTone.AGGRESSIVE: "High contrast, hard shadows, stark backlighting",
            EmotionalTone.SERENE: "Soft diffused light, even fill, natural tones",
            EmotionalTone.MYSTERIOUS: "Silhouettes, rim lighting, negative fill",
            EmotionalTone.DARK: "Minimal key, deep shadows, single source"
        }
        return lighting_styles.get(tone, "Balanced three-point setup")

    def _generate_composition_notes(self, shot_type: ShotType) -> str:
        """Generate composition guidelines."""
        return f"Rule of thirds, lead room for movement, {shot_type.value} framing conventions"

    def generate_shot_list(self, duration: float, bpm: float, sections: List[Dict]) -> List[ShotSpec]:
        """Generate a complete shot list for a sequence."""
        shot_list = []
        beat_duration = 60.0 / bpm

        for section in sections:
            section_shots = self._plan_section_shots(
                section.get('type', 'verse'),
                section.get('start', 0),
                section.get('duration', 10),
                section.get('energy', 0.5),
                beat_duration
            )
            shot_list.extend(section_shots)

        return shot_list

    def _plan_section_shots(self, section_type: str, start: float,
                           duration: float, energy: float, beat_duration: float) -> List[ShotSpec]:
        """Plan shots for a specific section."""
        profile = self.GENRE_SHOT_PROFILES.get(self.genre, self.GENRE_SHOT_PROFILES['pop'])
        avg_duration = profile['avg_shot_duration']

        # Adjust for energy
        if energy > 0.7:
            avg_duration *= 0.7  # Faster cuts for high energy
        elif energy < 0.3:
            avg_duration *= 1.5  # Slower for low energy

        num_shots = max(1, int(duration / avg_duration))
        shots = []

        for i in range(num_shots):
            shot_duration = min(avg_duration, duration - sum(s.duration for s in shots))
            if shot_duration <= 0:
                break

            shot = self.design_shot(
                energy_level=energy,
                beat_position=section_type,
                duration=shot_duration,
                context=f"Section: {section_type}, Shot {i+1}/{num_shots}"
            )
            shots.append(shot)

        return shots


# ============================================================
# THE EDITOR™
# ============================================================

class TheEditor:
    """
    THE EDITOR™ - Rhythm & Assembly Agent

    Responsibilities:
    - Pacing and rhythm alignment
    - Cut timing and beat synchronization
    - Narrative flow and continuity
    - Transition selection
    """

    TRANSITION_TYPES = {
        'cut': {'duration': 0, 'use_cases': ['action', 'dialogue', 'fast_pacing']},
        'dissolve': {'duration': 0.5, 'use_cases': ['time_passage', 'dream', 'memory']},
        'fade': {'duration': 1.0, 'use_cases': ['scene_end', 'emotional_pause', 'intro_outro']},
        'wipe': {'duration': 0.3, 'use_cases': ['location_change', 'parallel_action']},
        'match_cut': {'duration': 0, 'use_cases': ['visual_connection', 'thematic_link']}
    }

    def __init__(self, style: str = "dynamic"):
        self.style = style
        self.edit_decisions: List[EditDecision] = []
        self.cut_points: List[float] = []

    def analyze_rhythm(self, beats: List[float], energy_curve: List[float]) -> Dict:
        """Analyze the rhythmic structure for editing."""
        return {
            'beat_count': len(beats),
            'avg_beat_interval': sum(b2 - b1 for b1, b2 in zip(beats[:-1], beats[1:])) / max(1, len(beats) - 1) if len(beats) > 1 else 0,
            'energy_peaks': [i for i, e in enumerate(energy_curve) if e > 0.8],
            'recommended_cuts_per_minute': self._calculate_cut_rate(energy_curve)
        }

    def _calculate_cut_rate(self, energy_curve: List[float]) -> float:
        """Calculate recommended cuts per minute based on energy."""
        avg_energy = sum(energy_curve) / len(energy_curve) if energy_curve else 0.5

        if avg_energy > 0.7:
            return 24  # Fast-paced: 24 cuts/min (2.5s avg shot)
        elif avg_energy > 0.4:
            return 15  # Medium: 15 cuts/min (4s avg shot)
        else:
            return 8   # Slow: 8 cuts/min (7.5s avg shot)

    def generate_edit_decision_list(self,
                                    beats: List[float],
                                    shots: List[ShotSpec],
                                    energy_curve: List[float]) -> List[EditDecision]:
        """Generate edit decisions synchronized to beats."""
        decisions = []
        current_time = 0

        for i, shot in enumerate(shots):
            # Find nearest beat for cut point
            cut_time = self._find_nearest_beat(current_time + shot.duration, beats)

            # Select transition type
            transition = self._select_transition(
                i, len(shots),
                energy_curve[min(int(cut_time), len(energy_curve)-1)] if energy_curve else 0.5
            )

            decision = EditDecision(
                timestamp=cut_time,
                cut_type=transition,
                duration=self.TRANSITION_TYPES[transition]['duration'],
                motivation=f"Beat-synced cut to shot {i+1}",
                beat_aligned=True
            )
            decisions.append(decision)
            current_time = cut_time

        self.edit_decisions = decisions
        return decisions

    def _find_nearest_beat(self, target_time: float, beats: List[float]) -> float:
        """Find the nearest beat to a target timestamp."""
        if not beats:
            return target_time

        nearest = min(beats, key=lambda b: abs(b - target_time))
        return nearest

    def _select_transition(self, shot_index: int, total_shots: int, energy: float) -> str:
        """Select appropriate transition type."""
        # First and last shots get fades
        if shot_index == 0:
            return 'fade'
        if shot_index == total_shots - 1:
            return 'fade'

        # High energy = hard cuts
        if energy > 0.7:
            return 'cut'

        # Medium energy = mix
        if energy > 0.4:
            return 'cut' if shot_index % 3 != 0 else 'dissolve'

        # Low energy = softer transitions
        return 'dissolve'

    def export_edl(self, output_path: str) -> str:
        """Export Edit Decision List in CMX3600 format."""
        edl_content = "TITLE: VISUALX_SEQUENCE\nFCM: NON-DROP FRAME\n\n"

        for i, decision in enumerate(self.edit_decisions, 1):
            tc_in = self._frames_to_timecode(int(decision.timestamp * 24))
            tc_out = self._frames_to_timecode(int((decision.timestamp + decision.duration) * 24))

            edl_content += f"{i:03d}  001  V     C        {tc_in} {tc_out} {tc_in} {tc_out}\n"
            edl_content += f"* {decision.motivation}\n\n"

        with open(output_path, 'w') as f:
            f.write(edl_content)

        return output_path

    def _frames_to_timecode(self, frames: int, fps: int = 24) -> str:
        """Convert frame count to SMPTE timecode."""
        total_seconds = frames // fps
        remaining_frames = frames % fps
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{remaining_frames:02d}"


# ============================================================
# THE COLORIST™
# ============================================================

class TheColorist:
    """
    THE COLORIST™ - Visual Grading Agent

    Responsibilities:
    - Color palette design
    - Mood and atmosphere through color
    - Visual consistency across shots
    - Platform-specific color optimization
    """

    MOOD_PALETTES = {
        EmotionalTone.EUPHORIC: ColorPalette(
            primary_hue="#ffd700", secondary_hue="#ff6b6b",
            temperature="warm", saturation=1.2, contrast=1.1, style="modern"
        ),
        EmotionalTone.MELANCHOLIC: ColorPalette(
            primary_hue="#5f6caf", secondary_hue="#3d4f7c",
            temperature="cool", saturation=0.8, contrast=1.0, style="cinematic"
        ),
        EmotionalTone.AGGRESSIVE: ColorPalette(
            primary_hue="#ff4444", secondary_hue="#1a1a1a",
            temperature="neutral", saturation=1.3, contrast=1.4, style="modern"
        ),
        EmotionalTone.SERENE: ColorPalette(
            primary_hue="#87ceeb", secondary_hue="#98d8c8",
            temperature="cool", saturation=0.9, contrast=0.9, style="natural"
        ),
        EmotionalTone.MYSTERIOUS: ColorPalette(
            primary_hue="#4a0080", secondary_hue="#1a0033",
            temperature="cool", saturation=1.0, contrast=1.2, style="cinematic"
        ),
        EmotionalTone.DARK: ColorPalette(
            primary_hue="#1a1a2e", secondary_hue="#0f0f1a",
            temperature="cool", saturation=0.7, contrast=1.3, style="cinematic"
        ),
        EmotionalTone.TRIUMPHANT: ColorPalette(
            primary_hue="#ffc107", secondary_hue="#ff5722",
            temperature="warm", saturation=1.3, contrast=1.2, style="modern"
        ),
        EmotionalTone.NOSTALGIC: ColorPalette(
            primary_hue="#d4a373", secondary_hue="#ccd5ae",
            temperature="warm", saturation=0.85, contrast=0.95, style="vintage"
        )
    }

    GENRE_STYLES = {
        'hip-hop': {'contrast': 1.2, 'saturation': 1.1, 'style': 'modern'},
        'electronic': {'contrast': 1.3, 'saturation': 1.2, 'style': 'neon'},
        'r&b': {'contrast': 1.0, 'saturation': 0.9, 'style': 'cinematic'},
        'rock': {'contrast': 1.4, 'saturation': 1.1, 'style': 'modern'},
        'pop': {'contrast': 1.1, 'saturation': 1.2, 'style': 'modern'},
        'ambient': {'contrast': 0.9, 'saturation': 0.8, 'style': 'natural'}
    }

    def __init__(self, genre: str = "electronic"):
        self.genre = genre.lower()
        self.master_palette: Optional[ColorPalette] = None
        self.shot_grades: Dict[int, ColorPalette] = {}

    def design_master_palette(self, emotional_tone: EmotionalTone,
                             custom_colors: Optional[Dict] = None) -> ColorPalette:
        """Design the master color palette for the project."""
        base_palette = self.MOOD_PALETTES.get(emotional_tone, self.MOOD_PALETTES[EmotionalTone.SERENE])
        genre_style = self.GENRE_STYLES.get(self.genre, self.GENRE_STYLES['pop'])

        # Apply genre adjustments
        palette = ColorPalette(
            primary_hue=custom_colors.get('primary', base_palette.primary_hue) if custom_colors else base_palette.primary_hue,
            secondary_hue=custom_colors.get('secondary', base_palette.secondary_hue) if custom_colors else base_palette.secondary_hue,
            shadow_color=base_palette.shadow_color,
            highlight_color=base_palette.highlight_color,
            saturation=base_palette.saturation * genre_style['saturation'],
            contrast=base_palette.contrast * genre_style['contrast'],
            temperature=base_palette.temperature,
            style=genre_style['style']
        )

        self.master_palette = palette
        return palette

    def grade_shot(self, shot_index: int, shot_spec: ShotSpec,
                   override: Optional[Dict] = None) -> ColorPalette:
        """Generate color grade for a specific shot."""
        if not self.master_palette:
            self.design_master_palette(shot_spec.emotional_tone)

        # Start with master palette
        shot_palette = ColorPalette(
            primary_hue=self.master_palette.primary_hue,
            secondary_hue=self.master_palette.secondary_hue,
            shadow_color=self.master_palette.shadow_color,
            highlight_color=self.master_palette.highlight_color,
            saturation=self.master_palette.saturation,
            contrast=self.master_palette.contrast,
            temperature=self.master_palette.temperature,
            style=self.master_palette.style
        )

        # Adjust based on shot's emotional tone if different from master
        shot_mood = self.MOOD_PALETTES.get(shot_spec.emotional_tone)
        if shot_mood:
            shot_palette.temperature = shot_mood.temperature

        # Apply overrides
        if override:
            for key, value in override.items():
                if hasattr(shot_palette, key):
                    setattr(shot_palette, key, value)

        self.shot_grades[shot_index] = shot_palette
        return shot_palette

    def export_lut_instructions(self, output_path: str) -> str:
        """Export color grading instructions (LUT generation guide)."""
        instructions = {
            'master_palette': self.master_palette.to_dict() if self.master_palette else None,
            'shot_grades': {k: v.to_dict() for k, v in self.shot_grades.items()},
            'generation_notes': [
                "Apply master palette as base grade",
                "Use shot-specific grades for scene variations",
                "Maintain consistent shadow/highlight colors for cohesion",
                "Adjust saturation curves for skin tones if needed"
            ]
        }

        with open(output_path, 'w') as f:
            json.dump(instructions, f, indent=2)

        return output_path


# ============================================================
# THE STORYBOARD ARTIST™
# ============================================================

class TheStoryboardArtist:
    """
    THE STORYBOARD ARTIST™ - Visual Planning Agent

    Responsibilities:
    - Scene visualization and composition
    - Visual narrative planning
    - Reference gathering and mood boards
    - Shot sequence planning
    """

    def __init__(self):
        self.scenes: List[Dict] = []
        self.mood_board: List[str] = []
        self.visual_references: List[str] = []

    def create_scene(self,
                    description: str,
                    shots: List[ShotSpec],
                    narrative_purpose: str,
                    visual_theme: str) -> Dict:
        """Create a scene breakdown for storyboarding."""
        scene = {
            'id': len(self.scenes) + 1,
            'description': description,
            'shots': [s.to_dict() for s in shots],
            'narrative_purpose': narrative_purpose,
            'visual_theme': visual_theme,
            'panel_count': len(shots),
            'created_at': datetime.utcnow().isoformat()
        }

        self.scenes.append(scene)
        return scene

    def generate_prompt_sequence(self, shots: List[ShotSpec],
                                style: str = "cinematic") -> List[str]:
        """Generate AI image prompts for storyboard panels."""
        prompts = []

        for i, shot in enumerate(shots):
            prompt = self._build_visual_prompt(shot, style, i, len(shots))
            prompts.append(prompt)

        return prompts

    def _build_visual_prompt(self, shot: ShotSpec, style: str,
                            index: int, total: int) -> str:
        """Build a detailed prompt for AI image generation."""
        components = [
            f"{style} photography",
            shot.description,
            f"{shot.shot_type.value.replace('_', ' ')} shot",
            f"{shot.focal_length} lens",
            f"{shot.depth_of_field} depth of field",
            shot.lighting_notes,
            f"{shot.emotional_tone.value} mood",
            "professional cinematography",
            "high production value",
            "8K resolution"
        ]

        return ", ".join(filter(None, components))

    def export_storyboard(self, output_path: str) -> str:
        """Export storyboard as JSON."""
        storyboard = {
            'scenes': self.scenes,
            'mood_board': self.mood_board,
            'visual_references': self.visual_references,
            'total_panels': sum(s['panel_count'] for s in self.scenes),
            'exported_at': datetime.utcnow().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(storyboard, f, indent=2)

        return output_path


# ============================================================
# THE DELIVERY ENGINEER™
# ============================================================

class TheDeliveryEngineer:
    """
    THE DELIVERY ENGINEER™ - Platform Optimization Agent

    Responsibilities:
    - Platform-specific formatting
    - Codec and bitrate optimization
    - Safe zone compliance
    - Multi-platform delivery packaging
    """

    PLATFORM_SPECS = {
        Platform.TIKTOK: DeliverySpec(
            platform=Platform.TIKTOK,
            resolution=(1080, 1920),
            fps=30,
            codec="h264",
            bitrate="8M",
            aspect_ratio="9:16",
            max_duration=180,
            safe_zones={'top': 150, 'bottom': 200}
        ),
        Platform.YOUTUBE: DeliverySpec(
            platform=Platform.YOUTUBE,
            resolution=(1920, 1080),
            fps=30,
            codec="h264",
            bitrate="12M",
            aspect_ratio="16:9"
        ),
        Platform.YOUTUBE_SHORTS: DeliverySpec(
            platform=Platform.YOUTUBE_SHORTS,
            resolution=(1080, 1920),
            fps=30,
            codec="h264",
            bitrate="8M",
            aspect_ratio="9:16",
            max_duration=60
        ),
        Platform.INSTAGRAM_REELS: DeliverySpec(
            platform=Platform.INSTAGRAM_REELS,
            resolution=(1080, 1920),
            fps=30,
            codec="h264",
            bitrate="8M",
            aspect_ratio="9:16",
            max_duration=90
        ),
        Platform.INSTAGRAM_FEED: DeliverySpec(
            platform=Platform.INSTAGRAM_FEED,
            resolution=(1080, 1080),
            fps=30,
            codec="h264",
            bitrate="6M",
            aspect_ratio="1:1",
            max_duration=60
        ),
        Platform.THEATRICAL: DeliverySpec(
            platform=Platform.THEATRICAL,
            resolution=(4096, 2160),
            fps=24,
            codec="prores",
            bitrate="200M",
            aspect_ratio="1.85:1"
        ),
        Platform.STREAMING_4K: DeliverySpec(
            platform=Platform.STREAMING_4K,
            resolution=(3840, 2160),
            fps=24,
            codec="h265",
            bitrate="25M",
            aspect_ratio="16:9"
        ),
        Platform.BROADCAST: DeliverySpec(
            platform=Platform.BROADCAST,
            resolution=(1920, 1080),
            fps=29.97,
            codec="prores",
            bitrate="45M",
            aspect_ratio="16:9"
        )
    }

    def __init__(self):
        self.delivery_packages: List[Dict] = []

    def get_spec(self, platform: Platform) -> DeliverySpec:
        """Get delivery specifications for a platform."""
        return self.PLATFORM_SPECS.get(platform, self.PLATFORM_SPECS[Platform.YOUTUBE])

    def create_delivery_package(self,
                               source_path: str,
                               platforms: List[Platform],
                               output_dir: str) -> List[Dict]:
        """Create delivery packages for multiple platforms."""
        packages = []

        for platform in platforms:
            spec = self.get_spec(platform)
            package = {
                'platform': platform.value,
                'spec': spec.to_dict(),
                'source': source_path,
                'output_path': os.path.join(output_dir, f"{platform.value}_delivery.mp4"),
                'status': 'pending',
                'ffmpeg_command': self._generate_ffmpeg_command(source_path, spec, output_dir)
            }
            packages.append(package)

        self.delivery_packages = packages
        return packages

    def _generate_ffmpeg_command(self, source: str, spec: DeliverySpec, output_dir: str) -> str:
        """Generate FFmpeg command for platform encoding."""
        output = os.path.join(output_dir, f"{spec.platform.value}_delivery.mp4")

        # Base command
        cmd = f'ffmpeg -i "{source}"'

        # Video codec
        if spec.codec == "h264":
            cmd += f' -c:v libx264 -preset slow -crf 18'
        elif spec.codec == "h265":
            cmd += f' -c:v libx265 -preset slow -crf 20'
        elif spec.codec == "prores":
            cmd += f' -c:v prores_ks -profile:v 3'

        # Resolution and FPS
        cmd += f' -vf "scale={spec.resolution[0]}:{spec.resolution[1]},fps={spec.fps}"'

        # Bitrate
        cmd += f' -b:v {spec.bitrate}'

        # Audio
        cmd += ' -c:a aac -b:a 256k'

        # Output
        cmd += f' "{output}"'

        return cmd

    def validate_delivery(self, file_path: str, platform: Platform) -> Dict:
        """Validate a file against platform requirements."""
        spec = self.get_spec(platform)

        # In production, this would use ffprobe to check actual file specs
        validation = {
            'platform': platform.value,
            'file': file_path,
            'spec_required': spec.to_dict(),
            'validation_status': 'pending',
            'notes': "Run ffprobe for actual validation"
        }

        return validation

    def export_delivery_manifest(self, output_path: str) -> str:
        """Export delivery manifest with all package details."""
        manifest = {
            'packages': self.delivery_packages,
            'generated_at': datetime.utcnow().isoformat(),
            'version': '1.0'
        }

        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        return output_path


# ============================================================
# VISUALX ORCHESTRATOR
# ============================================================

class VISUALXOrchestrator:
    """
    Main orchestrator that coordinates all VISUALX agents.
    """

    def __init__(self, genre: str = "electronic", style: str = "cinematic"):
        self.genre = genre
        self.style = style

        # Initialize all agents
        self.cinematographer = TheCinematographer(genre=genre, style=style)
        self.editor = TheEditor(style=style)
        self.colorist = TheColorist(genre=genre)
        self.storyboard_artist = TheStoryboardArtist()
        self.delivery_engineer = TheDeliveryEngineer()

        # Project state
        self.project_data: Dict[str, Any] = {}

    def create_visual_package(self,
                             title: str,
                             audio_analysis: Dict,
                             target_platforms: List[Platform],
                             output_dir: str) -> Dict:
        """
        Create a complete visual package using all agents.

        This is the main entry point for the VISUALX pipeline.
        """

        # Extract audio data
        bpm = audio_analysis.get('bpm', 120)
        sections = audio_analysis.get('sections', [])
        beats = audio_analysis.get('beats', [])
        energy_curve = audio_analysis.get('energy_curve', [0.5])
        duration = audio_analysis.get('duration', 180)

        # 1. CINEMATOGRAPHER: Design shots
        shot_list = self.cinematographer.generate_shot_list(duration, bpm, sections)

        # 2. EDITOR: Create edit decisions
        edit_decisions = self.editor.generate_edit_decision_list(beats, shot_list, energy_curve)

        # 3. COLORIST: Design color palette
        dominant_tone = self._determine_dominant_tone(energy_curve)
        master_palette = self.colorist.design_master_palette(dominant_tone)

        # Grade each shot
        for i, shot in enumerate(shot_list):
            self.colorist.grade_shot(i, shot)

        # 4. STORYBOARD: Create visual plans
        prompts = self.storyboard_artist.generate_prompt_sequence(shot_list, self.style)

        # 5. DELIVERY: Package for platforms
        delivery_packages = self.delivery_engineer.create_delivery_package(
            source_path="",  # Will be filled after render
            platforms=target_platforms,
            output_dir=output_dir
        )

        # Compile result
        visual_package = {
            'title': title,
            'genre': self.genre,
            'style': self.style,
            'shots': [s.to_dict() for s in shot_list],
            'edit_decisions': [e.to_dict() for e in edit_decisions],
            'color_palette': master_palette.to_dict(),
            'shot_grades': {k: v.to_dict() for k, v in self.colorist.shot_grades.items()},
            'prompts': prompts,
            'delivery_packages': delivery_packages,
            'metadata': {
                'bpm': bpm,
                'duration': duration,
                'total_shots': len(shot_list),
                'created_at': datetime.utcnow().isoformat()
            }
        }

        # Save package
        package_path = os.path.join(output_dir, 'visual_package.json')
        with open(package_path, 'w') as f:
            json.dump(visual_package, f, indent=2)

        self.project_data = visual_package
        return visual_package

    def _determine_dominant_tone(self, energy_curve: List[float]) -> EmotionalTone:
        """Determine the dominant emotional tone from energy curve."""
        if not energy_curve:
            return EmotionalTone.SERENE

        avg_energy = sum(energy_curve) / len(energy_curve)

        if avg_energy > 0.7:
            return EmotionalTone.EUPHORIC
        elif avg_energy > 0.5:
            return EmotionalTone.TRIUMPHANT
        elif avg_energy > 0.3:
            return EmotionalTone.MYSTERIOUS
        else:
            return EmotionalTone.MELANCHOLIC

    def get_next_prompt(self, shot_index: int) -> Optional[str]:
        """Get the AI generation prompt for a specific shot."""
        if 'prompts' in self.project_data and shot_index < len(self.project_data['prompts']):
            return self.project_data['prompts'][shot_index]
        return None

    def export_all(self, output_dir: str) -> Dict[str, str]:
        """Export all project files."""
        exports = {}

        # EDL
        edl_path = os.path.join(output_dir, 'edit_decision_list.edl')
        self.editor.export_edl(edl_path)
        exports['edl'] = edl_path

        # Color instructions
        color_path = os.path.join(output_dir, 'color_instructions.json')
        self.colorist.export_lut_instructions(color_path)
        exports['color'] = color_path

        # Storyboard
        storyboard_path = os.path.join(output_dir, 'storyboard.json')
        self.storyboard_artist.export_storyboard(storyboard_path)
        exports['storyboard'] = storyboard_path

        # Delivery manifest
        manifest_path = os.path.join(output_dir, 'delivery_manifest.json')
        self.delivery_engineer.export_delivery_manifest(manifest_path)
        exports['delivery'] = manifest_path

        return exports
