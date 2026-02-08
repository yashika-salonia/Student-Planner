import axios from "axios";

const API_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_URL,
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    // Add token to all requests except login/register
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Handle 401 errors globally (token expiry or invalid)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

// Auth API for registration and login
export const authAPI = {
  register: (data) => axios.post(`${API_URL}/auth/register/`, data),
  LoginStep1: (data)=> axios.post(`${API_URL}/auth/login-step1/`,data),
  LoginStep2: (data)=> axios.post(`${API_URL}/auth/login-step2/`,data),
};

// Task API for CRUD operations on tasks
export const taskAPI = {
  getAll: () => api.get("/tasks/"),
  create: (data) => api.post("/tasks/", data),
  update: (id, data) => api.patch(`/tasks/${id}/`, data),
  delete: (id) => api.delete(`/tasks/${id}/`),
};

export default api;
