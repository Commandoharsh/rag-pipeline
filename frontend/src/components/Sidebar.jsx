import {
    Plus,
    MessageSquare,
    Trash2
} from "lucide-react";

function Sidebar({
    conversations,
    activeConversation,
    onSelect,
    onCreate,
    onDelete,
}) {

    return (
        <aside className="sidebar">

            <div className="sidebar-header">

                <h2>ResearchRAG</h2>

                <button
                    onClick={onCreate}
                    title="New conversation"
                >
                    <Plus size={18} />
                </button>

            </div>

            <div className="conversation-list">

                {conversations.map(
                    (conversation) => (

                    <div
                        key={conversation.id}
                        className={
                            "conversation-item " +
                            (
                                activeConversation ===
                                conversation.id
                                    ? "active"
                                    : ""
                            )
                        }
                    >

                        <button
                            className="conversation-select"
                            onClick={() =>
                                onSelect(
                                    conversation.id
                                )
                            }
                        >
                            <MessageSquare size={16} />

                            <span>
                                {conversation.title}
                            </span>
                        </button>

                        <button
                            onClick={() =>
                                onDelete(
                                    conversation.id
                                )
                            }
                        >
                            <Trash2 size={15} />
                        </button>

                    </div>

                ))}

            </div>

        </aside>
    );
}

export default Sidebar;