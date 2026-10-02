@'
import { useRef, useState } from "react";
import { Upload, FileText, CheckCircle, AlertCircle } from "lucide-react";
import { uploadDocument } from "../api/upload";

function DocumentUploader({ onUploaded }) {

    const fileInputRef = useRef(null);

    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState("");
    const [error, setError] = useState("");

    function handleFileChange(event) {

        const selectedFile =
            event.target.files?.[0];

        if (!selectedFile) {
            return;
        }

        setError("");
        setStatus("");

        if (
            selectedFile.type !==
            "application/pdf"
        ) {
            setFile(null);
            setError(
                "Only PDF files are supported."
            );
            return;
        }

        const maxSize =
            25 * 1024 * 1024;

        if (selectedFile.size > maxSize) {
            setFile(null);
            setError(
                "File size must be less than 25 MB."
            );
            return;
        }

        setFile(selectedFile);
    }

    async function handleUpload() {

        if (!file || uploading) {
            return;
        }

        setUploading(true);
        setError("");
        setStatus("Uploading document...");

        try {

            const result =
                await uploadDocument(file);

            setStatus(
                "Document indexed successfully."
            );

            setFile(null);

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }

            if (onUploaded) {
                onUploaded(result);
            }

        } catch (error) {

            console.error(
                "Document upload failed:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Document upload failed."
            );

            setStatus("");

        } finally {

            setUploading(false);
        }
    }

    return (
        <div className="document-uploader">

            <div
                className="upload-area"
                onClick={() =>
                    fileInputRef.current?.click()
                }
            >

                <Upload size={32} />

                <h3>
                    Upload a research PDF
                </h3>

                <p>
                    Click to select a PDF
                </p>

                <small>
                    Maximum file size: 25 MB
                </small>

                <input
                    ref={fileInputRef}
                    type="file"
                    accept="application/pdf,.pdf"
                    onChange={handleFileChange}
                    hidden
                />

            </div>

            {file && (

                <div className="selected-file">

                    <FileText size={20} />

                    <div className="file-info">

                        <strong>
                            {file.name}
                        </strong>

                        <span>
                            {(
                                file.size /
                                (1024 * 1024)
                            ).toFixed(2)} MB
                        </span>

                    </div>

                    <button
                        onClick={handleUpload}
                        disabled={uploading}
                    >
                        {uploading
                            ? "Processing..."
                            : "Upload"}
                    </button>

                </div>

            )}

            {status && (

                <div className="upload-success">

                    <CheckCircle size={18} />

                    <span>
                        {status}
                    </span>

                </div>

            )}

            {error && (

                <div className="upload-error">

                    <AlertCircle size={18} />

                    <span>
                        {error}
                    </span>

                </div>

            )}

        </div>
    );
}

export default DocumentUploader;
'@ | Set-Content src\components\DocumentUploader.jsx