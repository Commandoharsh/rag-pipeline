function Message({ message }) {

    const isUser =
        message.role === "user";

    return (
        <div
            className={
                isUser
                    ? "message user-message"
                    : "message assistant-message"
            }
        >

            <div className="message-role">
                {isUser ? "You" : "ResearchRAG"}
            </div>

            <div className="message-content">
                {message.content}
            </div>

        </div>
    );
}

export default Message;