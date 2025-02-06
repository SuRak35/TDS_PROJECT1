import os
import subprocess
import json
import glob
from datetime import datetime
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
            user_email = "24ds1000046@ds.study.iitm.ac.in"
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

    elif "count" in task.lower() and "wednesdays" in task.lower():
        try:
            input_file = "/data/dates.txt"
            output_file = "/data/dates-wednesdays.txt"

            if not os.path.exists(input_file):
                return {"status": "error", "message": "Input file not found"}

            with open(input_file, "r", encoding="utf-8") as file:
                dates = file.readlines()

            wednesday_count = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(str(wednesday_count))

            return {"status": "success", "message": "Task A3 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "sort" in task.lower() and "contacts" in task.lower():
        try:
            input_file = "/data/contacts.json"
            output_file = "/data/contacts-sorted.json"

            if not os.path.exists(input_file):
                return {"status": "error", "message": "Input file not found"}

            with open(input_file, "r", encoding="utf-8") as file:
                contacts = json.load(file)

            contacts.sort(key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))

            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(contacts, file, indent=4)

            return {"status": "success", "message": "Task A4 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "write" in task.lower() and "recent log" in task.lower():
        try:
            log_dir = "/data/logs/"
            output_file = "/data/logs-recent.txt"

            if not os.path.exists(log_dir):
                return {"status": "error", "message": "Log directory not found"}

            log_files = sorted(
                glob.glob(os.path.join(log_dir, "*.log")),
                key=os.path.getmtime,
                reverse=True
            )[:10]

            recent_lines = []
            for log_file in log_files:
                with open(log_file, "r", encoding="utf-8") as file:
                    first_line = file.readline().strip()
                    if first_line:
                        recent_lines.append(first_line)

            with open(output_file, "w", encoding="utf-8") as file:
                file.write("\n".join(recent_lines))

            return {"status": "success", "message": "Task A5 completed successfully"}
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
