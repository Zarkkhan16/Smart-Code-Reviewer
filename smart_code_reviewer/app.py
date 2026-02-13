"""Web UI for Smart Code Reviewer."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from .review import review_file

app = FastAPI(title="Smart Code Reviewer", version="0.1.0")


def _load_template() -> str:
    """Load index.html so it works when the package is bundled (e.g. Vercel serverless)."""
    try:
        from importlib.resources import files
        return (files("smart_code_reviewer") / "templates" / "index.html").read_text(encoding="utf-8")
    except Exception:
        pass
    template_path = Path(__file__).parent / "templates" / "index.html"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return "<!DOCTYPE html><html><body><h1>Smart Code Reviewer</h1><p>Template not found.</p></body></html>"


class ReviewRequest(BaseModel):
    source: str
    filename: str = "snippet.py"


@app.exception_handler(Exception)
async def unhandled(_request: Request, exc: Exception) -> JSONResponse:
    """Avoid 500 crash loop; return structured error for debugging."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal error", "type": type(exc).__name__},
    )


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return _load_template()


@app.post("/review")
def review(request: ReviewRequest) -> dict:
    """Review pasted code and return report as JSON."""
    report = review_file(request.filename, source=request.source)
    return {"report": report.to_dict()}


def run_web(host: str = "127.0.0.1", port: int = 8000) -> None:
    import uvicorn
    uvicorn.run("smart_code_reviewer.app:app", host=host, port=port, reload=False)
