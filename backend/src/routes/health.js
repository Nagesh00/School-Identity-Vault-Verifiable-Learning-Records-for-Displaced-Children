const express = require('express');
const router = express.Router();

/**
 * GET /api/health
 * Health check endpoint
 */
router.get('/', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    service: 'School Identity Vault Backend',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

module.exports = router;
