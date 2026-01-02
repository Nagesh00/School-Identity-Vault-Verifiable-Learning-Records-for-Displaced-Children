const express = require('express');
const router = express.Router();
const multer = require('multer');
const { processDocument } = require('../services/documentService');

const upload = multer({ 
  limits: { fileSize: 50 * 1024 * 1024 },
  storage: multer.memoryStorage()
});

/**
 * POST /api/documents/upload
 * Upload and process a school document (photo of certificate, report card, etc.)
 */
router.post('/upload', upload.single('file'), async (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file provided' });
    }

    const documentData = {
      filename: req.file.originalname,
      mimetype: req.file.mimetype,
      buffer: req.file.buffer,
      uploadedBy: req.body.uploadedBy || 'anonymous',
      metadata: {
        type: req.body.documentType || 'unknown', // certificate, report_card, id, handwritten_note
        childId: req.body.childId,
        sourceCountry: req.body.sourceCountry,
        uploadDate: new Date()
      }
    };

    // Process document with AI (returns OCR + extracted data)
    const processedData = await processDocument(documentData);

    res.status(200).json({
      success: true,
      documentId: processedData.documentId,
      ocrText: processedData.ocrText,
      extractedData: processedData.extractedData,
      confidence: processedData.confidence,
      message: 'Document processed successfully'
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/documents/:documentId
 * Retrieve processed document details
 */
router.get('/:documentId', async (req, res, next) => {
  try {
    // TODO: Implement document retrieval from database
    res.status(200).json({
      documentId: req.params.documentId,
      message: 'Document retrieval - implementation pending'
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
