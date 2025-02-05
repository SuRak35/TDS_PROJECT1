import os
import subprocess
import requests
from fastapi import FastAPI, Query

app = FastAPI()

@app.post("/run")
def run_task(task: str):
    if "install uv" in task.lower() and "run" in task.lower():
        try:
            subprocess.run(["pip", "install", "uv"], check=True)
            url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
            response = requests.get(url)
            with open("datagen.py", "w", encoding="utf-8") as file:
                file.write(response.text)
            user_email = "24ds1000046@ds.study.iitm.ac.in"  # Update your email
            subprocess.run(["python", "datagen.py", user_email], check=True)
            return {"status": "success", "message": "Task A1 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "format" in task.lower() and "prettier" in task.lower():
        try:
            file_path = "/data/format.md"
            if not os.path.exists(file_path):
                return {"status": "error", "message": "File not found"}
            
            subprocess.run(["prettier", "--write", file_path], check=True)
            return {"status": "success", "message": "Task A2 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Task not recognized"}

@app.get("/read")
def read_file(path: str = Query(..., description="File path to read")):
    if not os.path.exists(path):
        return {"status": "error", "message": "File not found"}
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    return {"status": "success", "content": content}
