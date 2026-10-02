class ReindexService:

    def __init__(
        self,
        indexing_pipeline,
        vector_manager,
        document_repository,
    ):

        self.indexing_pipeline = indexing_pipeline
        self.vector_manager = vector_manager
        self.document_repository = (
            document_repository
        )

    def reindex(
        self,
        document_id: str,
    ):

        document = (
            self.document_repository.get(
                document_id
            )
        )

        if document is None:
            raise ValueError(
                "Document not found."
            )

        self.vector_manager.delete_document(
            document.filename
        )

        result = (
            self.indexing_pipeline.index_pdf(
                document.file_path
            )
        )

        return result