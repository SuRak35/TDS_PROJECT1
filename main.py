from fastapi import FastAPI, HTTPException
import os

app = FastAPI()

@app.post("/run")
async def run_task(task: str):
    """
    Executes a plain-English task.
    """
    if not task:
        raise HTTPException(status_code=400, detail="Task description is required")

    try:
        # Placeholder for task execution logic
        return {"status": "success", "message": f"Task '{task}' executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/read")
async def read_file(path: str):
    """
    Returns the content of the specified file.
    """
    if not path.startswith("/data/"):
        raise HTTPException(status_code=403, detail="Access denied: Only files in /data/ can be read")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(path, "r") as file:
            content = file.read()
        return {"status": "success", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
