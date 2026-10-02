import { useState } from "react";

import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import Documents from "./Documents";
import Monitoring from "./Monitoring";

import {
    createConversation,
    getConversation,
    queryConversation,
} from "../api/conversations";


function generateConversationTitle(question) {
    const cleaned = question.trim();

    if (!cleaned) {
        return "New Conversation";
    }

    if (cleaned.length <= 40) {
        return cleaned;
    }

    return `${cleaned.substring(0, 40)}...`;
}


function Chat({
    user,
    onLogout,
}) {
    const [conversationId, setConversationId] =
        useState(null);

    const [messages, setMessages] =
        useState([]);

    const [loading, setLoading] =
        useState(false);

    const [page, setPage] =
        useState("chat");


    /*
     * Load an existing conversation
     */
    async function loadConversation(id) {
        if (!id) {
            setConversationId(null);
            setMessages([]);
            setPage("chat");
            return;
        }

        try {
            setLoading(true);

            const data =
                await getConversation(id);

            setConversationId(id);

            /*
             * Backend may return messages directly
             * or inside a conversation object.
             */
            const conversationMessages =
                data.messages ||
                data.conversation?.messages ||
                [];

            setMessages(
                conversationMessages.map(
                    (message) => ({
                        id: message.id,
                        role: message.role,
                        content:
                            message.content,
                        citations:
                            message.citations ||
                            [],
                    })
                )
            );

            setPage("chat");
        } catch (error) {
            console.error(
                "Failed to load conversation:",
                error
            );

            setMessages([
                {
                    id: `error-${Date.now()}`,
                    role: "assistant",
                    content:
                        error.response?.data
                            ?.detail ||
                        "Failed to load this conversation.",
                    citations: [],
                },
            ]);
        } finally {
            setLoading(false);
        }
    }


    /*
     * Create a new conversation from the sidebar
     */
    function handleConversationCreated(
        conversation
    ) {
        setConversationId(
            conversation.id
        );

        setMessages([]);

        setPage("chat");
    }


    /*
     * Select an existing conversation
     */
    function handleConversationSelect(id) {
        loadConversation(id);
    }


    /*
     * Send a question to ResearchRAG
     */
    async function handleSend(question) {
        if (loading) {
            return;
        }

        const cleanedQuestion =
            question.trim();

        if (!cleanedQuestion) {
            return;
        }

        let activeConversationId =
            conversationId;

        try {
            setLoading(true);

            /*
             * If the user sends a question before
             * creating a conversation, create one
             * automatically.
             */
            if (!activeConversationId) {
                const conversation =
                    await createConversation(
                        generateConversationTitle(
                            cleanedQuestion
                        )
                    );

                activeConversationId =
                    conversation.id;

                setConversationId(
                    activeConversationId
                );

                setPage("chat");
            }


            /*
             * Show the user's message immediately.
             */
            const temporaryMessage = {
                id: `user-${Date.now()}`,
                role: "user",
                content:
                    cleanedQuestion,
                citations: [],
            };

            setMessages((previous) => [
                ...previous,
                temporaryMessage,
            ]);


            /*
             * Send the question to the
             * conversation RAG endpoint.
             */
            const result =
                await queryConversation(
                    activeConversationId,
                    cleanedQuestion
                );


            /*
             * Add the RAG answer.
             */
            const assistantMessage = {
                id:
                    result.message_id ||
                    `assistant-${Date.now()}`,

                role: "assistant",

                content:
                    result.answer ||
                    "ResearchRAG did not return an answer.",

                citations:
                    result.citations ||
                    [],
            };


            setMessages((previous) => [
                ...previous,
                assistantMessage,
            ]);
        } catch (error) {
            console.error(
                "RAG query failed:",
                error
            );

            const errorMessage = {
                id: `error-${Date.now()}`,

                role: "assistant",

                content:
                    error.response?.data
                        ?.detail ||
                    "Something went wrong while processing your question.",

                citations: [],
            };

            setMessages((previous) => [
                ...previous,
                errorMessage,
            ]);
        } finally {
            setLoading(false);
        }
    }


    /*
     * Start a completely new conversation.
     */
    function handleNewConversation(
        conversation
    ) {
        setConversationId(
            conversation.id
        );

        setMessages([]);

        setPage("chat");
    }


    /*
     * Navigate to Documents.
     */
    function handleDocuments() {
        setPage("documents");
    }


    /*
     * Navigate to Monitoring.
     */
    function handleMonitoring() {
        setPage("monitoring");
    }


    /*
     * Main application UI
     */
    return (
        <div className="app-shell">

            {/* =========================
                SIDEBAR
            ========================= */}

            <Sidebar
                activeConversationId={
                    conversationId
                }

                onConversationSelect={
                    handleConversationSelect
                }

                onConversationCreated={
                    handleNewConversation
                }

                onDocuments={
                    handleDocuments
                }

                onMonitoring={
                    handleMonitoring
                }
            />


            {/* =========================
                MAIN APPLICATION
            ========================= */}

            <main className="main-area">

                {/* =========================
                    TOP BAR
                ========================= */}

                <header className="topbar">

                    <div className="topbar-title">
                        {page === "chat" &&
                            "ResearchRAG"}

                        {page ===
                            "documents" &&
                            "Documents"}

                        {page ===
                            "monitoring" &&
                            "Monitoring"}
                    </div>


                    <div className="topbar-right">

                        {user?.email && (
                            <span className="user-email">
                                {user.email}
                            </span>
                        )}

                        <button
                            className="logout-button"
                            onClick={onLogout}
                        >
                            Logout
                        </button>

                    </div>

                </header>


                {/* =========================
                    CHAT PAGE
                ========================= */}

                {page === "chat" && (
                    <>
                        <ChatWindow
                            messages={
                                messages
                            }

                            loading={
                                loading
                            }
                        />

                        <div className="chat-input-wrapper">

                            <ChatInput
                                onSend={
                                    handleSend
                                }

                                disabled={
                                    loading
                                }
                            />

                        </div>
                    </>
                )}


                {/* =========================
                    DOCUMENTS PAGE
                ========================= */}

                {page ===
                    "documents" && (
                    <Documents />
                )}


                {/* =========================
                    MONITORING PAGE
                ========================= */}

                {page ===
                    "monitoring" && (
                    <Monitoring />
                )}

            </main>

        </div>
    );
}


export default Chat;