#!/usr/bin/env python3
"""
VISUALX Engine Service
Exposes all engines via HTTP API for Node.js integration

Features:
- Audio upload and analysis
- Creative Council prompt generation
- ColorBrain color grading
- ShotBrain shot design
- EditBrain cut analysis
- Full VisualX Magic orchestration
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys
import os
import uuid
import json
import threading
from datetime import datetime

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

# Try to import audio analyzer (optional - requires librosa)
try:
    import librosa
    import numpy as np
    AUDIO_ANALYSIS_ENABLED = True
except ImportError:
    print("⚠️ librosa not installed - audio analysis disabled")
    AUDIO_ANALYSIS_ENABLED = False

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:8080',
    'http://localhost:3000',
    'https://thevisualx.com',
    'https://www.thevisualx.com',
    'https://thevisualx.onrender.com'
])

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'm4a', 'ogg'}
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize engines
councils = {}
colorbrains = {}
shotbrains = {}
editbrains = {}
orchestrators = {}

# Project and job storage
projects = {}
jobs = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sanitize_title(title):
    """Convert title to safe folder name."""
    import re
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    safe = safe.replace(' ', '_')
    return safe[:50]


class AudioAnalyzer:
    """Audio analysis using librosa."""
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.y = None
        self.sr = None
        self.duration = 0

    def load_audio(self):
        if not AUDIO_ANALYSIS_ENABLED:
            raise Exception("Audio analysis not available - librosa not installed")
        self.y, self.sr = librosa.load(self.audio_path)
        self.duration = float(librosa.get_duration(y=self.y, sr=self.sr))
        return self.duration

    def get_tempo(self):
        if self.y is None:
            self.load_audio()
        tempo, _ = librosa.beat.beat_track(y=self.y, sr=self.sr)
        if isinstance(tempo, np.ndarray):
            tempo = float(tempo[0]) if tempo.size > 0 else 120.0
        return float(tempo)

    def get_energy_curve(self, num_points=20):
        """Get energy curve for the track."""
        if self.y is None:
            self.load_audio()
        hop_length = 512
        rms = librosa.feature.rms(y=self.y, frame_length=2048, hop_length=hop_length)[0]
        # Resample to num_points
        indices = np.linspace(0, len(rms) - 1, num_points).astype(int)
        return [float(rms[i]) for i in indices]

    def get_loudest_section(self, duration=5):
        """Finds the loudest section for clip generation."""
        if self.y is None:
            self.load_audio()
        hop_length = 512
        rms = librosa.feature.rms(y=self.y, frame_length=2048, hop_length=hop_length)[0]
        times = librosa.frames_to_time(np.arange(len(rms)), sr=self.sr, hop_length=hop_length)
        frames_per_sec = self.sr / hop_length
        window_frames = int(duration * frames_per_sec)
        max_energy = 0
        best_start_frame = 0
        for i in range(0, len(rms) - window_frames, int(frames_per_sec)):
            current_energy = np.sum(rms[i:i + window_frames])
            if current_energy > max_energy:
                max_energy = current_energy
                best_start_frame = i
        start_time = times[best_start_frame]
        return float(start_time), float(start_time + duration)

    def detect_sections(self):
        """Detect song sections (verse, chorus, drop, etc.)."""
        if self.y is None:
            self.load_audio()
        # Simple section detection based on energy changes
        hop_length = 512
        rms = librosa.feature.rms(y=self.y, frame_length=2048, hop_length=hop_length)[0]
        times = librosa.frames_to_time(np.arange(len(rms)), sr=self.sr, hop_length=hop_length)

        # Segment into sections based on energy thresholds
        avg_energy = np.mean(rms)
        sections = []
        section_names = ['intro', 'verse', 'verse', 'drop', 'drop', 'bridge', 'verse', 'drop', 'outro']

        num_sections = min(len(section_names), int(self.duration / 15))  # ~15 sec per section
        section_duration = self.duration / num_sections

        for i in range(num_sections):
            start = i * section_duration
            end = (i + 1) * section_duration
            sections.append({
                'name': section_names[i % len(section_names)],
                'start': float(start),
                'end': float(end)
            })

        return sections


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'VISUALX Engine Service',
        'version': '2.1.0',
        'powered_by': 'VLTRN',
        'audio_analysis': AUDIO_ANALYSIS_ENABLED,
        'agents': [
            'THE CINEMATOGRAPHER',
            'THE EDITOR',
            'THE COLORIST',
            'THE STORYBOARD ARTIST',
            'THE DELIVERY ENGINEER'
        ],
        'modules': [
            'ShotBrain',
            'EditBrain',
            'ColorBrain',
            'CreativeCouncil',
            'PlatformPackager'
        ],
        'timestamp': datetime.utcnow().isoformat()
    })


# ============================================================
# AUDIO UPLOAD & ANALYSIS ENDPOINTS
# ============================================================

@app.route('/api/upload', methods=['POST'])
def upload_audio():
    """Upload an audio file and create a new project."""
    # Accept both 'file' and 'audio' field names
    file = request.files.get('file') or request.files.get('audio')
    if not file:
        return jsonify({'success': False, 'error': 'No audio file provided'}), 400
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'Invalid file type. Allowed: {ALLOWED_EXTENSIONS}'}), 400

    # Get metadata from form
    title = request.form.get('title', 'Untitled Track')
    genre = request.form.get('genre', 'Electronic')

    # Create project ID
    project_id = str(uuid.uuid4())[:8]
    project_folder = sanitize_title(title)

    # Create project directory
    project_path = os.path.join(OUTPUT_FOLDER, project_folder)
    os.makedirs(project_path, exist_ok=True)

    # Save audio file
    filename = secure_filename(file.filename)
    audio_path = os.path.join(project_path, filename)
    file.save(audio_path)

    # Create project record
    project = {
        'id': project_id,
        'title': title,
        'genre': genre,
        'folder': project_folder,
        'audio_file': filename,
        'audio_path': audio_path,
        'project_path': project_path,
        'created_at': datetime.utcnow().isoformat(),
        'status': 'uploaded',
        'analysis': None
    }

    # Save project to memory and disk
    projects[project_id] = project
    meta_path = os.path.join(project_path, 'project.json')
    with open(meta_path, 'w') as f:
        json.dump(project, f, indent=2)

    return jsonify({
        'success': True,
        'project_id': project_id,
        'project': project
    })


@app.route('/api/analyze/<project_id>', methods=['POST'])
def analyze_audio(project_id):
    """Analyze uploaded audio file."""
    if not AUDIO_ANALYSIS_ENABLED:
        return jsonify({'error': 'Audio analysis not available - librosa not installed'}), 503

    # Find project
    project = projects.get(project_id)
    if not project:
        # Try to load from disk
        for folder in os.listdir(OUTPUT_FOLDER):
            meta_path = os.path.join(OUTPUT_FOLDER, folder, 'project.json')
            if os.path.exists(meta_path):
                with open(meta_path) as f:
                    p = json.load(f)
                    if p.get('id') == project_id:
                        project = p
                        projects[project_id] = p
                        break

    if not project:
        return jsonify({'error': 'Project not found'}), 404

    try:
        # Run analysis
        analyzer = AudioAnalyzer(project['audio_path'])
        duration = analyzer.load_audio()
        bpm = analyzer.get_tempo()
        energy_curve = analyzer.get_energy_curve()
        sections = analyzer.detect_sections()
        loudest_start, loudest_end = analyzer.get_loudest_section()

        analysis = {
            'duration': duration,
            'bpm': bpm,
            'energy_curve': energy_curve,
            'sections': sections,
            'loudest_section': {
                'start': loudest_start,
                'end': loudest_end
            },
            'analyzed_at': datetime.utcnow().isoformat()
        }

        # Update project
        project['analysis'] = analysis
        project['status'] = 'analyzed'

        # Save to disk
        meta_path = os.path.join(project['project_path'], 'project.json')
        with open(meta_path, 'w') as f:
            json.dump(project, f, indent=2)

        return jsonify({
            'success': True,
            'project_id': project_id,
            'analysis': analysis
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects', methods=['GET'])
def list_projects():
    """List all projects."""
    user_id = request.args.get('user_id')  # Optional filter by user
    project_list = []
    if os.path.exists(OUTPUT_FOLDER):
        for folder in os.listdir(OUTPUT_FOLDER):
            project_path = os.path.join(OUTPUT_FOLDER, folder)
            meta_path = os.path.join(project_path, 'project.json')
            if os.path.isdir(project_path) and os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r') as f:
                        project = json.load(f)
                        # Include analysis data if available
                        analysis = project.get('analysis', {})
                        project_data = {
                            'id': project.get('id'),
                            'title': project.get('title', 'Untitled'),
                            'genre': project.get('genre', 'Unknown'),
                            'status': project.get('status', 'uploaded'),
                            'duration': analysis.get('duration', 0),
                            'bpm': analysis.get('bpm', 0),
                            'created_at': project.get('created_at'),
                            'mode': project.get('mode', 'manual')
                        }
                        project_list.append(project_data)
                except:
                    pass
    # Sort by created_at desc
    project_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return jsonify({'success': True, 'projects': project_list})


@app.route('/api/project/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get project details."""
    project = projects.get(project_id)
    if not project:
        for folder in os.listdir(OUTPUT_FOLDER):
            meta_path = os.path.join(OUTPUT_FOLDER, folder, 'project.json')
            if os.path.exists(meta_path):
                with open(meta_path) as f:
                    p = json.load(f)
                    if p.get('id') == project_id:
                        return jsonify(p)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404


