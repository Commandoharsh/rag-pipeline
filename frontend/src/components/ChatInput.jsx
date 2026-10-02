import { useState } from "react";
import { Send } from "lucide-react";

function ChatInput({
    onSend,
    disabled,
}) {

    const [question, setQuestion] =
        useState("");

    async function handleSubmit(event) {

        event.preventDefault();

        const value = question.trim();

        if (!value || disabled) {
            return;
        }

        setQuestion("");

        await onSend(value);
    }

    return (
        <form
            className="chat-input"
            onSubmit={handleSubmit}
        >

            <input
                value={question}
                onChange={(event) =>
                    setQuestion(
                        event.target.value
                    )
                }
                placeholder="Ask ResearchRAG..."
                disabled={disabled}
            />

            <button
                type="submit"
                disabled={disabled}
            >
                <Send size={18} />
            </button>

        </form>
    );
}

export default ChatInput;