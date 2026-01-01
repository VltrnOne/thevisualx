"""
ShotBrain™ - AI Shot Designer
Powered by VLTRN / VISUALX

Advanced shot planning and cinematography intelligence module.
Handles dynamic shot selection, camera psychology, and visual storytelling.
"""

import os
import json
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

from visualx_agents import (
    ShotType, CameraMovement, EmotionalTone,
    ShotSpec, TheCinematographer
)


# ============================================================
# Camera Psychology Rules
# ============================================================

class CameraPsychology:
    """
    Rules engine for camera psychology and viewer manipulation.
    Based on established cinematography principles.
    """

    # Angle Psychology
    ANGLE_EFFECTS = {
        'low_angle': {
            'effect': 'power, dominance, importance',
            'use_for': ['authority', 'heroism', 'intimidation'],
            'tilt_range': (-15, -5)
        },
        'high_angle': {
            'effect': 'vulnerability, weakness, insignificance',
            'use_for': ['submission', 'sadness', 'overview'],
            'tilt_range': (5, 15)
        },
        'eye_level': {
            'effect': 'equality, neutrality, connection',
            'use_for': ['dialogue', 'intimacy', 'trust'],
            'tilt_range': (-2, 2)
        },
        'dutch_angle': {
            'effect': 'unease, tension, disorientation',
            'use_for': ['horror', 'confusion', 'drama'],
            'roll_range': (10, 25)
        },
        'birds_eye': {
            'effect': 'omniscience, isolation, fate',
            'use_for': ['establishing', 'isolation', 'scope'],
            'tilt_range': (75, 90)
        },
        'worms_eye': {
            'effect': 'extreme power, godlike, overwhelming',
            'use_for': ['monuments', 'giants', 'oppression'],
            'tilt_range': (-75, -45)
        }
    }

    # Movement Psychology
    MOVEMENT_EFFECTS = {
        CameraMovement.DOLLY_IN: {
            'effect': 'increasing intensity, focus, revelation',
            'emotional': ['tension', 'intimacy', 'importance']
        },
        CameraMovement.DOLLY_OUT: {
            'effect': 'revelation of context, isolation, conclusion',
            'emotional': ['loneliness', 'scale', 'departure']
        },
        CameraMovement.PAN_LEFT: {
            'effect': 'following natural reading direction, past',
            'emotional': ['memory', 'regression', 'reflection']
        },
        CameraMovement.PAN_RIGHT: {
            'effect': 'progress, future, continuation',
            'emotional': ['hope', 'advancement', 'journey']
        },
        CameraMovement.TILT_UP: {
            'effect': 'hope, aspiration, grandeur',
            'emotional': ['awe', 'freedom', 'triumph']
        },
        CameraMovement.TILT_DOWN: {
            'effect': 'doom, descent, grounding',
            'emotional': ['defeat', 'reality', 'discovery']
        },
        CameraMovement.CRANE_UP: {
            'effect': 'transcendence, liberation, overview',
            'emotional': ['joy', 'release', 'perspective']
        },
        CameraMovement.CRANE_DOWN: {
            'effect': 'arrival, focusing, grounding',
            'emotional': ['attention', 'presence', 'weight']
        },
        CameraMovement.HANDHELD: {
            'effect': 'immediacy, documentary, urgency',
            'emotional': ['chaos', 'reality', 'intimacy']
        },
        CameraMovement.STEADICAM: {
            'effect': 'smooth pursuit, dreamlike, graceful',
            'emotional': ['elegance', 'following', 'fluidity']
        },
        CameraMovement.ZOOM_IN: {
            'effect': 'sudden focus, realization, emphasis',
            'emotional': ['shock', 'importance', 'discovery']
        },
        CameraMovement.ZOOM_OUT: {
            'effect': 'reveal, context, diminishment',
            'emotional': ['scale', 'insignificance', 'overview']
        },
        CameraMovement.STATIC: {
            'effect': 'stability, observation, contemplation',
            'emotional': ['calm', 'patience', 'presence']
        }
    }

    # Focal Length Psychology
    LENS_EFFECTS = {
        '16mm': {
            'effect': 'distortion, immersion, vastness',
            'use_for': ['landscapes', 'environments', 'claustrophobia']
        },
        '24mm': {
            'effect': 'context, slight distortion, scope',
            'use_for': ['establishing', 'groups', 'interiors']
        },
        '35mm': {
            'effect': 'natural perspective, versatile',
            'use_for': ['dialogue', 'walking', 'documentary']
        },
        '50mm': {
            'effect': 'closest to human eye, neutral',
            'use_for': ['portraits', 'narrative', 'intimacy']
        },
        '85mm': {
            'effect': 'flattering compression, isolation',
            'use_for': ['close-ups', 'interviews', 'beauty']
        },
        '135mm': {
            'effect': 'strong compression, voyeuristic',
            'use_for': ['details', 'separation', 'abstraction']
        },
        '200mm+': {
            'effect': 'extreme compression, surveillance',
            'use_for': ['sports', 'wildlife', 'stalking']
        }
    }

    @classmethod
    def get_recommended_setup(cls, emotional_goal: str, energy_level: float) -> Dict:
        """Get recommended camera setup for an emotional goal."""
        # Find matching angle
        recommended_angle = 'eye_level'
        for angle, data in cls.ANGLE_EFFECTS.items():
            if emotional_goal.lower() in [u.lower() for u in data['use_for']]:
                recommended_angle = angle
                break

        # Find matching movement
        recommended_movement = CameraMovement.STATIC
        for movement, data in cls.MOVEMENT_EFFECTS.items():
            if emotional_goal.lower() in [e.lower() for e in data['emotional']]:
                recommended_movement = movement
                break

        # Energy affects speed and stability
        if energy_level > 0.7:
            stability = 'dynamic'
            speed = 'fast'
        elif energy_level > 0.4:
            stability = 'smooth'
            speed = 'medium'
        else:
            stability = 'stable'
            speed = 'slow'

        return {
            'angle': recommended_angle,
            'angle_effect': cls.ANGLE_EFFECTS[recommended_angle]['effect'],
            'movement': recommended_movement,
            'movement_effect': cls.MOVEMENT_EFFECTS[recommended_movement]['effect'],
            'stability': stability,
            'speed': speed,
            'energy_level': energy_level
        }


# ============================================================
# Shot Pattern Engine
# ============================================================

class ShotPatternEngine:
    """
    Engine for recognizing and generating cinematic shot patterns.
    """

    # Classic shot sequences
    PATTERNS = {
        'dialogue_tennis': {
            'description': 'Classic shot-reverse-shot for dialogue',
            'sequence': [
                ShotType.MEDIUM, ShotType.OVER_SHOULDER,
                ShotType.OVER_SHOULDER, ShotType.CLOSE_UP,
                ShotType.CLOSE_UP, ShotType.MEDIUM
            ],
            'use_for': ['conversation', 'interview', 'confrontation']
        },
        'reveal_pattern': {
            'description': 'Building to a dramatic reveal',
            'sequence': [
                ShotType.EXTREME_CLOSE, ShotType.CLOSE_UP,
                ShotType.MEDIUM_CLOSE, ShotType.MEDIUM,
                ShotType.WIDE
            ],
            'use_for': ['mystery', 'introduction', 'discovery']
        },
        'approach_pattern': {
            'description': 'Gradual approach to subject',
            'sequence': [
                ShotType.EXTREME_WIDE, ShotType.WIDE,
                ShotType.MEDIUM, ShotType.CLOSE_UP
            ],
            'use_for': ['journey', 'focus', 'intimacy_building']
        },
        'departure_pattern': {
            'description': 'Pulling away from subject',
            'sequence': [
                ShotType.CLOSE_UP, ShotType.MEDIUM,
                ShotType.WIDE, ShotType.EXTREME_WIDE
            ],
            'use_for': ['ending', 'isolation', 'farewell']
        },
        'intensity_build': {
            'description': 'Escalating tension through framing',
            'sequence': [
                ShotType.WIDE, ShotType.MEDIUM,
                ShotType.MEDIUM_CLOSE, ShotType.CLOSE_UP,
                ShotType.EXTREME_CLOSE
            ],
            'use_for': ['climax', 'tension', 'emotional_peak']
        },
        'performance_montage': {
            'description': 'Mixed sizes for music performance',
            'sequence': [
                ShotType.WIDE, ShotType.MEDIUM,
                ShotType.CLOSE_UP, ShotType.INSERT,
                ShotType.MEDIUM_WIDE, ShotType.EXTREME_CLOSE
            ],
            'use_for': ['concert', 'music_video', 'dance']
        }
    }

    @classmethod
    def get_pattern(cls, pattern_name: str) -> Optional[Dict]:
        """Get a specific shot pattern."""
        return cls.PATTERNS.get(pattern_name)

    @classmethod
    def suggest_pattern(cls, context: str) -> str:
        """Suggest a pattern based on context."""
        context_lower = context.lower()

        for pattern_name, pattern_data in cls.PATTERNS.items():
            if any(use in context_lower for use in pattern_data['use_for']):
                return pattern_name

        return 'performance_montage'  # Default for music videos


