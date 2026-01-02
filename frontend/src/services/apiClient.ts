import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Documents API
export const documentsAPI = {
  upload: (file, metadata) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('documentType', metadata.documentType);
    formData.append('childId', metadata.childId);
    formData.append('sourceCountry', metadata.sourceCountry);

    return apiClient.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },

  getDocument: (documentId) => apiClient.get(`/documents/${documentId}`)
};

// Profiles API
export const profilesAPI = {
  create: (profileData) => apiClient.post('/profiles', profileData),
  get: (profileId) => apiClient.get(`/profiles/${profileId}`),
  update: (profileId, updates) => apiClient.put(`/profiles/${profileId}`, updates),
  merge: (profileId, mergeData) => apiClient.post(`/profiles/${profileId}/merge`, mergeData)
};

// Verification API
export const verificationAPI = {
  verify: (verificationData) => apiClient.post('/verification/verify', verificationData),
  addSignature: (verificationId, schoolPrivateKey) =>
    apiClient.post(`/verification/${verificationId}/sign`, { schoolPrivateKey }),
  getHistory: (profileId) => apiClient.get(`/verification/${profileId}/history`),
  submitToBlockchain: (verificationId) =>
    apiClient.post(`/verification/${verificationId}/blockchain`)
};

export default apiClient;
