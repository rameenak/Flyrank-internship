
from fastapi import FastAPI, HTTPException, Body

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple in-memory CRUD API for managing tasks."
)

# In-memory task list
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Test the API", "done": True}
]


# Stage 1: Root endpoint
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# Stage 1: Health endpoint
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Stage 2: Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# Stage 2: Get a task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Stage 3: Create a new task
@app.post("/tasks", status_code=201)
def create_task(task_data: dict = Body(...)):
    title = task_data.get("title")

    # Validate the title
    if not isinstance(title, str) or not title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    # Assign the next available ID
    new_id = max(
        (task["id"] for task in tasks),
        default=0
    ) + 1

    # Create the task
    new_task = {
        "id": new_id,
        "title": title.strip(),
        "done": False
    }

    tasks.append(new_task)

    return new_task