# ============================================================
# ShotBrain Main Class
# ============================================================

@dataclass
class ShotBrainOutput:
    """Output from ShotBrain analysis."""
    shot_spec: ShotSpec
    camera_psychology: Dict
    alternative_shots: List[ShotSpec]
    confidence: float
    reasoning: str

    def to_dict(self) -> Dict:
        return {
            'shot_spec': self.shot_spec.to_dict(),
            'camera_psychology': self.camera_psychology,
            'alternative_shots': [s.to_dict() for s in self.alternative_shots],
            'confidence': self.confidence,
            'reasoning': self.reasoning
        }


class ShotBrain:
    """
    ShotBrain™ - AI Shot Designer

    The intelligent cinematography engine that designs shots based on:
    - Musical context (energy, beat position, genre)
    - Emotional goals
    - Visual continuity
    - Camera psychology principles
    """

    def __init__(self, genre: str = "electronic", style: str = "cinematic"):
        self.genre = genre.lower()
        self.style = style
        self.cinematographer = TheCinematographer(genre=genre, style=style)
        self.shot_history: List[ShotSpec] = []
        self.pattern_engine = ShotPatternEngine()
        self.psychology = CameraPsychology()

    def design_shot(self,
                    energy_level: float,
                    beat_position: str,
                    duration: float = 5.0,
                    emotional_goal: Optional[str] = None,
                    context: str = "",
                    previous_shot: Optional[ShotSpec] = None) -> ShotBrainOutput:
        """
        Design an optimal shot using AI cinematography principles.

        Args:
            energy_level: 0.0-1.0 energy from audio analysis
            beat_position: verse, chorus, bridge, drop, intro, outro
            duration: Shot duration in seconds
            emotional_goal: Target emotion (optional)
            context: Additional context string
            previous_shot: Previous shot for continuity

        Returns:
            ShotBrainOutput with full analysis
        """

        # Get camera psychology recommendations
        emotional_target = emotional_goal or self._infer_emotion(energy_level, beat_position)
        psychology_rec = self.psychology.get_recommended_setup(emotional_target, energy_level)

        # Use cinematographer for base shot
        base_shot = self.cinematographer.design_shot(
            energy_level=energy_level,
            beat_position=beat_position,
            duration=duration,
            context=context
        )

        # Apply psychology recommendations
        enhanced_shot = self._apply_psychology(base_shot, psychology_rec)

        # Ensure continuity with previous shot
        if previous_shot:
            enhanced_shot = self._ensure_continuity(enhanced_shot, previous_shot)

        # Generate alternatives
        alternatives = self._generate_alternatives(enhanced_shot, energy_level, beat_position)

        # Calculate confidence
        confidence = self._calculate_confidence(enhanced_shot, previous_shot, energy_level)

        # Generate reasoning
        reasoning = self._generate_reasoning(enhanced_shot, psychology_rec, beat_position)

        self.shot_history.append(enhanced_shot)

        return ShotBrainOutput(
            shot_spec=enhanced_shot,
            camera_psychology=psychology_rec,
            alternative_shots=alternatives,
            confidence=confidence,
            reasoning=reasoning
        )

    def _infer_emotion(self, energy: float, beat_position: str) -> str:
        """Infer emotional goal from audio context."""
        emotion_map = {
            ('high', 'chorus'): 'triumph',
            ('high', 'drop'): 'intensity',
            ('high', 'verse'): 'energy',
            ('medium', 'chorus'): 'hope',
            ('medium', 'verse'): 'presence',
            ('medium', 'bridge'): 'reflection',
            ('low', 'verse'): 'intimacy',
            ('low', 'intro'): 'mystery',
            ('low', 'outro'): 'departure'
        }

        energy_level = 'high' if energy > 0.7 else ('medium' if energy > 0.3 else 'low')
        return emotion_map.get((energy_level, beat_position), 'presence')

    def _apply_psychology(self, shot: ShotSpec, psychology: Dict) -> ShotSpec:
        """Apply camera psychology recommendations to shot."""
        # Apply recommended movement if different
        recommended_movement = psychology.get('movement')
        if isinstance(recommended_movement, CameraMovement):
            # Blend with existing if complementary
            if shot.camera_movement == CameraMovement.STATIC:
                shot.camera_movement = recommended_movement

        # Adjust composition notes
        shot.composition_notes += f". Psychology: {psychology.get('angle_effect', '')}"

        return shot

    def _ensure_continuity(self, current: ShotSpec, previous: ShotSpec) -> ShotSpec:
        """Ensure visual continuity with previous shot."""
        # Avoid jump cuts (same size back-to-back)
        if current.shot_type == previous.shot_type:
            # Vary by at least one size
            shot_order = list(ShotType)
            current_idx = shot_order.index(current.shot_type)
            new_idx = (current_idx + 2) % len(shot_order)  # Jump 2 sizes
            current.shot_type = shot_order[new_idx]

        # Avoid crossing the line (maintain screen direction)
        opposing_movements = {
            CameraMovement.PAN_LEFT: CameraMovement.PAN_RIGHT,
            CameraMovement.PAN_RIGHT: CameraMovement.PAN_LEFT,
            CameraMovement.TRUCK_LEFT: CameraMovement.TRUCK_RIGHT,
            CameraMovement.TRUCK_RIGHT: CameraMovement.TRUCK_LEFT
        }

        if previous.camera_movement in opposing_movements:
            if current.camera_movement == opposing_movements[previous.camera_movement]:
                current.camera_movement = CameraMovement.STATIC

        return current

    def _generate_alternatives(self, shot: ShotSpec, energy: float,
                              beat_position: str) -> List[ShotSpec]:
        """Generate alternative shot options."""
        alternatives = []

        # Alternative 1: Different shot size
        alt1 = ShotSpec(
            shot_type=self._get_adjacent_shot_type(shot.shot_type),
            camera_movement=shot.camera_movement,
            duration=shot.duration,
            description=f"Alternative framing: {shot.description}",
            emotional_tone=shot.emotional_tone,
            lighting_notes=shot.lighting_notes,
            composition_notes=shot.composition_notes,
            focal_length=shot.focal_length,
            depth_of_field=shot.depth_of_field
        )
        alternatives.append(alt1)

        # Alternative 2: Different movement
        alt2 = ShotSpec(
            shot_type=shot.shot_type,
            camera_movement=self._get_alternative_movement(shot.camera_movement, energy),
            duration=shot.duration,
            description=f"Alternative movement: {shot.description}",
            emotional_tone=shot.emotional_tone,
            lighting_notes=shot.lighting_notes,
            composition_notes=shot.composition_notes,
            focal_length=shot.focal_length,
            depth_of_field=shot.depth_of_field
        )
        alternatives.append(alt2)

        return alternatives

    def _get_adjacent_shot_type(self, current: ShotType) -> ShotType:
        """Get an adjacent shot type for variety."""
        shot_order = [
            ShotType.EXTREME_WIDE, ShotType.WIDE, ShotType.MEDIUM_WIDE,
            ShotType.MEDIUM, ShotType.MEDIUM_CLOSE, ShotType.CLOSE_UP,
            ShotType.EXTREME_CLOSE
        ]

        try:
            idx = shot_order.index(current)
            new_idx = (idx + 1) % len(shot_order)
            return shot_order[new_idx]
        except ValueError:
            return ShotType.MEDIUM

    def _get_alternative_movement(self, current: CameraMovement, energy: float) -> CameraMovement:
        """Get alternative camera movement."""
        if energy > 0.6:
            options = [CameraMovement.DOLLY_IN, CameraMovement.CRANE_UP, CameraMovement.HANDHELD]
        else:
            options = [CameraMovement.STATIC, CameraMovement.STEADICAM, CameraMovement.DOLLY_OUT]

        # Return something different from current
        for opt in options:
            if opt != current:
                return opt

        return CameraMovement.STATIC

    def _calculate_confidence(self, shot: ShotSpec, previous: Optional[ShotSpec],
                             energy: float) -> float:
        """Calculate confidence score for the shot design."""
        confidence = 0.7  # Base confidence

        # Boost for good continuity
        if previous and shot.shot_type != previous.shot_type:
            confidence += 0.1

        # Boost for energy-appropriate movement
        if energy > 0.6 and shot.camera_movement != CameraMovement.STATIC:
            confidence += 0.1
        elif energy < 0.4 and shot.camera_movement in [CameraMovement.STATIC, CameraMovement.STEADICAM]:
            confidence += 0.1

        return min(1.0, confidence)

    def _generate_reasoning(self, shot: ShotSpec, psychology: Dict,
                           beat_position: str) -> str:
        """Generate human-readable reasoning for the shot choice."""
        return (
            f"Selected {shot.shot_type.value} shot with {shot.camera_movement.value} "
            f"for {beat_position} section. {psychology.get('angle_effect', '')}. "
            f"Movement creates {psychology.get('movement_effect', 'visual interest')}. "
            f"Emotional target: {shot.emotional_tone.value}."
        )

    def design_sequence(self,
                       sections: List[Dict],
                       beats: List[float],
                       bpm: float) -> List[ShotBrainOutput]:
        """Design a complete shot sequence for multiple sections."""
        sequence = []
        previous_shot = None

        for section in sections:
            section_type = section.get('type', 'verse')
            energy = section.get('energy', 0.5)
            start = section.get('start', 0)
            duration = section.get('duration', 10)

            # Calculate shots needed
            avg_shot_duration = self._get_avg_shot_duration(energy)
            num_shots = max(1, int(duration / avg_shot_duration))

            for i in range(num_shots):
                shot_output = self.design_shot(
                    energy_level=energy,
                    beat_position=section_type,
                    duration=avg_shot_duration,
                    context=f"Section {section_type}, shot {i+1}/{num_shots}",
                    previous_shot=previous_shot
                )
                sequence.append(shot_output)
                previous_shot = shot_output.shot_spec

        return sequence

    def _get_avg_shot_duration(self, energy: float) -> float:
        """Get average shot duration based on energy."""
        if energy > 0.7:
            return 2.5  # Fast cuts
        elif energy > 0.4:
            return 4.0  # Medium pace
        else:
            return 6.0  # Slow, contemplative

    def export_shot_list(self, output_path: str) -> str:
        """Export the shot list to JSON."""
        shot_list = {
            'shots': [s.to_dict() for s in self.shot_history],
            'genre': self.genre,
            'style': self.style,
            'total_shots': len(self.shot_history),
            'exported_at': datetime.utcnow().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(shot_list, f, indent=2)

        return output_path

    def get_prompt_for_shot(self, shot: ShotSpec, style_modifiers: List[str] = None) -> str:
        """Generate an AI image generation prompt for a shot."""
        components = [
            f"cinematic {self.style} photography",
            shot.description,
            f"{shot.shot_type.value.replace('_', ' ')} shot",
            f"{shot.focal_length} lens",
            f"{shot.depth_of_field} depth of field",
            shot.lighting_notes,
            f"{shot.emotional_tone.value} atmosphere",
            "professional cinematography",
            "film grain",
            "8K resolution"
        ]

        if style_modifiers:
            components.extend(style_modifiers)

        return ", ".join(filter(None, components))
