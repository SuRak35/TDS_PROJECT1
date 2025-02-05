import os
import subprocess
import requests
from fastapi import FastAPI, Query

app = FastAPI()

@app.post("/run")
def run_task(task: str):
    if "install uv" in task.lower() and "run" in task.lower():
        try:
            # Install uv if not installed
            subprocess.run(["pip", "install", "uv"], check=True)

            # Download datagen.py
            url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
            response = requests.get(url)
            with open("datagen.py", "w", encoding="utf-8") as file:
                file.write(response.text)

            # Run datagen.py with user email
            user_email = "24ds1000046@ds.study.iitm.ac.in"  # Replace with your actual email
            subprocess.run(["python", "datagen.py", user_email], check=True)

            return {"status": "success", "message": "Task A1 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Task not recognized"}
