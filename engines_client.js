/**
 * VISUALX Engines Client
 * Node.js client for communicating with the Python engine service
 */

const axios = require('axios');

const ENGINE_SERVICE_URL = process.env.ENGINE_SERVICE_URL || 'http://localhost:5051';

class EnginesClient {
    constructor(baseURL = ENGINE_SERVICE_URL) {
        this.baseURL = baseURL;
    }

    /**
     * Check if the engine service is healthy
     */
    async healthCheck() {
        try {
            const response = await axios.get(`${this.baseURL}/health`);
            return response.data;
        } catch (error) {
            throw new Error(`Engine service health check failed: ${error.message}`);
        }
    }

    /**
     * Convene the Creative Council to generate prompts
     */
    async conveneCouncil({
        song_title,
        genre = 'electronic',
        bpm = 120,
        analysis_data = {},
        mode = 'cinematic',
        artist_description = null,
        project_context = null,
        engine = 'rules'
    }) {
        try {
            const response = await axios.post(`${this.baseURL}/api/council/convene`, {
                song_title,
                genre,
                bpm,
                analysis_data,
                mode,
                artist_description,
                project_context,
                engine
            });
            return response.data;
        } catch (error) {
            throw new Error(`Creative Council failed: ${error.message}`);
        }
    }

    /**
     * Develop a master color look using ColorBrain
     */
    async developColorLook({
        genre = 'electronic',
        emotion = 'serene',
        custom_style = null,
        key_color = null
    }) {
        try {
            const response = await axios.post(`${this.baseURL}/api/colorbrain/develop`, {
                genre,
                emotion,
                custom_style,
                key_color
            });
            return response.data;
        } catch (error) {
            throw new Error(`ColorBrain failed: ${error.message}`);
        }
    }

    /**
     * Design a shot using ShotBrain
     */
    async designShot({
        genre = 'electronic',
        style = 'cinematic',
        energy_level = 0.5,
        beat_position = 'verse',
        duration = 5.0,
        emotional_goal = null,
        context = ''
    }) {
        try {
            const response = await axios.post(`${this.baseURL}/api/shotbrain/design`, {
                genre,
                style,
                energy_level,
                beat_position,
                duration,
                emotional_goal,
                context
            });
            return response.data;
        } catch (error) {
            throw new Error(`ShotBrain failed: ${error.message}`);
        }
    }

    /**
     * Analyze audio for cut points using EditBrain
     */
    async analyzeForCuts({
        genre = 'electronic',
        bpm = 120.0,
        duration = 180.0,
        energy_curve = [],
        sections = []
    }) {
        try {
            const response = await axios.post(`${this.baseURL}/api/editbrain/analyze`, {
                genre,
                bpm,
                duration,
                energy_curve,
                sections
            });
            return response.data;
        } catch (error) {
            throw new Error(`EditBrain failed: ${error.message}`);
        }
    }

    /**
     * Create a complete visual package using the orchestrator
     */
    async createVisualPackage({
        title = 'Untitled',
        genre = 'electronic',
        style = 'cinematic',
        audio_analysis = {},
        target_platforms = ['youtube'],
        output_dir = './output'
    }) {
        try {
            const response = await axios.post(`${this.baseURL}/api/orchestrator/create`, {
                title,
                genre,
                style,
                audio_analysis,
                target_platforms,
                output_dir
            });
            return response.data;
        } catch (error) {
            throw new Error(`Orchestrator failed: ${error.message}`);
        }
    }
}

module.exports = EnginesClient;



