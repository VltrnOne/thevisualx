"""
EditBrain™ - Rough Cut Engine
Powered by VLTRN / VISUALX

Intelligent editing engine for beat-synced assembly,
rhythm analysis, and professional cut timing.
"""

import os
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

from visualx_agents import EditDecision, ShotSpec, TheEditor


# ============================================================
# Edit Intelligence Types
# ============================================================

class CutMotive(Enum):
    """Motivation for making a cut."""
    BEAT_SYNC = "beat_sync"           # Cut on musical beat
    ENERGY_CHANGE = "energy_change"   # Energy level shift
    SECTION_CHANGE = "section_change" # Musical section boundary
    VISUAL_INTEREST = "visual_interest" # Maintain engagement
    NARRATIVE = "narrative"           # Story progression
    MATCH_ACTION = "match_action"     # Continuous motion
    CONTRAST = "contrast"             # Visual juxtaposition
    RHYTHM = "rhythm"                 # Maintain cut rhythm


class TransitionStyle(Enum):
    """Visual transition styles."""
    HARD_CUT = "hard_cut"
    DISSOLVE = "dissolve"
    FADE_BLACK = "fade_black"
    FADE_WHITE = "fade_white"
    WIPE_LEFT = "wipe_left"
    WIPE_RIGHT = "wipe_right"
    MORPH = "morph"
    ZOOM_TRANSITION = "zoom_transition"
    WHIP_PAN = "whip_pan"
    FLASH = "flash"
    GLITCH = "glitch"


@dataclass
class CutPoint:
    """Detailed cut point specification."""
    timestamp: float
    motive: CutMotive
    transition: TransitionStyle
    transition_duration: float
    beat_aligned: bool
    beat_offset: float  # Offset from nearest beat (ms)
    confidence: float
    notes: str

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'motive': self.motive.value,
            'transition': self.transition.value,
            'transition_duration': self.transition_duration,
            'beat_aligned': self.beat_aligned,
            'beat_offset': self.beat_offset,
            'confidence': self.confidence,
            'notes': self.notes
        }


@dataclass
class EditBlock:
    """A block of edited content."""
    source_clip: str
    in_point: float
    out_point: float
    timeline_start: float
    timeline_end: float
    speed: float  # 1.0 = normal, 0.5 = slow-mo, 2.0 = fast
    reverse: bool
    effects: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# Rhythm Analyzer
# ============================================================

class RhythmAnalyzer:
    """
    Analyzes musical rhythm for optimal cut placement.
    """

    def __init__(self, bpm: float):
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm  # seconds per beat
        self.bar_duration = self.beat_duration * 4  # Assuming 4/4 time

    def get_beat_grid(self, duration: float) -> List[float]:
        """Generate a grid of beat timestamps."""
        beats = []
        current = 0.0
        while current < duration:
            beats.append(current)
            current += self.beat_duration
        return beats

    def get_strong_beats(self, duration: float) -> List[float]:
        """Get strong beats (downbeats) for major cuts."""
        # Every 4th beat (bar start) is strong
        all_beats = self.get_beat_grid(duration)
        return [b for i, b in enumerate(all_beats) if i % 4 == 0]

    def get_syncopated_beats(self, duration: float) -> List[float]:
        """Get syncopated positions (off-beats) for dynamic cuts."""
        beats = self.get_beat_grid(duration)
        # Half-beat positions
        syncopated = []
        for i in range(len(beats) - 1):
            syncopated.append((beats[i] + beats[i+1]) / 2)
        return syncopated

    def snap_to_beat(self, timestamp: float) -> Tuple[float, float]:
        """
        Snap a timestamp to the nearest beat.
        Returns (snapped_time, offset_ms).
        """
        beats = int(timestamp / self.beat_duration)
        beat_position = beats * self.beat_duration
        next_beat = beat_position + self.beat_duration

        # Find nearest
        if abs(timestamp - beat_position) < abs(timestamp - next_beat):
            snapped = beat_position
        else:
            snapped = next_beat

        offset_ms = (timestamp - snapped) * 1000
        return snapped, offset_ms

    def get_cut_rating(self, timestamp: float) -> float:
        """
        Rate how good a timestamp is for cutting (0-1).
        Strong beats = 1.0, off-beats = 0.7, random = 0.3
        """
        _, offset = self.snap_to_beat(timestamp)
        offset_abs = abs(offset)

        if offset_abs < 20:  # Within 20ms of beat
            return 1.0
        elif offset_abs < 50:  # Within 50ms
            return 0.8
        elif offset_abs < 100:  # Within 100ms
            return 0.6
        else:
            return 0.3


# ============================================================
# EditBrain Main Class
# ============================================================

