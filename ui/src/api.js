// Central place for reading the API base URL from the environment.
// Never hardcode URLs elsewhere in the app — import API_BASE_URL from here.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
