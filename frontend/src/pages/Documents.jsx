@'
import { useEffect, useState } from "react";
import {
    FileText,
    RefreshCw,
    Database,
} from "lucide-react";

import DocumentUploader from "../components/DocumentUploader";
import { getDocuments } from "../api/documents";

function Documents() {

    const [
        documents,
        setDocuments
    ] = useState([]);

    const [
        loading,
        setLoading
    ] = useState(true);

    const [
        error,
        setError
    ] = useState("");

    async function loadDocuments() {

        setLoading(true);
        setError("");

        try {

            const data =
                await getDocuments();

            /*
             * The backend may return either:
             *
             * [
             *   {...},
             *   {...}
             * ]
             *
             * or:
             *
             * {
             *   "documents": [...]
             * }
             */

            if (Array.isArray(data)) {

                setDocuments(data);

            } else {

                setDocuments(
                    data.documents || []
                );
            }

        } catch (error) {

            console.error(
                "Failed to load documents:",
                error
            );

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

    function handleUploaded() {
        loadDocuments();
    }

    function getStatusClass(status) {

        switch (
            status?.toLowerCase()
        ) {

            case "indexed":
                return "status-indexed";

            case "indexing":
                return "status-indexing";

            case "failed":
                return "status-failed";

            default:
                return "status-default";
        }
    }

    function formatFileSize(bytes) {

        if (!bytes) {
            return "0 MB";
        }

        if (
            bytes <
            1024 * 1024
        ) {
            return (
                `${(
                    bytes / 1024
                ).toFixed(1)} KB`
            );
        }

        return (
            `${(
                bytes /
                (1024 * 1024)
            ).toFixed(2)} MB`
        );
    }

    function formatDate(date) {

        if (!date) {
            return "—";
        }

        try {

            return new Date(
                date
            ).toLocaleString();

        } catch {

            return date;
        }
    }

    return (
        <div className="documents-page">

            <div className="documents-header">

                <div>

                    <h1>
                        Research Documents
                    </h1>

                    <p>
                        Manage the documents
                        available to ResearchRAG.
                    </p>

                </div>

                <button
                    className="refresh-button"
                    onClick={loadDocuments}
                    disabled={loading}
                >
                    <RefreshCw
                        size={17}
                    />

                    Refresh
                </button>

            </div>

            <DocumentUploader
                onUploaded={
                    handleUploaded
                }
            />

            <div className="documents-section">

                <div className="section-title">

                    <div>
                        <Database
                            size={20}
                        />

                        <h2>
                            Indexed Documents
                        </h2>
                    </div>

                    <span>
                        {documents.length}
                    </span>

                </div>

                {loading && (

                    <div className="documents-loading">
                        Loading documents...
                    </div>

                )}

                {error && (

                    <div className="documents-error">
                        {error}
                    </div>

                )}

                {!loading &&
                    !error &&
                    documents.length === 0 && (

                    <div className="documents-empty">

                        <FileText
                            size={40}
                        />

                        <h3>
                            No documents yet
                        </h3>

                        <p>
                            Upload a PDF to build
                            your research knowledge
                            base.
                        </p>

                    </div>

                )}

                {!loading &&
                    documents.length > 0 && (

                    <div className="document-table">

                        <div className="document-row document-header-row">

                            <span>
                                Document
                            </span>

                            <span>
                                Type
                            </span>

                            <span>
                                Size
                            </span>

                            <span>
                                Chunks
                            </span>

                            <span>
                                Status
                            </span>

                            <span>
                                Updated
                            </span>

                        </div>

                        {documents.map(
                            (document) => (

                            <div
                                className="document-row"
                                key={document.id}
                            >

                                <div className="document-name">

                                    <FileText
                                        size={19}
                                    />

                                    <div>

                                        <strong>
                                            {
                                                document.filename
                                            }
                                        </strong>

                                        <small>
                                            {
                                                document.id
                                            }
                                        </small>

                                    </div>

                                </div>

                                <span>
                                    {
                                        document.file_type ||
                                        "pdf"
                                    }
                                </span>

                                <span>
                                    {formatFileSize(
                                        document.file_size
                                    )}
                                </span>

                                <span>
                                    {
                                        document.chunk_count ??
                                        0
                                    }
                                </span>

                                <span>

                                    <span
                                        className={
                                            `document-status ${
                                                getStatusClass(
                                                    document.status
                                                )
                                            }`
                                        }
                                    >
                                        {
                                            document.status ||
                                            "unknown"
                                        }
                                    </span>

                                </span>

                                <span>
                                    {formatDate(
                                        document.updated_at
                                    )}
                                </span>

                            </div>

                        ))}

                    </div>

                )}

            </div>

        </div>
    );
}

export default Documents;
'@ | Set-Content src\pages\Documents.jsx