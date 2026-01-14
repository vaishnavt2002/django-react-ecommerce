import axios from "axios";
import { refreshToken } from "./auth";

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    },
    withCredentials: true,
});

let isRefreshing = false
let failedQueue = [];

const processQueue = (error=null)=>{
    failedQueue.forEach(({resolve, reject})=>{
        if(error){
            reject(error);
        } else {
            resolve();
        }
    });
    failedQueue = [];
}

apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if(error.response?.status != 401){
            const message =
            error.response?.data?.error ||
            error.response?.data?.message ||
            "Something went wrong";

            return Promise.reject(new Error(message))
        }
        if (originalRequest._retry) {
            return Promise.reject(error);
        }
        originalRequest._retry = true;

        if (isRefreshing){
            return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject });
        })
        .then(() => apiClient(originalRequest))
        .catch((err) => Promise.reject(err));
        }
        isRefreshing = true;

        try {
            await refreshToken();
            processQueue();
            return apiClient(originalRequest);
        } catch (refreshError) {
            processQueue(refreshError);
            return Promise.reject(refreshError);
        } finally {
            isRefreshing = false;
        }
    }
);

export default apiClient