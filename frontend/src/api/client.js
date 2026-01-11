import axios from "axios";

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    }
});

apiClient.interceptors.request.use(
    (response) => response,
    (error) => {
        const message =
        error.response?.data?.error ||
        error.response?.date?.message ||
        "Something went wrong";

        return Promise.reject(new Error(message))
    }
);

export default apiClient