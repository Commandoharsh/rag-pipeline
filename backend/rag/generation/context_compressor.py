import re


class ContextCompressor:

    def compress(
        self,
        query: str,
        content: str
    ) -> str:

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if not content.strip():
            return ""

        query_terms = set(
            re.findall(
                r"\b\w+\b",
                query.lower()
            )
        )

        sentences = re.split(
            r"(?<=[.!?])\s+",
            content
        )

        relevant_sentences = []

        for sentence in sentences:

            sentence_terms = set(
                re.findall(
                    r"\b\w+\b",
                    sentence.lower()
                )
            )

            if query_terms.intersection(sentence_terms):
                relevant_sentences.append(sentence.strip())

        if not relevant_sentences:
            return content.strip()

        return " ".join(relevant_sentences)