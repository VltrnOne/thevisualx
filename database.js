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
        role TEXT DEFAULT 'user',
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
        // Add role column if it doesn't exist (for existing databases)
        db.run(`ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'`, (alterErr) => {
          // Ignore error if column already exists
          resolve(db);
        });
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
  },

  async findById(id) {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      db.get('SELECT id, email, name, role, created_at, last_login, is_active FROM users WHERE id = ?', [id], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row);
        }
      });
    });
  },

  async getAllUsers() {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      db.all('SELECT id, email, name, role, created_at, last_login, is_active FROM users ORDER BY created_at DESC', (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  },

  async updateRole(userId, role) {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      db.run(
        'UPDATE users SET role = ? WHERE id = ?',
        [role, userId],
        (err) => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        }
      );
    });
  },

  async toggleActive(userId, isActive) {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      db.run(
        'UPDATE users SET is_active = ? WHERE id = ?',
        [isActive ? 1 : 0, userId],
        (err) => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        }
      );
    });
  },

  async deleteUser(userId) {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      db.run('DELETE FROM users WHERE id = ?', [userId], (err) => {
        if (err) {
          reject(err);
        } else {
          resolve();
        }
      });
    });
  },

  async getStats() {
    const db = await getDatabase();
    return new Promise((resolve, reject) => {
      db.get(`
        SELECT
          COUNT(*) as total,
          SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) as admins,
          SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active,
          SUM(CASE WHEN date(created_at) = date('now') THEN 1 ELSE 0 END) as today
        FROM users
      `, (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row);
        }
      });
    });
  }
};

module.exports = { initDatabase, User };
