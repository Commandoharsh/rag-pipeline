import { useState } from "react";
import { Send } from "lucide-react";

function ChatInput({ onSend, disabled = false }) {
    const [message, setMessage] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();

        const question = message.trim();

        if (!question || disabled) {
            return;
        }

        setMessage("");

        await onSend(question);
    }

    function handleKeyDown(event) {
        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {
            event.preventDefault();

            event.currentTarget.form?.requestSubmit();
        }
    }

    return (
        <form
            className="chat-input-container"
            onSubmit={handleSubmit}
        >
            <textarea
                className="chat-input"
                placeholder="Ask ResearchRAG..."
                value={message}
                onChange={(event) =>
                    setMessage(event.target.value)
                }
                onKeyDown={handleKeyDown}
                disabled={disabled}
                rows={1}
            />

            <button
                type="submit"
                className="send-button"
                disabled={
                    disabled ||
                    message.trim().length === 0
                }
                title="Send message"
            >
                <Send size={19} />
            </button>
        </form>
    );
}

export default ChatInput;