import { User, Bot } from "lucide-react";

function Message({
    role,
    content,
    citations = [],
}) {
    const isUser = role === "user";

    return (
        <div
            className={`message-row ${
                isUser
                    ? "message-user"
                    : "message-assistant"
            }`}
        >
            <div className="message-icon">
                {isUser ? (
                    <User size={17} />
                ) : (
                    <Bot size={18} />
                )}
            </div>

            <div className="message-body">
                <div className="message-role">
                    {isUser
                        ? "You"
                        : "ResearchRAG"}
                </div>

                <div className="message-content">
                    {content}
                </div>

                {!isUser &&
                    citations.length > 0 && (
                        <div className="citation-list">
                            <div className="citation-heading">
                                Sources
                            </div>

                            {citations.map(
                                (citation, index) => (
                                    <div
                                        className="citation-item"
                                        key={
                                            citation.id ||
                                            index
                                        }
                                    >
                                        <span>
                                            📄
                                        </span>

                                        <span>
                                            {citation.filename ||
                                                citation.source ||
                                                "Source"}

                                            {citation.page
                                                ? ` — Page ${citation.page}`
                                                : ""}
                                        </span>
                                    </div>
                                )
                            )}
                        </div>
                    )}
            </div>
        </div>
    );
}

export default Message;