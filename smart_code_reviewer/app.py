"""Web UI for Smart Code Reviewer."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .review import review_file

app = FastAPI(title="Smart Code Reviewer", version="0.1.0")

TEMPLATES_DIR = Path(__file__).parent / "templates"


class ReviewRequest(BaseModel):
    source: str
    filename: str = "snippet.py"


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    html = (TEMPLATES_DIR / "index.html").read_text(encoding="utf-8")
    return html


@app.post("/review")
def review(request: ReviewRequest) -> dict:
    """Review pasted code and return report as JSON."""
    report = review_file(request.filename, source=request.source)
    return {"report": report.to_dict()}


def run_web(host: str = "127.0.0.1", port: int = 8000) -> None:
    import uvicorn
    uvicorn.run("smart_code_reviewer.app:app", host=host, port=port, reload=False)