class EditBrain:
    """
    EditBrain™ - Intelligent Rough Cut Engine

    Creates professional edit assemblies using:
    - Beat synchronization
    - Energy-based pacing
    - Genre-specific cut patterns
    - Visual continuity rules
    """

    # Genre-specific editing styles
    GENRE_STYLES = {
        'hip-hop': {
            'cuts_per_bar': 2,
            'preferred_transitions': [TransitionStyle.HARD_CUT, TransitionStyle.WHIP_PAN],
            'syncopation': 0.3,  # 30% cuts on off-beats
            'speed_ramps': True
        },
        'electronic': {
            'cuts_per_bar': 4,
            'preferred_transitions': [TransitionStyle.HARD_CUT, TransitionStyle.FLASH, TransitionStyle.GLITCH],
            'syncopation': 0.4,
            'speed_ramps': True
        },
        'r&b': {
            'cuts_per_bar': 1,
            'preferred_transitions': [TransitionStyle.DISSOLVE, TransitionStyle.HARD_CUT],
            'syncopation': 0.1,
            'speed_ramps': False
        },
        'rock': {
            'cuts_per_bar': 2,
            'preferred_transitions': [TransitionStyle.HARD_CUT, TransitionStyle.WHIP_PAN],
            'syncopation': 0.2,
            'speed_ramps': True
        },
        'pop': {
            'cuts_per_bar': 2,
            'preferred_transitions': [TransitionStyle.HARD_CUT, TransitionStyle.DISSOLVE],
            'syncopation': 0.2,
            'speed_ramps': True
        },
        'ambient': {
            'cuts_per_bar': 0.5,  # One cut every 2 bars
            'preferred_transitions': [TransitionStyle.DISSOLVE, TransitionStyle.FADE_BLACK],
            'syncopation': 0.0,
            'speed_ramps': False
        }
    }

    def __init__(self, genre: str = "electronic", bpm: float = 120.0):
        self.genre = genre.lower()
        self.bpm = bpm
        self.rhythm = RhythmAnalyzer(bpm)
        self.editor = TheEditor(style=self._get_edit_style())
        self.cut_points: List[CutPoint] = []
        self.edit_blocks: List[EditBlock] = []
        self.style_config = self.GENRE_STYLES.get(self.genre, self.GENRE_STYLES['pop'])

    def _get_edit_style(self) -> str:
        """Get edit style based on genre."""
        if self.genre in ['electronic', 'hip-hop', 'rock']:
            return 'dynamic'
        elif self.genre in ['r&b', 'ambient']:
            return 'smooth'
        else:
            return 'balanced'

    def analyze_for_cuts(self,
                        duration: float,
                        energy_curve: List[float],
                        sections: List[Dict]) -> List[CutPoint]:
        """
        Analyze audio data and determine optimal cut points.

        Args:
            duration: Total duration in seconds
            energy_curve: Energy values over time (0-1)
            sections: Musical sections with type, start, duration

        Returns:
            List of CutPoint objects
        """
        cut_points = []

        # 1. Get base beat grid
        beats = self.rhythm.get_beat_grid(duration)
        strong_beats = self.rhythm.get_strong_beats(duration)

        # 2. Calculate cuts per bar based on genre
        cuts_per_bar = self.style_config['cuts_per_bar']
        bar_duration = self.rhythm.bar_duration

        # 3. Process each section
        for section in sections:
            section_start = section.get('start', 0)
            section_duration = section.get('duration', 10)
            section_type = section.get('type', 'verse')
            section_energy = section.get('energy', 0.5)

            # Adjust cut frequency based on energy and section type
            adjusted_cuts = self._adjust_cut_frequency(cuts_per_bar, section_energy, section_type)

            # Generate cut points within section
            section_cuts = self._generate_section_cuts(
                section_start,
                section_duration,
                adjusted_cuts,
                section_type,
                beats,
                strong_beats
            )
            cut_points.extend(section_cuts)

        # 4. Add section boundary cuts
        for i, section in enumerate(sections[:-1]):
            next_section = sections[i + 1]
            boundary_cut = CutPoint(
                timestamp=next_section['start'],
                motive=CutMotive.SECTION_CHANGE,
                transition=self._get_section_transition(section, next_section),
                transition_duration=0.5,
                beat_aligned=True,
                beat_offset=0,
                confidence=0.95,
                notes=f"Section change: {section.get('type')} -> {next_section.get('type')}"
            )
            cut_points.append(boundary_cut)

        # Sort by timestamp
        cut_points.sort(key=lambda x: x.timestamp)

        # Remove duplicates (cuts too close together)
        self.cut_points = self._deduplicate_cuts(cut_points)

        return self.cut_points

    def _adjust_cut_frequency(self, base_cuts: float, energy: float, section_type: str) -> float:
        """Adjust cut frequency based on context."""
        # Energy multiplier
        if energy > 0.7:
            multiplier = 1.5
        elif energy > 0.4:
            multiplier = 1.0
        else:
            multiplier = 0.7

        # Section type adjustments
        section_adjustments = {
            'chorus': 1.3,
            'drop': 1.5,
            'verse': 0.8,
            'bridge': 0.6,
            'intro': 0.5,
            'outro': 0.5,
            'breakdown': 0.4
        }

        section_mult = section_adjustments.get(section_type, 1.0)

        return base_cuts * multiplier * section_mult

    def _generate_section_cuts(self,
                              start: float,
                              duration: float,
                              cuts_per_bar: float,
                              section_type: str,
                              beats: List[float],
                              strong_beats: List[float]) -> List[CutPoint]:
        """Generate cut points within a section."""
        cuts = []
        bar_duration = self.rhythm.bar_duration
        num_bars = duration / bar_duration
        total_cuts = int(num_bars * cuts_per_bar)

        if total_cuts == 0:
            return cuts

        cut_interval = duration / total_cuts

        for i in range(total_cuts):
            raw_timestamp = start + (i * cut_interval)

            # Snap to beat
            snapped, offset = self.rhythm.snap_to_beat(raw_timestamp)

            # Make sure we're in the section
            if snapped < start or snapped >= start + duration:
                continue

            # Determine motive
            motive = self._determine_motive(snapped, beats, strong_beats, i, total_cuts)

            # Select transition
            transition = self._select_transition(motive, section_type)

            cut = CutPoint(
                timestamp=snapped,
                motive=motive,
                transition=transition,
                transition_duration=0 if transition == TransitionStyle.HARD_CUT else 0.3,
                beat_aligned=abs(offset) < 50,
                beat_offset=offset,
                confidence=self.rhythm.get_cut_rating(snapped),
                notes=f"{section_type} section, cut {i+1}/{total_cuts}"
            )
            cuts.append(cut)

        return cuts

    def _determine_motive(self,
                         timestamp: float,
                         beats: List[float],
                         strong_beats: List[float],
                         cut_index: int,
                         total_cuts: int) -> CutMotive:
        """Determine the motivation for a cut."""
        # Check if on strong beat
        for sb in strong_beats:
            if abs(timestamp - sb) < 0.05:
                return CutMotive.BEAT_SYNC

        # First and last cuts
        if cut_index == 0:
            return CutMotive.NARRATIVE
        if cut_index == total_cuts - 1:
            return CutMotive.SECTION_CHANGE

        # Default to rhythm
        return CutMotive.RHYTHM

    def _select_transition(self, motive: CutMotive, section_type: str) -> TransitionStyle:
        """Select appropriate transition style."""
        # Most cuts are hard cuts for music videos
        if motive in [CutMotive.BEAT_SYNC, CutMotive.RHYTHM]:
            return TransitionStyle.HARD_CUT

        # Section changes may use transitions
        if motive == CutMotive.SECTION_CHANGE:
            if section_type in ['bridge', 'breakdown']:
                return TransitionStyle.DISSOLVE
            elif section_type == 'outro':
                return TransitionStyle.FADE_BLACK

        # Use genre preference
        preferred = self.style_config['preferred_transitions']
        return preferred[0] if preferred else TransitionStyle.HARD_CUT

    def _get_section_transition(self, from_section: Dict, to_section: Dict) -> TransitionStyle:
        """Get transition style between sections."""
        from_type = from_section.get('type', 'verse')
        to_type = to_section.get('type', 'chorus')

        # Special transitions for specific changes
        if to_type == 'drop':
            return TransitionStyle.FLASH
        if from_type == 'breakdown' and to_type == 'chorus':
            return TransitionStyle.HARD_CUT  # Impact cut
        if to_type == 'outro':
            return TransitionStyle.FADE_BLACK
        if to_type == 'bridge':
            return TransitionStyle.DISSOLVE

        return TransitionStyle.HARD_CUT

    def _deduplicate_cuts(self, cuts: List[CutPoint], min_gap: float = 0.5) -> List[CutPoint]:
        """Remove cuts that are too close together."""
        if not cuts:
            return cuts

        deduped = [cuts[0]]
        for cut in cuts[1:]:
            if cut.timestamp - deduped[-1].timestamp >= min_gap:
                deduped.append(cut)
            elif cut.confidence > deduped[-1].confidence:
                # Replace with higher confidence cut
                deduped[-1] = cut

        return deduped

    def create_edit_blocks(self,
                          clips: List[str],
                          cut_points: Optional[List[CutPoint]] = None) -> List[EditBlock]:
        """
        Create edit blocks assigning clips to cut points.

        Args:
            clips: List of clip file paths
            cut_points: Optional cut points (uses self.cut_points if None)

        Returns:
            List of EditBlock objects for timeline assembly
        """
        if cut_points is None:
            cut_points = self.cut_points

        if not cut_points or not clips:
            return []

        blocks = []
        num_clips = len(clips)

        for i, cut in enumerate(cut_points):
            # Select clip (cycle through available clips)
            clip_index = i % num_clips
            clip_path = clips[clip_index]

            # Calculate duration until next cut
            if i < len(cut_points) - 1:
                duration = cut_points[i + 1].timestamp - cut.timestamp
            else:
                duration = 5.0  # Default 5s for last cut

            # Create block
            block = EditBlock(
                source_clip=clip_path,
                in_point=0.0,  # Start of clip
                out_point=min(duration, 5.0),  # Clip length or cut duration
                timeline_start=cut.timestamp,
                timeline_end=cut.timestamp + duration,
                speed=1.0,
                reverse=False,
                effects=[]
            )

            # Add speed ramping for certain genres/sections
            if self.style_config['speed_ramps'] and cut.motive == CutMotive.BEAT_SYNC:
                if i % 4 == 0:  # Every 4th cut
                    block.speed = 0.5  # Slow-mo
                    block.effects.append('speed_ramp')

            blocks.append(block)

        self.edit_blocks = blocks
        return blocks

    def export_edl(self, output_path: str, timeline_name: str = "VISUALX_CUT") -> str:
        """Export Edit Decision List in CMX3600 format."""
        edl_lines = [
            f"TITLE: {timeline_name}",
            "FCM: NON-DROP FRAME",
            ""
        ]

        for i, block in enumerate(self.edit_blocks, 1):
            # Calculate timecodes
            tc_in = self._seconds_to_tc(block.in_point)
            tc_out = self._seconds_to_tc(block.out_point)
            tc_rec_in = self._seconds_to_tc(block.timeline_start)
            tc_rec_out = self._seconds_to_tc(block.timeline_end)

            # EDL line format: EVENT# REEL# TRACK TYPE IN OUT RECIN RECOUT
            edl_lines.append(
                f"{i:03d}  AX       V     C        {tc_in} {tc_out} {tc_rec_in} {tc_rec_out}"
            )
            edl_lines.append(f"* FROM CLIP NAME: {os.path.basename(block.source_clip)}")

            if block.speed != 1.0:
                edl_lines.append(f"* SPEED: {block.speed}")
            if block.effects:
                edl_lines.append(f"* EFFECTS: {', '.join(block.effects)}")

            edl_lines.append("")

        with open(output_path, 'w') as f:
            f.write('\n'.join(edl_lines))

        return output_path

    def export_timeline_json(self, output_path: str) -> str:
        """Export timeline as JSON for web-based editors."""
        timeline = {
            'name': 'VISUALX Timeline',
            'bpm': self.bpm,
            'genre': self.genre,
            'cut_points': [c.to_dict() for c in self.cut_points],
            'edit_blocks': [b.to_dict() for b in self.edit_blocks],
            'style_config': {
                k: v if not isinstance(v, list) else [
                    t.value if hasattr(t, 'value') else t for t in v
                ] for k, v in self.style_config.items()
            },
            'exported_at': datetime.utcnow().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(timeline, f, indent=2)

        return output_path

    def _seconds_to_tc(self, seconds: float, fps: int = 24) -> str:
        """Convert seconds to SMPTE timecode."""
        total_frames = int(seconds * fps)
        frames = total_frames % fps
        total_seconds = total_frames // fps
        secs = total_seconds % 60
        mins = (total_seconds // 60) % 60
        hours = total_seconds // 3600

        return f"{hours:02d}:{mins:02d}:{secs:02d}:{frames:02d}"

    def get_cut_stats(self) -> Dict:
        """Get statistics about the edit."""
        if not self.cut_points:
            return {}

        durations = []
        for i in range(len(self.cut_points) - 1):
            dur = self.cut_points[i + 1].timestamp - self.cut_points[i].timestamp
            durations.append(dur)

        return {
            'total_cuts': len(self.cut_points),
            'avg_shot_duration': sum(durations) / len(durations) if durations else 0,
            'min_shot_duration': min(durations) if durations else 0,
            'max_shot_duration': max(durations) if durations else 0,
            'cuts_per_minute': len(self.cut_points) / (self.cut_points[-1].timestamp / 60) if self.cut_points else 0,
            'beat_aligned_percentage': sum(1 for c in self.cut_points if c.beat_aligned) / len(self.cut_points) * 100 if self.cut_points else 0,
            'motive_breakdown': self._get_motive_breakdown()
        }

    def _get_motive_breakdown(self) -> Dict[str, int]:
        """Get breakdown of cut motives."""
        breakdown = {}
        for cut in self.cut_points:
            motive = cut.motive.value
            breakdown[motive] = breakdown.get(motive, 0) + 1
        return breakdown
