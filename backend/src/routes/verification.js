const express = require('express');
const router = express.Router();
const { 
  verifyProfile, 
  addVerificationSignature,
  getVerificationHistory,
  submitToBlockchain 
} = require('../services/verificationService');

/**
 * POST /api/verification/verify
 * Verify a learning profile
 */
router.post('/verify', async (req, res, next) => {
  try {
    const { profileId, schoolId, schoolName, verificationNotes, isVerified } = req.body;

    const verification = await verifyProfile({
      profileId,
      schoolId,
      schoolName,
      verificationNotes,
      isVerified,
      verificationDate: new Date()
    });

    res.status(201).json({
      success: true,
      verification,
      message: 'Profile verified'
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/verification/:verificationId/sign
 * Add cryptographic signature to verification
 */
router.post('/:verificationId/sign', async (req, res, next) => {
  try {
    const { schoolPrivateKey } = req.body;

    const signature = await addVerificationSignature(
      req.params.verificationId,
      schoolPrivateKey
    );

    res.status(200).json({
      success: true,
      signature,
      message: 'Verification signed'
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/verification/:profileId/history
 * Get verification history for a profile
 */
router.get('/:profileId/history', async (req, res, next) => {
  try {
    const history = await getVerificationHistory(req.params.profileId);

    res.status(200).json({
      success: true,
      history,
      totalVerifications: history.length
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/verification/:verificationId/blockchain
 * Submit verification to blockchain
 */
router.post('/:verificationId/blockchain', async (req, res, next) => {
  try {
    const blockchainRecord = await submitToBlockchain(req.params.verificationId);

    res.status(201).json({
      success: true,
      blockchainRecord,
      message: 'Verification submitted to blockchain',
      transactionHash: blockchainRecord.transactionHash,
      blockNumber: blockchainRecord.blockNumber
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
