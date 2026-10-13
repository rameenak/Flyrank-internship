
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
    return {"status": "ok"}


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


# Stage 3: Create a task
@app.post("/tasks", status_code=201)
def create_task(task_data: dict = Body(...)):
    title = task_data.get("title")

    if not isinstance(title, str) or not title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    new_id = max(
        (task["id"] for task in tasks),
        default=0
    ) + 1

    new_task = {
        "id": new_id,
        "title": title.strip(),
        "done": False
    }

    tasks.append(new_task)
    return new_task


# Stage 4: Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: dict = Body(...)):
    task = None

    for existing_task in tasks:
        if existing_task["id"] == task_id:
            task = existing_task
            break

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    if not isinstance(task_data, dict) or not task_data:
        raise HTTPException(
            status_code=400,
            detail="Request body cannot be empty"
        )

    if "title" in task_data:
        title = task_data["title"]

        if not isinstance(title, str) or not title.strip():
            raise HTTPException(
                status_code=400,
                detail="Title must be a non-empty string"
            )

        task["title"] = title.strip()

    if "done" in task_data:
        done = task_data["done"]

        if not isinstance(done, bool):
            raise HTTPException(
                status_code=400,
                detail="Done must be true or false"
            )

        task["done"] = done

    invalid_fields = set(task_data.keys()) - {"title", "done"}

    if invalid_fields:
        raise HTTPException(
            status_code=400,
            detail="Only title and done fields are allowed"
        )

    return task


# Stage 4: Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