# ============================================================
# VISUALX MAGIC ENDPOINTS
# ============================================================

@app.route('/api/magic/generate-prompts', methods=['POST'])
def magic_generate_prompts():
    """
    VisualX Magic Step 1: Generate all prompts via Creative Council.
    Returns prompts for user review before execution.
    """
    data = request.json
    project_id = data.get('project_id')
    engine = data.get('engine', 'rules')  # 'rules' or 'llm'
    artist_description = data.get('artist_description')
    emotion = data.get('emotion', 'auto')

    if not project_id:
        return jsonify({'error': 'project_id required'}), 400

    # Find project
    project = projects.get(project_id)
    if not project:
        for folder in os.listdir(OUTPUT_FOLDER):
            meta_path = os.path.join(OUTPUT_FOLDER, folder, 'project.json')
            if os.path.exists(meta_path):
                with open(meta_path) as f:
                    p = json.load(f)
                    if p.get('id') == project_id:
                        project = p
                        projects[project_id] = p
                        break

    if not project:
        return jsonify({'error': 'Project not found'}), 404

    if not project.get('analysis'):
        return jsonify({'error': 'Audio not analyzed yet. Call /api/analyze first.'}), 400

    try:
        analysis = project['analysis']
        genre = project['genre']
        title = project['title']
        bpm = analysis['bpm']
        sections = analysis['sections']

        # Create council
        council = CreativeCouncil(engine=engine)

        # Generate prompts for each section
        prompts = []
        for i, section in enumerate(sections):
            mode = 'performance' if section['name'] in ['drop', 'chorus'] else 'cinematic'
            energy = 0.8 if section['name'] in ['drop', 'chorus'] else 0.5

            image_prompt, motion_prompt = council.convene_council(
                song_title=title,
                genre=genre,
                bpm=bpm,
                analysis_data={'energy': energy, 'section': section['name']},
                mode=mode,
                artist_description=artist_description
            )

            prompts.append({
                'clip_number': i + 1,
                'section': section['name'],
                'start_time': section['start'],
                'end_time': section['end'],
                'mode': mode,
                'energy': energy,
                'visual_prompt': image_prompt,
                'motion_prompt': motion_prompt
            })

        # Save prompts
        prompts_data = {
            'project_id': project_id,
            'title': title,
            'genre': genre,
            'total_clips': len(prompts),
            'prompts': prompts,
            'generated_at': datetime.utcnow().isoformat(),
            'status': 'awaiting_approval'
        }

        prompts_path = os.path.join(project['project_path'], 'video_prompts.json')
        with open(prompts_path, 'w') as f:
            json.dump(prompts_data, f, indent=2)

        return jsonify({
            'success': True,
            'project_id': project_id,
            'total_clips': len(prompts),
            'prompts': prompts,
            'message': 'Prompts generated. Review and edit, then call /api/magic/execute'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/magic/prompts/<project_id>', methods=['GET'])
def get_magic_prompts(project_id):
    """Get generated prompts for a project."""
    for folder in os.listdir(OUTPUT_FOLDER):
        meta_path = os.path.join(OUTPUT_FOLDER, folder, 'project.json')
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                p = json.load(f)
                if p.get('id') == project_id:
                    prompts_path = os.path.join(OUTPUT_FOLDER, folder, 'video_prompts.json')
                    if os.path.exists(prompts_path):
                        with open(prompts_path) as pf:
                            return jsonify(json.load(pf))
                    return jsonify({'error': 'No prompts generated yet'}), 404
    return jsonify({'error': 'Project not found'}), 404


@app.route('/api/magic/prompts/<project_id>', methods=['PUT'])
def update_magic_prompts(project_id):
    """Update/edit prompts before execution."""
    data = request.json

    for folder in os.listdir(OUTPUT_FOLDER):
        meta_path = os.path.join(OUTPUT_FOLDER, folder, 'project.json')
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                p = json.load(f)
                if p.get('id') == project_id:
                    prompts_path = os.path.join(OUTPUT_FOLDER, folder, 'video_prompts.json')
                    if not os.path.exists(prompts_path):
                        return jsonify({'error': 'No prompts to update'}), 404

                    with open(prompts_path) as pf:
                        prompts_data = json.load(pf)

                    # Update specific prompt or all
                    if 'clip_number' in data:
                        for prompt in prompts_data['prompts']:
                            if prompt['clip_number'] == data['clip_number']:
                                if 'visual_prompt' in data:
                                    prompt['visual_prompt'] = data['visual_prompt']
                                if 'motion_prompt' in data:
                                    prompt['motion_prompt'] = data['motion_prompt']
                                break
                    elif 'prompts' in data:
                        prompts_data['prompts'] = data['prompts']

                    prompts_data['edited_at'] = datetime.utcnow().isoformat()
                    prompts_data['user_edited'] = True

                    with open(prompts_path, 'w') as pf:
                        json.dump(prompts_data, pf, indent=2)

                    return jsonify({'success': True, 'message': 'Prompts updated'})

    return jsonify({'error': 'Project not found'}), 404


@app.route('/api/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status."""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(jobs[job_id])


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



