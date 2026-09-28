import re


class QueryPreprocessor:

    def preprocess(self, query: str) -> str:

        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        # Normalize whitespace
        query = re.sub(r"\s+", " ", query)

        # Normalize repeated punctuation
        query = re.sub(r"[?]{2,}", "?", query)
        query = re.sub(r"[!]{2,}", "!", query)

        return query