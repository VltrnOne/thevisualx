require('dotenv').config();
const express = require('express');
const Stripe = require('stripe');
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios');
const path = require('path');
const fs = require('fs');
const FormData = require('form-data');
const multer = require('multer');
const { initDatabase } = require('./database');
const { signup, login, verify, authenticateToken, authenticateAdmin, adminLogin, adminVerify } = require('./auth');
const { User } = require('./database');
const EnginesClient = require('./engines_client');

// Configure multer for audio file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + '-' + file.originalname);
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 50 * 1024 * 1024 }, // 50MB limit
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('audio/')) {
      cb(null, true);
    } else {
      cb(new Error('Only audio files are allowed'), false);
    }
  }
});

const app = express();
const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

// Initialize VISUALX Engines Client
const enginesClient = new EnginesClient(process.env.ENGINE_SERVICE_URL || 'http://localhost:5051');

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public')); // Serve static files from public directory

// Initialize database on startup
initDatabase().catch(err => {
  console.error('❌ Failed to initialize database:', err);
  process.exit(1);
});

// Authentication routes
app.post('/api/auth/signup', signup);
app.post('/api/auth/login', login);
app.get('/api/auth/verify', authenticateToken, verify);

// Admin authentication routes
app.post('/api/admin/login', adminLogin);
app.get('/api/admin/verify', authenticateToken, adminVerify);

