import apiClient from "./client";

export async function createConversation(
    title = "New Conversation"
) {
    const response = await apiClient.post(
        "/conversations",
        {
            title,
        }
    );

    return response.data.conversation;
}

export async function getConversations() {
    const response = await apiClient.get(
        "/conversations"
    );

    return response.data.conversations;
}

export async function getConversation(
    conversationId
) {
    const response = await apiClient.get(
        `/conversations/${conversationId}`
    );

    return response.data;
}

export async function deleteConversation(
    conversationId
) {
    await apiClient.delete(
        `/conversations/${conversationId}`
    );
}

export async function queryConversation(
    conversationId,
    question
) {
    const response = await apiClient.post(
        `/conversations/${conversationId}/query`,
        {
            question,
        }
    );

    return response.data;
}