import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: BASE_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export const authApi = {
  login: (email: string, password: string) =>
    api.post("/api/auth/login", { email, password }),
  register: (data: any) => api.post("/api/auth/register", data),
  me: () => api.get("/api/users/me"),
};

export const workflowApi = {
  list: () => api.get("/api/workflows/"),
  create: (data: any) => api.post("/api/workflows/", data),
  run: (id: string, input: any) => api.post(`/api/workflows/${id}/run`, { workflow_id: id, input_data: input }),
};

export const analyticsApi = {
  dashboard: () => api.get("/api/analytics/dashboard"),
};

export default api;
