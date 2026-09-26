from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.model_name = model_name

        self.model = SentenceTransformer(
            model_name
        )

    def encode(
        self,
        texts: list[str]
    ):

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

    def encode_single(
        self,
        text: str
    ):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )