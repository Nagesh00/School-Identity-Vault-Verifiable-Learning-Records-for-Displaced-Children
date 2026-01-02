require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const logger = require('./config/logger');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// Request logging
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.path}`);
  next();
});

// Routes
app.use('/api/documents', require('./routes/documents'));
app.use('/api/profiles', require('./routes/profiles'));
app.use('/api/verification', require('./routes/verification'));
app.use('/api/health', require('./routes/health'));

// Error handling
app.use((err, req, res, next) => {
  logger.error(err.message, err);
  res.status(err.status || 500).json({
    error: err.message,
    status: err.status || 500
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
app.listen(PORT, () => {
  logger.info(`School Identity Vault Backend running on port ${PORT}`);
});

module.exports = app;
