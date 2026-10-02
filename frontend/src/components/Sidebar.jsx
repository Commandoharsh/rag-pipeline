import { useEffect, useState } from "react";
import {
    Plus,
    MessageSquare,
    FileText,
    Activity,
    Trash2,
} from "lucide-react";

import {
    createConversation,
    getConversations,
    deleteConversation,
} from "../api/conversations";

function Sidebar({
    activeConversationId,
    onConversationSelect,
    onConversationCreated,
    onDocuments,
    onMonitoring,
}) {
    const [conversations, setConversations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [creating, setCreating] = useState(false);

    async function loadConversations() {
        try {
            setLoading(true);

            const data = await getConversations();

            setConversations(data || []);
        } catch (error) {
            console.error(
                "Failed to load conversations:",
                error
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadConversations();
    }, []);

    async function handleNewConversation() {
        if (creating) {
            return;
        }

        try {
            setCreating(true);

            const conversation =
                await createConversation(
                    "New Conversation"
                );

            setConversations((previous) => [
                conversation,
                ...previous,
            ]);

            onConversationCreated(conversation);
        } catch (error) {
            console.error(
                "Failed to create conversation:",
                error
            );
        } finally {
            setCreating(false);
        }
    }

    async function handleDelete(
        event,
        conversationId
    ) {
        event.stopPropagation();

        const confirmed = window.confirm(
            "Delete this conversation?"
        );

        if (!confirmed) {
            return;
        }

        try {
            await deleteConversation(
                conversationId
            );

            setConversations((previous) =>
                previous.filter(
                    (conversation) =>
                        conversation.id !==
                        conversationId
                )
            );

            if (
                activeConversationId ===
                conversationId
            ) {
                onConversationSelect(null);
            }
        } catch (error) {
            console.error(
                "Failed to delete conversation:",
                error
            );
        }
    }

    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="brand">
                    ResearchRAG
                </div>

                <button
                    className="new-chat-button"
                    onClick={handleNewConversation}
                    disabled={creating}
                    title="New conversation"
                >
                    <Plus size={21} />
                </button>
            </div>

            <div className="sidebar-section">
                <div className="sidebar-section-title">
                    Conversations
                </div>

                <div className="conversation-list">
                    {loading && (
                        <div className="sidebar-empty">
                            Loading...
                        </div>
                    )}

                    {!loading &&
                        conversations.length === 0 && (
                            <div className="sidebar-empty">
                                No conversations yet.
                            </div>
                        )}

                    {!loading &&
                        conversations.map(
                            (conversation) => (
                                <div
                                    key={
                                        conversation.id
                                    }
                                    className={`conversation-item ${
                                        activeConversationId ===
                                        conversation.id
                                            ? "active"
                                            : ""
                                    }`}
                                    onClick={() =>
                                        onConversationSelect(
                                            conversation.id
                                        )
                                    }
                                >
                                    <MessageSquare
                                        size={16}
                                    />

                                    <span className="conversation-title">
                                        {
                                            conversation.title
                                        }
                                    </span>

                                    <button
                                        className="delete-conversation"
                                        onClick={(event) =>
                                            handleDelete(
                                                event,
                                                conversation.id
                                            )
                                        }
                                        title="Delete conversation"
                                    >
                                        <Trash2
                                            size={14}
                                        />
                                    </button>
                                </div>
                            )
                        )}
                </div>
            </div>

            <div className="sidebar-bottom">
                <button
                    className="sidebar-nav-button"
                    onClick={onDocuments}
                >
                    <FileText size={18} />
                    <span>Documents</span>
                </button>

                <button
                    className="sidebar-nav-button"
                    onClick={onMonitoring}
                >
                    <Activity size={18} />
                    <span>Monitoring</span>
                </button>
            </div>
        </aside>
    );
}

export default Sidebar;