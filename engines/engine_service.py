#!/usr/bin/env python3
"""
VISUALX Engine Service
Exposes all engines via HTTP API for Node.js integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add engines directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visualx_agents import (
    TheCinematographer, TheEditor, TheColorist,
    VISUALXOrchestrator, EmotionalTone, ShotType, CameraMovement, Platform
)
from creative_council import CreativeCouncil
from colorbrain import ColorBrain, LookStyle
from shotbrain import ShotBrain
from editbrain import EditBrain

app = Flask(__name__)
CORS(app)

# Initialize engines
councils = {}
colorbrains = {}
shotbrains = {}
editbrains = {}
orchestrators = {}


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'VISUALX Engine Service'})


@app.route('/api/council/convene', methods=['POST'])
def convene_council():
    """Convene the Creative Council to generate prompts."""
    data = request.json
    
    song_title = data.get('song_title', 'Untitled')
    genre = data.get('genre', 'electronic')
    bpm = data.get('bpm', 120)
    analysis_data = data.get('analysis_data', {})
    mode = data.get('mode', 'cinematic')
    artist_description = data.get('artist_description')
    project_context = data.get('project_context')
    engine = data.get('engine', 'rules')
    
    # Get or create council instance
    key = f"{genre}_{engine}"
    if key not in councils:
        councils[key] = CreativeCouncil(engine=engine)
    
    council = councils[key]
    
    try:
        image_prompt, motion_prompt = council.convene_council(
            song_title=song_title,
            genre=genre,
            bpm=bpm,
            analysis_data=analysis_data,
            mode=mode,
            artist_description=artist_description,
            project_context=project_context
        )
        
        return jsonify({
            'success': True,
            'image_prompt': image_prompt,
            'motion_prompt': motion_prompt
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/colorbrain/develop', methods=['POST'])
def develop_color_look():
    """Develop a master color look."""
    data = request.json
    
    genre = data.get('genre', 'electronic')
    emotion_str = data.get('emotion', 'serene')
    custom_style = data.get('custom_style')
    key_color = data.get('key_color')
    
    # Get or create colorbrain instance
    if genre not in colorbrains:
        colorbrains[genre] = ColorBrain(genre=genre)
    
    colorbrain = colorbrains[genre]
    
    # Convert emotion string to enum
    emotion_map = {
        'euphoric': EmotionalTone.EUPHORIC,
        'melancholic': EmotionalTone.MELANCHOLIC,
        'aggressive': EmotionalTone.AGGRESSIVE,
        'serene': EmotionalTone.SERENE,
        'mysterious': EmotionalTone.MYSTERIOUS,
        'romantic': EmotionalTone.ROMANTIC,
        'dark': EmotionalTone.DARK,
        'triumphant': EmotionalTone.TRIUMPHANT,
        'anxious': EmotionalTone.ANXIOUS,
        'nostalgic': EmotionalTone.NOSTALGIC
    }
    
    emotion = emotion_map.get(emotion_str.lower(), EmotionalTone.SERENE)
    
    # Convert style if provided
    look_style = None
    if custom_style:
        style_map = {
            'blockbuster': LookStyle.BLOCKBUSTER,
            'indie': LookStyle.INDIE,
            'vintage': LookStyle.VINTAGE,
            'neon': LookStyle.NEON,
            'noir': LookStyle.NOIR,
            'natural': LookStyle.NATURAL,
            'dream': LookStyle.DREAM,
            'gritty': LookStyle.GRITTY,
            'pastel': LookStyle.PASTEL,
            'moody': LookStyle.MOODY
        }
        look_style = style_map.get(custom_style.lower())
    
    try:
        grade_spec = colorbrain.develop_master_look(
            emotion=emotion,
            custom_style=look_style,
            key_color=key_color
        )
        
        return jsonify({
            'success': True,
            'grade_spec': grade_spec.to_dict(),
            'color_palette': colorbrain.get_color_palette()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/shotbrain/design', methods=['POST'])
def design_shot():
    """Design a shot using ShotBrain."""
    data = request.json
    
    genre = data.get('genre', 'electronic')
    style = data.get('style', 'cinematic')
    energy_level = data.get('energy_level', 0.5)
    beat_position = data.get('beat_position', 'verse')
    duration = data.get('duration', 5.0)
    emotional_goal = data.get('emotional_goal')
    context = data.get('context', '')
    
    # Get or create shotbrain instance
    key = f"{genre}_{style}"
    if key not in shotbrains:
        shotbrains[key] = ShotBrain(genre=genre, style=style)
    
    shotbrain = shotbrains[key]
    
    try:
        output = shotbrain.design_shot(
            energy_level=energy_level,
            beat_position=beat_position,
            duration=duration,
            emotional_goal=emotional_goal,
            context=context
        )
        
        return jsonify({
            'success': True,
            'output': output.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/editbrain/analyze', methods=['POST'])
def analyze_for_cuts():
    """Analyze audio and determine cut points."""
    data = request.json
    
    genre = data.get('genre', 'electronic')
    bpm = data.get('bpm', 120.0)
    duration = data.get('duration', 180.0)
    energy_curve = data.get('energy_curve', [])
    sections = data.get('sections', [])
    
    # Get or create editbrain instance
    key = f"{genre}_{bpm}"
    if key not in editbrains:
        editbrains[key] = EditBrain(genre=genre, bpm=bpm)
    
    editbrain = editbrains[key]
    
    try:
        cut_points = editbrain.analyze_for_cuts(
            duration=duration,
            energy_curve=energy_curve,
            sections=sections
        )
        
        return jsonify({
            'success': True,
            'cut_points': [cp.to_dict() for cp in cut_points],
            'stats': editbrain.get_cut_stats()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/orchestrator/create', methods=['POST'])
def create_visual_package():
    """Create a complete visual package using the orchestrator."""
    data = request.json
    
    title = data.get('title', 'Untitled')
    genre = data.get('genre', 'electronic')
    style = data.get('style', 'cinematic')
    audio_analysis = data.get('audio_analysis', {})
    target_platforms = data.get('target_platforms', ['youtube'])
    output_dir = data.get('output_dir', './output')
    
    # Get or create orchestrator
    key = f"{genre}_{style}"
    if key not in orchestrators:
        orchestrators[key] = VISUALXOrchestrator(genre=genre, style=style)
    
    orchestrator = orchestrators[key]
    
    # Convert platform strings to enums
    platform_map = {
        'tiktok': Platform.TIKTOK,
        'youtube': Platform.YOUTUBE,
        'youtube_shorts': Platform.YOUTUBE_SHORTS,
        'instagram_reels': Platform.INSTAGRAM_REELS,
        'instagram_feed': Platform.INSTAGRAM_FEED,
        'theatrical': Platform.THEATRICAL,
        'streaming_4k': Platform.STREAMING_4K,
        'broadcast': Platform.BROADCAST
    }
    
    platforms = [platform_map.get(p.lower(), Platform.YOUTUBE) for p in target_platforms]
    
    try:
        visual_package = orchestrator.create_visual_package(
            title=title,
            audio_analysis=audio_analysis,
            target_platforms=platforms,
            output_dir=output_dir
        )
        
        return jsonify({
            'success': True,
            'package': visual_package
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('ENGINE_SERVICE_PORT', 5051))
    app.run(host='0.0.0.0', port=port, debug=True)



