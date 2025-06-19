import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export async function enerateMappingReportg(formData) {
  try {
    const response = await apiClient.post('/generate-mapping', formData);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to generate mapping report');
  }
}

export default {
  generateMappingReport
};
