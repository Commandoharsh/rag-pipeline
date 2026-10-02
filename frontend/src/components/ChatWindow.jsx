import Message from "./Message";
import Citation from "./Citation";

function ChatWindow({
    messages,
    citations,
    loading,
}) {

    return (
        <div className="chat-window">

            <div className="messages">

                {messages.length === 0 && (
                    <div className="empty-chat">

                        <h1>
                            ResearchRAG
                        </h1>

                        <p>
                            Ask questions about your
                            indexed research documents.
                        </p>

                    </div>
                )}

                {messages.map((message) => (
                    <Message
                        key={message.id}
                        message={message}
                    />
                ))}

                {loading && (
                    <div className="message assistant-message">
                        ResearchRAG is thinking...
                    </div>
                )}

            </div>

            {citations.length > 0 && (

                <div className="citations">

                    <h3>
                        Sources
                    </h3>

                    {citations.map(
                        (citation, index) => (
                            <Citation
                                key={index}
                                citation={citation}
                            />
                        )
                    )}

                </div>

            )}

        </div>
    );
}

export default ChatWindow;