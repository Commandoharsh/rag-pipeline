from pathlib import Path
from pypdf import PdfReader

from .document import Document


class PDFLoader:

    def load(self, file_path: str) -> list[Document]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        reader = PdfReader(file_path)

        documents = []

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if not text:
                continue

            document = Document(
                content=text.strip(),
                metadata={
                    "source": path.name,
                    "page": str(page_number),
                    "file_type": "pdf"
                }
            )

            documents.append(document)

        return documents