// Admin API routes
app.get('/api/admin/users', authenticateAdmin, async (req, res) => {
  try {
    const users = await User.getAllUsers();
    res.json({ users });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});

app.get('/api/admin/stats', authenticateAdmin, async (req, res) => {
  try {
    const stats = await User.getStats();
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch stats' });
  }
});

app.put('/api/admin/users/:id/role', authenticateAdmin, async (req, res) => {
  try {
    const { role } = req.body;
    if (!['user', 'admin'].includes(role)) {
      return res.status(400).json({ error: 'Invalid role' });
    }
    await User.updateRole(req.params.id, role);
    res.json({ success: true, message: 'Role updated' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to update role' });
  }
});

app.put('/api/admin/users/:id/toggle', authenticateAdmin, async (req, res) => {
  try {
    const { is_active } = req.body;
    await User.toggleActive(req.params.id, is_active);
    res.json({ success: true, message: 'User status updated' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to update user status' });
  }
});

app.delete('/api/admin/users/:id', authenticateAdmin, async (req, res) => {
  try {
    // Prevent self-deletion
    if (parseInt(req.params.id) === req.user.id) {
      return res.status(400).json({ error: 'Cannot delete yourself' });
    }
    await User.deleteUser(req.params.id);
    res.json({ success: true, message: 'User deleted' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete user' });
  }
});

// Protected route example
app.get('/api/profile', authenticateToken, (req, res) => {
  res.json({
    message: 'Protected route accessed successfully',
    user: req.user
  });
});

// ============================================================
// VISUALX Engines API Routes
// ============================================================

// Health check for engine service
app.get('/api/engines/health', async (req, res) => {
  try {
    const health = await enginesClient.healthCheck();
    res.json(health);
  } catch (error) {
    res.status(503).json({ 
      status: 'error', 
      message: 'Engine service unavailable',
      error: error.message 
    });
  }
});

// Creative Council - Generate prompts
app.post('/api/engines/council/convene', authenticateToken, async (req, res) => {
  try {
    const result = await enginesClient.conveneCouncil(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// ColorBrain - Develop color look
app.post('/api/engines/colorbrain/develop', authenticateToken, async (req, res) => {
  try {
    const result = await enginesClient.developColorLook(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// ShotBrain - Design shot
app.post('/api/engines/shotbrain/design', authenticateToken, async (req, res) => {
  try {
    const result = await enginesClient.designShot(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// EditBrain - Analyze for cuts
app.post('/api/engines/editbrain/analyze', authenticateToken, async (req, res) => {
  try {
    const result = await enginesClient.analyzeForCuts(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// Orchestrator - Create visual package
app.post('/api/engines/orchestrator/create', authenticateToken, async (req, res) => {
  try {
    const result = await enginesClient.createVisualPackage(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// ImageBrain - Generate still images with agent research
app.post('/api/engines/imagebrain/research', authenticateToken, async (req, res) => {
  try {
    const result = await enginesClient.researchAudience(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.post('/api/engines/imagebrain/generate', authenticateToken, async (req, res) => {
  try {
    const result = await enginesClient.generateStillImages(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// ============================================================
// Audio Upload & Project Management Routes
// ============================================================

// Upload audio file
app.post('/api/engines/upload', authenticateToken, upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'No audio file provided' });
    }

    const { title, genre, artist_description } = req.body;

    if (!title) {
      return res.status(400).json({ success: false, error: 'Project title is required' });
    }

    // Forward to Python engine service
    const formData = new FormData();
    formData.append('file', fs.createReadStream(req.file.path), req.file.originalname);
    formData.append('title', title);
    formData.append('genre', genre || 'electronic');
    formData.append('artist_description', artist_description || '');
    formData.append('user_id', req.user.id.toString());

    const engineUrl = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';
    const response = await axios.post(`${engineUrl}/api/upload`, formData, {
      headers: {
        ...formData.getHeaders(),
        'Content-Length': formData.getLengthSync()
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });

    // Clean up the temporary file
    fs.unlink(req.file.path, (err) => {
      if (err) console.error('Failed to delete temp file:', err);
    });

    res.json(response.data);
  } catch (error) {
    console.error('Upload error:', error.message);
    // Clean up on error
    if (req.file && req.file.path) {
      fs.unlink(req.file.path, () => {});
    }
    res.status(500).json({
      success: false,
      error: error.response?.data?.error || error.message
    });
  }
});

// Analyze uploaded audio
app.post('/api/engines/analyze/:projectId', authenticateToken, async (req, res) => {
  try {
    const engineUrl = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';
    const response = await axios.post(`${engineUrl}/api/analyze/${req.params.projectId}`, {}, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    res.json(response.data);
  } catch (error) {
    console.error('Analysis error:', error.message);
    res.status(500).json({
      success: false,
      error: error.response?.data?.error || error.message
    });
  }
});

// Get all projects for user
app.get('/api/engines/projects', authenticateToken, async (req, res) => {
  try {
    const engineUrl = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';
    const response = await axios.get(`${engineUrl}/api/projects`, {
      params: { user_id: req.user.id }
    });
    res.json(response.data);
  } catch (error) {
    console.error('Projects fetch error:', error.message);
    res.json({ success: true, projects: [] }); // Return empty array on error
  }
});

// Get single project
app.get('/api/engines/project/:projectId', authenticateToken, async (req, res) => {
  try {
    const engineUrl = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';
    const response = await axios.get(`${engineUrl}/api/project/${req.params.projectId}`);
    res.json(response.data);
  } catch (error) {
    console.error('Project fetch error:', error.message);
    res.status(404).json({
      success: false,
      error: 'Project not found'
    });
  }
});

// VisualX Magic - Generate prompts
app.post('/api/engines/magic/generate-prompts', authenticateToken, async (req, res) => {
  try {
    const engineUrl = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';
    const response = await axios.post(`${engineUrl}/api/magic/generate-prompts`, req.body, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    res.json(response.data);
  } catch (error) {
    console.error('Magic prompts error:', error.message);
    res.status(500).json({
      success: false,
      error: error.response?.data?.error || error.message
    });
  }
});

// Get prompts for project
app.get('/api/engines/magic/prompts/:projectId', authenticateToken, async (req, res) => {
  try {
    const engineUrl = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';
    const response = await axios.get(`${engineUrl}/api/magic/prompts/${req.params.projectId}`);
    res.json(response.data);
  } catch (error) {
    console.error('Get prompts error:', error.message);
    res.status(500).json({
      success: false,
      error: error.response?.data?.error || error.message
    });
  }
});

// Update prompts for project
app.put('/api/engines/magic/prompts/:projectId', authenticateToken, async (req, res) => {
  try {
    const engineUrl = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';
    const response = await axios.put(`${engineUrl}/api/magic/prompts/${req.params.projectId}`, req.body, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    res.json(response.data);
  } catch (error) {
    console.error('Update prompts error:', error.message);
    res.status(500).json({
      success: false,
      error: error.response?.data?.error || error.message
    });
  }
});

// Get job status
app.get('/api/engines/job/:jobId', authenticateToken, async (req, res) => {
  try {
    const engineUrl = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';
    const response = await axios.get(`${engineUrl}/api/job/${req.params.jobId}`);
    res.json(response.data);
  } catch (error) {
    console.error('Job status error:', error.message);
    res.status(500).json({
      success: false,
      error: error.response?.data?.error || error.message
    });
  }
});

// Existing webhook routes
app.post('/new-client', async (req, res) => {
  const data = req.body;
  console.log('📦 Webhook received:', data);

  // Identify product from request
  const product = data?.display_items?.[0]?.custom?.name || data?.metadata?.product || 'UNKNOWN';

  const validPlans = [
    'DFY Premium Credit Kit',
    'Coaching',
    '88X GPT',
    'Daily',
    'Access Pass'
  ];

  // Forward all valid plans to Zapier
  if (validPlans.includes(product)) {
    console.log('✅ Valid plan detected, forwarding to Zapier...');
    try {
      await axios.post('https://hooks.zapier.com/hooks/catch/13608213/2n2c0ku/', data);
    } catch (err) {
      console.error('❌ Zapier Forwarding Error:', err.message);
    }
  } else {
    console.log('⚠️ Plan not recognized or ignored:', product);
  }

  res.status(200).send({ status: 'received', message: 'Client data logged.' });
});

app.post('/unlock-access', (req, res) => {
  const { email, plan } = req.body;
  console.log('🔓 Unlock Access Received:', email, plan);

  if (!email || !plan) {
    return res.status(400).send({ error: 'Missing email or plan' });
  }

  // Trigger custom access logic here
  res.status(200).send({ status: 'success', message: `Access unlocked for ${email} on ${plan}` });
});

// Serve HTML pages
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/signup', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'signup.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/about', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'about.html'));
});

app.get('/admin-login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'admin-login.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'admin.html'));
});

app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

// Engine-specific pages
app.get('/engine/council', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'engine-council.html'));
});

app.get('/engine/colorbrain', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'engine-colorbrain.html'));
});

app.get('/engine/shotbrain', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'engine-shotbrain.html'));
});

app.get('/engine/editbrain', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'engine-editbrain.html'));
});

app.get('/engine/orchestrator', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'engine-orchestrator.html'));
});

app.get('/engine/imagebrain', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'engine-imagebrain.html'));
});

// Project detail page
app.get('/project/:id', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'project.html'));
});

// Projects API routes
app.get('/api/projects', authenticateToken, async (req, res) => {
  // Return user's projects
  res.json({ projects: [], total: 0 });
});

app.post('/api/projects', authenticateToken, async (req, res) => {
  // Create new project
  const { name, description } = req.body;
  res.json({ success: true, project: { id: Date.now(), name, description } });
});

// Engine history/stats routes
app.get('/api/stats', authenticateToken, async (req, res) => {
  res.json({
    projects: 0,
    engineRuns: 0,
    assetsGenerated: 0
  });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
  console.log(`🌐 Visit http://localhost:${PORT} to view the site`);
});
