import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import {
    createConversation,
    getConversations,
    getConversation,
    deleteConversation,
    queryConversation,
} from "../api/conversations";

import { logout } from "../api/auth";

function Chat({ user, onLogout }) {

    const [
        conversations,
        setConversations
    ] = useState([]);

    const [
        activeConversation,
        setActiveConversation
    ] = useState(null);

    const [
        messages,
        setMessages
    ] = useState([]);

    const [
        citations,
        setCitations
    ] = useState([]);

    const [
        loading,
        setLoading
    ] = useState(false);

    useEffect(() => {
        loadConversations();
    }, []);

    async function loadConversations() {

        try {

            const data =
                await getConversations();

            setConversations(data);

            if (data.length > 0) {
                await selectConversation(
                    data[0].id
                );
            }

        } catch (error) {
            console.error(error);
            
        }
    }

    async function selectConversation(id) {

        const data =
            await getConversation(id);

        setActiveConversation(id);

        setMessages(
            data.messages || []
        );

        setCitations([]);
    }

    async function handleCreateConversation() {

        const conversation =
            await createConversation();

        setConversations(
            (current) => [
                conversation,
                ...current
            ]
        );

        setActiveConversation(
            conversation.id
        );

        setMessages([]);

        setCitations([]);
    }

    async function handleDeleteConversation(id) {

        await deleteConversation(id);

        const remaining =
            conversations.filter(
                (conversation) =>
                    conversation.id !== id
            );

        setConversations(remaining);

        if (
            activeConversation === id
        ) {

            setActiveConversation(null);
            setMessages([]);
            setCitations([]);

            if (remaining.length > 0) {
                await selectConversation(
                    remaining[0].id
                );
            }
        }
    }

    async function handleSend(question) {

        if (!activeConversation) {

            const conversation =
                await createConversation(
                    question.slice(0, 50)
                );

            setConversations(
                (current) => [
                    conversation,
                    ...current
                ]
            );

            setActiveConversation(
                conversation.id
            );

            await sendQuestion(
                conversation.id,
                question
            );

            return;
        }

        await sendQuestion(
            activeConversation,
            question
        );
    }

    async function sendQuestion(
        conversationId,
        question
    ) {

        setLoading(true);

        try {

            const result =
                await queryConversation(
                    conversationId,
                    question
                );

            setMessages(
                (current) => [
                    ...current,
                    {
                        id:
                            result.messages.user.id,
                        role: "user",
                        content: question,
                    },
                    {
                        id:
                            result.messages.assistant.id,
                        role: "assistant",
                        content: result.answer,
                    }
                ]
            );

            setCitations(
                result.citations || []
            );

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);
        }
    }

    function handleLogout() {

        logout();
        onLogout();
    }

    return (
        <div className="chat-page">

            <Sidebar
                conversations={conversations}
                activeConversation={
                    activeConversation
                }
                onSelect={
                    selectConversation
                }
                onCreate={
                    handleCreateConversation
                }
                onDelete={
                    handleDeleteConversation
                }
            />

            <main className="chat-main">

                <header className="chat-header">

                    <div>
                        <strong>
                            ResearchRAG
                        </strong>

                        <span>
                            {user?.email}
                        </span>
                    </div>

                    <button
                        onClick={handleLogout}
                    >
                        Logout
                    </button>

                </header>

                <ChatWindow
                    messages={messages}
                    citations={citations}
                    loading={loading}
                />

                <ChatInput
                    onSend={handleSend}
                    disabled={loading}
                />

            </main>

        </div>
    );
}

export default Chat;