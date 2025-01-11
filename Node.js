const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const app = express();

app.use(express.json());

// Example User Database (use real DB in production)
let users = [];

// Register
app.post('/register', async (req, res) => {
  const { email, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);
  users.push({ email, password: hashedPassword, balance: 0 });
  res.status(201).send('User registered!');
});

// Login
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = users.find(user => user.email === email);
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).send('Invalid credentials');
  }
  const token = jwt.sign({ email }, 'secretKey', { expiresIn: '1h' });
  res.json({ token });
});

// Middleware to verify token
const authenticate = (req, res, next) => {
  const token = req.headers['authorization'];
  if (!token) return res.status(401).send('Access denied');
  jwt.verify(token, 'secretKey', (err, user) => {
    if (err) return res.status(403).send('Invalid token');
    req.user = user;
    next();
  });
};

// Protected Route
app.get('/dashboard', authenticate, (req, res) => {
  res.send('Welcome to your dashboard!');
});

app.listen(3000, () => console.log('Server running on port 3000'));
