import { useRef, useState } from "react";
import {
    Upload,
    FileText,
} from "lucide-react";

import { uploadDocument } from "../api/upload";

function DocumentUploader({
    onUploaded,
}) {
    const inputRef = useRef(null);

    const [file, setFile] =
        useState(null);

    const [uploading, setUploading] =
        useState(false);

    const [error, setError] =
        useState("");

    const [success, setSuccess] =
        useState("");

    function handleFileChange(event) {
        const selected =
            event.target.files?.[0];

        if (!selected) {
            return;
        }

        setError("");
        setSuccess("");

        if (
            selected.type !==
                "application/pdf" &&
            !selected.name
                .toLowerCase()
                .endsWith(".pdf")
        ) {
            setError(
                "Only PDF files are supported."
            );

            return;
        }

        const maxSize =
            25 * 1024 * 1024;

        if (selected.size > maxSize) {
            setError(
                "File size must be less than 25 MB."
            );

            return;
        }

        setFile(selected);
    }

    async function handleUpload() {
        if (!file || uploading) {
            return;
        }

        try {
            setUploading(true);
            setError("");
            setSuccess("");

            await uploadDocument(file);

            setSuccess(
                `${file.name} uploaded successfully.`
            );

            setFile(null);

            if (inputRef.current) {
                inputRef.current.value =
                    "";
            }

            if (onUploaded) {
                await onUploaded();
            }
        } catch (error) {
            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Upload failed."
            );
        } finally {
            setUploading(false);
        }
    }

    return (
        <div className="upload-card">
            <div className="upload-icon">
                <Upload size={24} />
            </div>

            <div className="upload-content">
                <h3>
                    Upload Research Document
                </h3>

                <p>
                    Upload a PDF to add it to
                    your ResearchRAG knowledge
                    base.
                </p>

                <div className="upload-controls">
                    <input
                        ref={inputRef}
                        type="file"
                        accept=".pdf,application/pdf"
                        onChange={
                            handleFileChange
                        }
                    />

                    {file && (
                        <div className="selected-file">
                            <FileText
                                size={17}
                            />

                            <span>
                                {file.name}
                            </span>
                        </div>
                    )}

                    <button
                        className="upload-button"
                        onClick={
                            handleUpload
                        }
                        disabled={
                            !file ||
                            uploading
                        }
                    >
                        {uploading
                            ? "Uploading..."
                            : "Upload PDF"}
                    </button>
                </div>

                {error && (
                    <div className="upload-error">
                        {error}
                    </div>
                )}

                {success && (
                    <div className="upload-success">
                        {success}
                    </div>
                )}
            </div>
        </div>
    );
}

export default DocumentUploader;