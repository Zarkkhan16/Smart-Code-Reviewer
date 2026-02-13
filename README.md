# Smart Code Reviewer

## What is this?

**Smart Code Reviewer** is an assistant that reviews your code for **readability**, **structure**, and **maintainability** before a human does. You run it on a file or folder (or paste code in the web UI) and get scores plus concrete suggestions—so you can fix issues before opening a PR or asking for review.

- **Readability** – line length, comments, clarity
- **Structure** – long functions, big files, organization
- **Maintainability** – cyclomatic complexity, maintainability index

Supported: **Python** (full analysis); other languages get basic line-based checks.

---

## How it works

1. You give it **source code** (file path, directory, stdin, or paste in the web UI).
2. It **analyzes** the code with static checks: line length, comment ratio, function length, cyclomatic complexity (via radon for Python), and maintainability index.
3. It turns those metrics into **scores (0–10)** and **suggestions** for each category (readability, structure, maintainability).
4. You get a **report** in the terminal (rich panels) or JSON, or in the browser if you use the web UI.

No data is sent to external APIs; analysis runs locally (and in-browser for the deployed web app).

---

## Output

**CLI (default):**

```
╭──────────────────────────────────────────────────────────────────────────────╮
│ 📄 smart_code_reviewer/report.py  (143 lines)                                │
│                                                                              │
│   Readability       ██████░░░░  Fair                                         │
│     → 8 line(s) exceed 100 chars – consider breaking for readability.        │
│   Structure         ██████████  Excellent                                    │
│   Maintainability   ██████████  Excellent                                    │
│     → High cyclomatic complexity in: build_report – simplify branches or     │
│ extract helpers.                                                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

**JSON (`--json`):**

```json
{
  "reports": [{
    "path": "example.py",
    "readability": { "score": 6.0, "suggestions": ["8 line(s) exceed 100 chars..."] },
    "structure": { "score": 10.0, "suggestions": [] },
    "maintainability": { "score": 10.0, "suggestions": ["High cyclomatic complexity in: build_report..."] },
    "error": null,
    "line_count": 143
  }]
}
```

**Web UI** – same scores and suggestions shown in the browser after you paste code and click Review.

---

## Install

```bash
pip install -r requirements.txt
```

## Usage

Review current directory (default):

```bash
python -m smart_code_reviewer
```

Review a file or directory:

```bash
python -m smart_code_reviewer -t path/to/file.py
python -m smart_code_reviewer -t path/to/project/
```

Review from stdin (paste code, then Ctrl+D):

```bash
python -m smart_code_reviewer -t -
```

JSON output:

```bash
python -m smart_code_reviewer -t . --json
```

**Web UI** – paste code and get instant feedback:

```bash
python -m smart_code_reviewer web
# Open http://127.0.0.1:8000
```

## Deploy with Docker

The app runs in a container. Use it locally or deploy to a free host.

### Run locally with Docker

```bash
docker build -t smart-code-reviewer .
docker run -p 8000:8000 smart-code-reviewer
```

Open **http://localhost:8000**

### Deploy to Render (free, with Docker)

1. Push this repo to **GitHub**.
2. Go to **[render.com](https://render.com)** → **New** → **Web Service** → connect **Smart-Code-Reviewer**.
3. Render will detect the **Dockerfile** and use it (no build/start commands needed).
4. Click **Create Web Service**. Your app will be at **`https://smart-code-reviewer.onrender.com`** (or the name you set).

Free tier: service sleeps after ~15 min idle; first request may take ~1 min to wake.

### Deploy to Fly.io (free allowance)

1. Install [flyctl](https://fly.io/docs/hands-on/install-flyctl/) and sign up: `fly auth signup`.
2. From the project root:
   ```bash
   fly launch
   ```
   Use the existing `fly.toml` (answer **no** to copying config if asked). Then:
   ```bash
   fly deploy
   ```
3. Your app will be at **`https://smart-code-reviewer.fly.dev`** (or the app name you chose). Open it with `fly open`.

### Deploy to Vercel (free)

1. Push this repo to **GitHub**.
2. Go to **[vercel.com](https://vercel.com)** → **Add New** → **Project** → import **Smart-Code-Reviewer**.
3. Vercel will detect the FastAPI app (root `index.py` and `vercel.json`). Click **Deploy**.
4. Your app will be at **`https://smart-code-reviewer.vercel.app`** (or the project name you set).

Runs as a serverless function; cold starts may add ~1–2 s on first request.

### Other options (no Docker)

- **Render (Python)** – Use **Build command:** `pip install -r requirements.txt` and **Start command:** `uvicorn smart_code_reviewer.app:app --host 0.0.0.0 --port $PORT` (see `render.yaml`).
- **Railway** – Deploy from GitHub; set the same build/start commands or use the Dockerfile.

## Project layout

- `smart_code_reviewer/` – main package
- `index.py` – Vercel entrypoint (exports FastAPI app)
- `vercel.json` – Vercel config (Python serverless)
- `Dockerfile` – container image (Render, Fly.io, Railway)
- `fly.toml` – Fly.io config
- `render.yaml` – Render config (Python or Docker)
- `runtime.txt` – Python version for Render (non-Docker)

## License

MIT
