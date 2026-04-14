import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/magic/api";

export const http = axios.create({
  baseURL,
  timeout: 20000
});

http.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg = err?.response?.data?.detail || err?.response?.data?.error || err?.message || "Request failed";
    return Promise.reject(new Error(msg));
  }
);
