const express = require('express');
const router = express.Router();
const { 
  createProfile, 
  updateProfile, 
  getProfile,
  mergeDocuments 
} = require('../services/profileService');

/**
 * POST /api/profiles
 * Create a new learning profile from documents
 */
router.post('/', async (req, res, next) => {
  try {
    const { childName, childId, documentIds, sourceCountry } = req.body;

    if (!documentIds || documentIds.length === 0) {
      return res.status(400).json({ error: 'At least one document is required' });
    }

    const profile = await createProfile({
      childName,
      childId,
      documentIds,
      sourceCountry
    });

    res.status(201).json({
      success: true,
      profile,
      message: 'Learning profile created'
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/profiles/:profileId
 * Retrieve a learning profile with all reconstructed data
 */
router.get('/:profileId', async (req, res, next) => {
  try {
    const profile = await getProfile(req.params.profileId);

    if (!profile) {
      return res.status(404).json({ error: 'Profile not found' });
    }

    res.status(200).json({
      success: true,
      profile
    });
  } catch (error) {
    next(error);
  }
});

/**
 * PUT /api/profiles/:profileId
 * Update profile with corrections
 */
router.put('/:profileId', async (req, res, next) => {
  try {
    const { corrections, verifiedBy } = req.body;

    const updatedProfile = await updateProfile(req.params.profileId, {
      corrections,
      verifiedBy,
      verificationDate: new Date()
    });

    res.status(200).json({
      success: true,
      profile: updatedProfile,
      message: 'Profile updated'
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/profiles/:profileId/merge
 * Merge conflicting information from multiple documents
 */
router.post('/:profileId/merge', async (req, res, next) => {
  try {
    const { documentIds, strategy } = req.body; // strategy: 'confidence', 'latest', 'manual'

    const mergedProfile = await mergeDocuments(req.params.profileId, {
      documentIds,
      strategy
    });

    res.status(200).json({
      success: true,
      profile: mergedProfile,
      message: 'Documents merged successfully'
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
