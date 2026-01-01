# VISUALX Engines Usage Guide

This guide shows how to use the VISUALX engines via the API.

## Prerequisites

1. Start the Python engine service:
   ```bash
   ./start_engines.sh
   ```

2. Start the Node.js server:
   ```bash
   npm start
   ```

3. Authenticate to get a JWT token (see main README for auth endpoints)

## Example Usage

### 1. Creative Council - Generate Prompts

Generate unique prompts for video generation:

```javascript
const response = await fetch('/api/engines/council/convene', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    song_title: 'Midnight Drive',
    genre: 'Hip Hop',
    bpm: 95,
    mode: 'cinematic',  // or 'performance'
    engine: 'rules'     // or 'llm', 'claude', 'openai'
  })
});

const { image_prompt, motion_prompt } = await response.json();
console.log('Image Prompt:', image_prompt);
console.log('Motion Prompt:', motion_prompt);
```

### 2. ColorBrain - Develop Color Look

Create a master color grade:

```javascript
const response = await fetch('/api/engines/colorbrain/develop', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    genre: 'electronic',
    emotion: 'euphoric',  // euphoric, melancholic, aggressive, serene, etc.
    custom_style: 'neon',  // optional: blockbuster, indie, vintage, neon, etc.
    key_color: '#ff00ff'  // optional: hex color
  })
});

const { grade_spec, color_palette } = await response.json();
console.log('Color Grade:', grade_spec);
console.log('Palette:', color_palette);
```

### 3. ShotBrain - Design Shot

Design a cinematic shot:

```javascript
const response = await fetch('/api/engines/shotbrain/design', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    genre: 'electronic',
    style: 'cinematic',
    energy_level: 0.8,      // 0.0 to 1.0
    beat_position: 'chorus', // verse, chorus, bridge, drop, intro, outro
    duration: 5.0,
    emotional_goal: 'triumph', // optional
    context: 'Main chorus section'
  })
});

const { output } = await response.json();
console.log('Shot Design:', output);
```

### 4. EditBrain - Analyze for Cuts

Analyze audio and determine optimal cut points:

```javascript
const response = await fetch('/api/engines/editbrain/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    genre: 'electronic',
    bpm: 128.0,
    duration: 180.0,  // seconds
    energy_curve: [0.5, 0.6, 0.8, 0.9, 0.7, ...], // array of 0-1 values
    sections: [
      { type: 'intro', start: 0, duration: 15, energy: 0.4 },
      { type: 'verse', start: 15, duration: 30, energy: 0.6 },
      { type: 'chorus', start: 45, duration: 30, energy: 0.9 },
      // ...
    ]
  })
});

const { cut_points, stats } = await response.json();
console.log('Cut Points:', cut_points);
console.log('Edit Stats:', stats);
```

### 5. Orchestrator - Create Complete Visual Package

Create a full visual package with all engines:

```javascript
const response = await fetch('/api/engines/orchestrator/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    title: 'My Music Video',
    genre: 'electronic',
    style: 'cinematic',
    audio_analysis: {
      bpm: 128,
      duration: 180,
      sections: [
        { type: 'intro', start: 0, duration: 15, energy: 0.4 },
        { type: 'verse', start: 15, duration: 30, energy: 0.6 },
        { type: 'chorus', start: 45, duration: 30, energy: 0.9 }
      ],
      beats: [0, 0.5, 1.0, 1.5, ...], // beat timestamps
      energy_curve: [0.4, 0.5, 0.6, ...] // energy over time
    },
    target_platforms: ['youtube', 'instagram_reels'],
    output_dir: './output'
  })
});

const { package } = await response.json();
console.log('Visual Package:', package);
// Includes: shots, edit_decisions, color_palette, prompts, delivery_packages
```

## Available Options

### Emotions (for ColorBrain)
- `euphoric`, `melancholic`, `aggressive`, `serene`, `mysterious`, `romantic`, `dark`, `triumphant`, `anxious`, `nostalgic`

### Look Styles (for ColorBrain)
- `blockbuster`, `indie`, `vintage`, `neon`, `noir`, `natural`, `dream`, `gritty`, `pastel`, `moody`

### Beat Positions (for ShotBrain/EditBrain)
- `verse`, `chorus`, `bridge`, `drop`, `intro`, `outro`, `breakdown`

### Platforms (for Orchestrator)
- `tiktok`, `youtube`, `youtube_shorts`, `instagram_reels`, `instagram_feed`, `theatrical`, `streaming_4k`, `broadcast`

### Creative Engines (for Creative Council)
- `rules` - Rule-based generation (fast, no API keys needed)
- `llm` - Auto-detect available LLM (Claude or GPT-4o)
- `claude` - Use Claude Sonnet 4 (requires ANTHROPIC_API_KEY)
- `openai` - Use GPT-4o (requires OPENAI_API_KEY)

## Error Handling

All endpoints return errors in this format:

```javascript
{
  success: false,
  error: "Error message here"
}
```

Common errors:
- `503` - Engine service unavailable (check if Python service is running)
- `500` - Engine processing error (check request parameters)
- `401` - Authentication required (provide valid JWT token)



