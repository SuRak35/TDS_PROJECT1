import os
import subprocess
import requests
import pandas as pd
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

    elif "sort" in task.lower() and "csv" in task.lower():
        try:
            file_path = "/data/sort.csv"
            if not os.path.exists(file_path):
                return {"status": "error", "message": "File not found"}
            
            df = pd.read_csv(file_path)
            if 'a' not in df.columns:
                return {"status": "error", "message": "Column 'a' not found in file"}
            
            df.sort_values(by="a", ascending=True, inplace=True)
            df.to_csv(file_path, index=False)
            
            return {"status": "success", "message": "Task A3 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Task not recognized"}

@app.get("/read")
def read_file(path: str = Query(..., description="File path to read")):
    print(f"Attempting to read file at path: {path}")  # Log the requested path

    if not os.path.exists(path):
        return {"status": "error", "message": "File not found"}
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    return {"status": "success", "content": content"}
