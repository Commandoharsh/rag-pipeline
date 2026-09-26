import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        # Normalize whitespace
        text = re.sub(r"[ \t]+", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text