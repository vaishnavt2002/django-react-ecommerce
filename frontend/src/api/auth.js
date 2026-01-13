const BASE_URL = import.meta.env.VITE_API_BASE_URL
import apiClient from "./client"

export async function registerUser(email, password) {
    const response = await apiClient.post("api/auth/register/", {
        email, password
    });

    return response.data
}

export async function  verifyOtp(verification_id, otp) {
    const response = await apiClient.post("api/auth/verify-otp/", {
        verification_id: verification_id,
        otp
    });
}

export async function login(email, password){
    const response = await apiClient.post("api/auth/login/", {
        email,
        password
    });
    return response.data
}

export async function refreshToken() {
    await apiClient.post("api/auth/refresh/");
}