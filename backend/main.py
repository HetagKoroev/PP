from fastapi import FastAPI, HTTPException
from typing import Optional

from pydantic import BaseModel
import uvicorn

app = FastAPI()

projects = [
    {
        "id": 1,
        "name": "Project A",
        "description": "This is project A",
        "author": "John Doe",
        "preview": "https://screenshot0.png",
        "tags": ["python", "web"],
        "screenshots": ["https://screenshot1.png", "https://screenshot2.png"],
        "rating": 4.2
    },
    {
        "id": 2,
        "name": "Project B",
        "description": "This is project B",
        "author": "Jane Smith",
        "preview": "https://screenshot1.png",
        "tags": ["javascript", "web"],
        "screenshots": ["https://screenshot3.png", "https://screenshot4.png"],
        "rating": 4.8
    }
]


class ProjectInput(BaseModel):
    name: str
    description: str
    author: str
    preview: str
    tags: list[str]
    screenshots: list[str]
    rating: int


class ProjectOutput(ProjectInput):
    id: int


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/projects")
def get_projects(sort_by: Optional[str] = None, filter_by: Optional[str] = None):
    global projects
    if sort_by:
        projects.sort(key=lambda p: p[sort_by])
    if filter_by:
        filter_key, filter_value = filter_by.split(":")
        projects = [p for p in projects if filter_value in p[filter_key]]
    return projects


@app.get("/projects/{project_id}")
def get_project_by_id(project_id: int):
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.post("/projects", response_model=ProjectOutput)
def create_project(project: ProjectInput):
    project_with_id = {"id": len(projects) + 1} | project.dict()
    projects.append(project_with_id)
    return project_with_id


@app.put("/projects/{project_id}")
def update_project_by_id(project_id: int, project: dict):
    index = next((i for i, p in enumerate(projects) if p["id"] == project_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Project not found")
    projects[index].update(project)
    return projects[index]


@app.delete("/projects/{project_id}")
def delete_project_by_id(project_id: int):
    index = next((i for i, p in enumerate(projects) if p["id"] == project_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Project not found")
    deleted_project = projects.pop(index)
    return deleted_project


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
