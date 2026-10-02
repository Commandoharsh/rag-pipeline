import { useEffect, useState } from "react";
import {
    FileText,
    RefreshCw,
    Upload,
    CheckCircle,
    Clock,
    XCircle,
} from "lucide-react";

import DocumentUploader from "../components/DocumentUploader";
import { getDocuments } from "../api/documents";

function formatBytes(bytes) {
    if (!bytes) {
        return "0 B";
    }

    const units = [
        "B",
        "KB",
        "MB",
        "GB",
    ];

    const index = Math.floor(
        Math.log(bytes) / Math.log(1024)
    );

    return `${(
        bytes /
        Math.pow(1024, index)
    ).toFixed(1)} ${units[index]}`;
}

function formatDate(date) {
    if (!date) {
        return "-";
    }

    return new Date(date).toLocaleString();
}

function StatusBadge({ status }) {
    if (status === "indexed") {
        return (
            <span className="document-status indexed">
                <CheckCircle size={14} />
                Indexed
            </span>
        );
    }

    if (status === "indexing") {
        return (
            <span className="document-status indexing">
                <Clock size={14} />
                Indexing
            </span>
        );
    }

    if (status === "failed") {
        return (
            <span className="document-status failed">
                <XCircle size={14} />
                Failed
            </span>
        );
    }

    return (
        <span className="document-status">
            {status || "Unknown"}
        </span>
    );
}

function Documents() {
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadDocuments() {
        try {
            setLoading(true);
            setError("");

            const data = await getDocuments();

            setDocuments(
                data.documents || data || []
            );
        } catch (error) {
            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Failed to load documents."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadDocuments();
    }, []);

    return (
        <div className="documents-page">
            <div className="documents-header">
                <div>
                    <h1>Documents</h1>

                    <p>
                        Manage your indexed research
                        documents.
                    </p>
                </div>

                <button
                    className="refresh-button"
                    onClick={loadDocuments}
                    disabled={loading}
                >
                    <RefreshCw
                        size={17}
                        className={
                            loading
                                ? "spin"
                                : ""
                        }
                    />

                    Refresh
                </button>
            </div>

            <DocumentUploader
                onUploaded={loadDocuments}
            />

            {error && (
                <div className="document-error">
                    {error}
                </div>
            )}

            <div className="documents-card">
                {loading ? (
                    <div className="documents-empty">
                        Loading documents...
                    </div>
                ) : documents.length === 0 ? (
                    <div className="documents-empty">
                        <FileText size={40} />

                        <h3>
                            No documents yet
                        </h3>

                        <p>
                            Upload a PDF to start
                            building your research
                            knowledge base.
                        </p>
                    </div>
                ) : (
                    <div className="documents-table-wrapper">
                        <table className="documents-table">
                            <thead>
                                <tr>
                                    <th>
                                        Document
                                    </th>
                                    <th>
                                        Type
                                    </th>
                                    <th>
                                        Size
                                    </th>
                                    <th>
                                        Chunks
                                    </th>
                                    <th>
                                        Status
                                    </th>
                                    <th>
                                        Updated
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                {documents.map(
                                    (document) => (
                                        <tr
                                            key={
                                                document.id
                                            }
                                        >
                                            <td>
                                                <div className="document-name">
                                                    <FileText
                                                        size={
                                                            18
                                                        }
                                                    />

                                                    <span>
                                                        {
                                                            document.filename
                                                        }
                                                    </span>
                                                </div>
                                            </td>

                                            <td>
                                                {document.file_type ||
                                                    "PDF"}
                                            </td>

                                            <td>
                                                {formatBytes(
                                                    document.file_size
                                                )}
                                            </td>

                                            <td>
                                                {
                                                    document.chunk_count
                                                }
                                            </td>

                                            <td>
                                                <StatusBadge
                                                    status={
                                                        document.status
                                                    }
                                                />
                                            </td>

                                            <td>
                                                {formatDate(
                                                    document.updated_at
                                                )}
                                            </td>
                                        </tr>
                                    )
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Documents;