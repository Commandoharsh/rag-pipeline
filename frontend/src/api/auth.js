import apiClient from "./client";

export async function register(email, password) {
    const response = await apiClient.post(
        "/auth/register",
        {
            email,
            password,
        }
    );

    return response.data;
}

export async function login(email, password) {
    const response = await apiClient.post(
        "/auth/login",
        {
            email,
            password,
        }
    );

    localStorage.setItem(
        "researchrag_token",
        response.data.access_token
    );

    return response.data;
}

export function logout() {
    localStorage.removeItem("researchrag_token");
}

export function getToken() {
    return localStorage.getItem("researchrag_token");
}