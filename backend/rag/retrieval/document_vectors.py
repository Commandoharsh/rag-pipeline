class DocumentVectorManager:

    def __init__(self, vector_store):

        self.vector_store = vector_store

    def delete_document(
        self,
        source: str,
    ):

        self.vector_store.delete_by_metadata(
            key="source",
            value=source,
        )