import apiClient from "./client";

export async function getDocuments() {

    const response =
        await apiClient.get(
            "/documents"
        );

    return response.data;
}