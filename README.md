# thevisualx.com - VISUALX Platform

Complete authentication system and VISUALX AI engines integration for thevisualx.com.

## Features

### Authentication System
- ✅ User signup with email and password
- ✅ Secure password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ Login with email/password
- ✅ Protected routes with authentication middleware
- ✅ SQLite database for user storage
- ✅ Modern, responsive UI

### VISUALX Engines
- ✅ **Creative Council** - Multi-agent prompt generation system
- ✅ **ColorBrain** - Intelligent color grading engine
- ✅ **ShotBrain** - AI shot designer and cinematography intelligence
- ✅ **EditBrain** - Rough cut engine for beat-synced editing
- ✅ **VISUALX Orchestrator** - Complete visual package creation

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
PORT=8080
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=7d
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# VISUALX Engine Service (optional, defaults shown)
ENGINE_SERVICE_URL=http://localhost:5051
```

**Important:** Change `JWT_SECRET` to a strong random string in production!

### 3. Set Up VISUALX Engines (Python Service)

The engines require Python 3.8+. Set up the Python environment:

```bash
# Start the engine service (creates venv and installs dependencies)
./start_engines.sh
```

Or manually:
```bash
cd engines
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 engine_service.py
```

The engine service runs on `http://localhost:5051` by default.

**Note:** For full functionality, you may also want to install the complete requirements from the visual-x repository.

### 4. Start the Node.js Server

```bash
npm start
```

For development with auto-reload:

```bash
npm run dev
```

The server will start on `http://localhost:8080`

**Important:** Make sure the Python engine service is running before using the engine API endpoints!

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Create a new user account
  - Body: `{ email, password, name? }`
  - Returns: `{ token, user }`

- `POST /api/auth/login` - Login with email and password
  - Body: `{ email, password }`
  - Returns: `{ token, user }`

- `GET /api/auth/verify` - Verify JWT token (requires Authorization header)
  - Headers: `Authorization: Bearer <token>`
  - Returns: `{ valid, user }`

### Protected Routes

- `GET /api/profile` - Get user profile (requires authentication)
  - Headers: `Authorization: Bearer <token>`

### VISUALX Engines API

All engine endpoints require authentication (JWT token).

- `GET /api/engines/health` - Check engine service health
  - Returns: `{ status, service }`

- `POST /api/engines/council/convene` - Generate prompts using Creative Council
  - Body: `{ song_title, genre, bpm, mode?, engine?, analysis_data?, artist_description?, project_context? }`
  - Returns: `{ success, image_prompt, motion_prompt }`

- `POST /api/engines/colorbrain/develop` - Develop master color look
  - Body: `{ genre, emotion, custom_style?, key_color? }`
  - Returns: `{ success, grade_spec, color_palette }`

- `POST /api/engines/shotbrain/design` - Design a shot
  - Body: `{ genre, style, energy_level, beat_position, duration?, emotional_goal?, context? }`
  - Returns: `{ success, output }`

- `POST /api/engines/editbrain/analyze` - Analyze audio for cut points
  - Body: `{ genre, bpm, duration, energy_curve, sections }`
  - Returns: `{ success, cut_points, stats }`

- `POST /api/engines/orchestrator/create` - Create complete visual package
  - Body: `{ title, genre, style, audio_analysis, target_platforms, output_dir }`
  - Returns: `{ success, package }`

## Frontend Pages

- `/` - Home page (shows login/signup buttons or user info if logged in)
- `/signup` - User registration page
- `/login` - User login page

## Database

The system uses SQLite with a `users` table that includes:
- `id` - Primary key
- `email` - Unique email address
- `password` - Hashed password
- `name` - User's name (optional)
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp
- `is_active` - Account status flag

Database file: `users.db` (created automatically)

## Security Features

- Passwords are hashed using bcrypt with salt rounds
- JWT tokens expire after 7 days (configurable)
- Protected routes require valid JWT token
- CORS enabled for cross-origin requests
- Input validation on signup/login

## Usage Example

### Signup
```javascript
const response = await fetch('/api/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securepassword123',
    name: 'John Doe'
  })
});
const { token, user } = await response.json();
localStorage.setItem('token', token);
```

### Login
```javascript
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securepassword123'
  })
});
const { token, user } = await response.json();
localStorage.setItem('token', token);
```

### Access Protected Route
```javascript
const token = localStorage.getItem('token');
const response = await fetch('/api/profile', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const data = await response.json();
```

## Deployment

1. Set environment variables on your hosting platform
2. Ensure `JWT_SECRET` is set to a strong random value
3. The database file (`users.db`) will be created automatically
4. Make sure Node.js version 14+ is available

## Notes

- Tokens are stored in localStorage on the frontend
- Passwords must be at least 6 characters
- Email addresses must be unique
- The database is created automatically on first run
