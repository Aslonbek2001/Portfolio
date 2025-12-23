from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import re

app = FastAPI(title="Portfolio Site")

# Static files (CSS, CV)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "projects.json"
SOCIAL_FILE = DATA_DIR / "social.json"
RESUME_FILE = DATA_DIR / "resume.json"


def load_projects():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def load_socials():
    return json.loads(SOCIAL_FILE.read_text(encoding="utf-8"))

def load_resume():
    return json.loads(RESUME_FILE.read_text(encoding="utf-8"))


def slugify(text):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "project"


def with_slugs(projects):
    return [{**project, "slug": slugify(project["name"])} for project in projects]


PROJECTS = load_projects()
SOCIALS = load_socials()
RESUME = load_resume()


# ======================
# HOME PAGE
# ======================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    projects = with_slugs(PROJECTS)[:3]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "projects": projects,
            "socials": SOCIALS
        }
    )


# ======================
# PROJECTS PAGE
# ======================
@app.get("/projects", response_class=HTMLResponse)
def projects_page(request: Request):
    projects = with_slugs(PROJECTS)

    return templates.TemplateResponse(
        "projects.html",
        {
            "request": request,
            "projects": projects
        }
    )


# ======================
# RESUME PAGE
# ======================
@app.get("/resume", response_class=HTMLResponse)
def resume_page(request: Request):
    return templates.TemplateResponse(
        "resume.html",
        {
            "request": request,
            "resume": RESUME
        }
    )


# ======================
# PROJECT DETAIL
# ======================
@app.get("/projects/{slug}", response_class=HTMLResponse)
def project_detail(request: Request, slug: str):
    projects = with_slugs(PROJECTS)
    project = next((item for item in projects if item["slug"] == slug), None)
    if not project:
        return templates.TemplateResponse(
            "project_detail.html",
            {"request": request, "project": None},
            status_code=404
        )

    return templates.TemplateResponse(
        "project_detail.html",
        {"request": request, "project": project}
    )


# ======================
# CV DOWNLOAD
# ======================
@app.get("/download-cv")
def download_cv():
    return FileResponse(
        path="static/cv.pdf",
        filename="My_CV.pdf",
        media_type="application/pdf"
    )
