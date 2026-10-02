class CorpusStatistics:

    def __init__(
        self,
        document_repository,
        vector_store,
    ):

        self.document_repository = (
            document_repository
        )

        self.vector_store = vector_store

    def get(self):

        documents = (
            self.document_repository.list()
        )

        indexed_documents = [
            document
            for document in documents
            if document.status == "indexed"
        ]

        chunks = (
            self.vector_store.get_all_chunks()
        )

        total_size = sum(
            document.file_size
            for document in documents
        )

        return {
            "documents": len(documents),
            "indexed_documents": len(
                indexed_documents
            ),
            "failed_documents": len(
                [
                    document
                    for document in documents
                    if document.status == "failed"
                ]
            ),
            "chunks": len(chunks),
            "total_bytes": total_size,
        }