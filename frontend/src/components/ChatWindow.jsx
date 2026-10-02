import { useEffect, useRef } from "react";

import Message from "./Message";

function ChatWindow({
    messages = [],
    loading = false,
}) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages, loading]);

    if (messages.length === 0 && !loading) {
        return (
            <div className="chat-empty">
                <div className="chat-empty-content">
                    <h1>ResearchRAG</h1>

                    <p>
                        Ask questions about your
                        indexed research documents.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="chat-window">
            <div className="messages-container">
                {messages.map((message) => (
                    <Message
                        key={message.id}
                        role={message.role}
                        content={message.content}
                        citations={
                            message.citations || []
                        }
                    />
                ))}

                {loading && (
                    <div className="message-row message-assistant">
                        <div className="message-icon">
                            🤖
                        </div>

                        <div className="message-body">
                            <div className="message-role">
                                ResearchRAG
                            </div>

                            <div className="typing-indicator">
                                <span />
                                <span />
                                <span />
                            </div>
                        </div>
                    </div>
                )}

                <div ref={bottomRef} />
            </div>
        </div>
    );
}

export default ChatWindow;