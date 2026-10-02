from enum import Enum


class QueryIntent(str, Enum):
    FACTUAL = "factual"
    DEFINITION = "definition"
    COMPARISON = "comparison"
    ANALYTICAL = "analytical"
    EXPLANATION = "explanation"
    UNKNOWN = "unknown"


class QueryIntentClassifier:

    def classify(self, query: str) -> QueryIntent:

        query_lower = query.lower().strip()

        # Comparison must be checked BEFORE definition
        # because comparison questions can contain
        # phrases such as "what is the difference..."
        if any(
            phrase in query_lower
            for phrase in [
                "compare",
                "comparison",
                "difference between",
                "differences between",
                "versus",
                " vs ",
                "vs.",
            ]
        ):
            return QueryIntent.COMPARISON

        if any(
            phrase in query_lower
            for phrase in [
                "what is",
                "what are",
                "define",
                "definition",
            ]
        ):
            return QueryIntent.DEFINITION

        if any(
            phrase in query_lower
            for phrase in [
                "why",
                "how does",
                "how do",
                "impact",
                "effect",
            ]
        ):
            return QueryIntent.ANALYTICAL

        if any(
            phrase in query_lower
            for phrase in [
                "explain",
                "describe",
            ]
        ):
            return QueryIntent.EXPLANATION

        return QueryIntent.FACTUAL