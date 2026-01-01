const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = path.join(__dirname, 'users.db');

// Initialize database and create users table
function initDatabase() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, (err) => {
      if (err) {
        console.error('❌ Database connection error:', err.message);
        reject(err);
        return;
      }
      console.log('✅ Connected to SQLite database');
    });

    // Create users table if it doesn't exist
    db.run(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_login DATETIME,
        is_active INTEGER DEFAULT 1
      )
    `, (err) => {
      if (err) {
        console.error('❌ Table creation error:', err.message);
        reject(err);
      } else {
        console.log('✅ Users table ready');
        resolve(db);
      }
    });
  });
}

// Get database instance
function getDatabase() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, (err) => {
      if (err) {
        reject(err);
      } else {
        resolve(db);
      }
    });
  });
}

// User operations
const User = {
  async findByEmail(email) {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      db.get('SELECT * FROM users WHERE email = ?', [email], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row);
        }
      });
    });
  },

  async create(userData) {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      const { email, password, name } = userData;
      db.run(
        'INSERT INTO users (email, password, name) VALUES (?, ?, ?)',
        [email, password, name || null],
        function(err) {
          if (err) {
            reject(err);
          } else {
            resolve({ id: this.lastID, email, name });
          }
        }
      );
    });
  },

  async updateLastLogin(userId) {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      db.run(
        'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
        [userId],
        (err) => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        }
      );
    });
  }
};

module.exports = { initDatabase, User };
