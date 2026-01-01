require('dotenv').config();
const express = require('express');
const Stripe = require('stripe');
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios');
const path = require('path');
const { initDatabase } = require('./database');
const { signup, login, verify, authenticateToken } = require('./auth');
const EnginesClient = require('./engines_client');

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
