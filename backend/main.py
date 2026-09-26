from fastapi import FastAPI

app = FastAPI(
    title="ResearchRAG",
    description="Intelligent Research & Technical Knowledge Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "ResearchRAG",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }