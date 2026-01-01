# VISUALX Engines

This directory contains the core VISUALX engines from the visual-x repository.

## Engines Included

- **CreativeCouncil** - Multi-agent prompt generation system
- **ColorBrain** - Intelligent color grading engine
- **ShotBrain** - AI shot designer and cinematography intelligence
- **EditBrain** - Rough cut engine for beat-synced editing
- **VISUALXOrchestrator** - Main orchestrator coordinating all agents

## Setup

### 1. Install Python Dependencies

```bash
cd engines
pip install -r requirements.txt
```

For full functionality, also install dependencies from the visual-x repository:
```bash
pip install -r ../visual-x-repo/requirements.txt
```

### 2. Start the Engine Service

```bash
python engine_service.py
```

The service will run on port 5051 by default (configurable via `ENGINE_SERVICE_PORT` env var).

## API Endpoints

The engine service exposes the following endpoints:

### Health Check
- `GET /health` - Service health check

### Creative Council
- `POST /api/council/convene` - Generate prompts using the Creative Council

### ColorBrain
- `POST /api/colorbrain/develop` - Develop master color look

### ShotBrain
- `POST /api/shotbrain/design` - Design a shot

### EditBrain
- `POST /api/editbrain/analyze` - Analyze audio for cut points

### Orchestrator
- `POST /api/orchestrator/create` - Create complete visual package

## Integration with Node.js

The engines are accessible via HTTP from the Express server. See `../server.js` for integration examples.



