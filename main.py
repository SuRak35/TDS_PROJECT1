import os
import subprocess
import requests
import locale
from datetime import datetime
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
            file_path = "data/format.md"
            if not os.path.exists(file_path):
                return {"status": "error", "message": "File not found"}
            
            subprocess.run(["prettier", "--write", file_path], check=True)
            return {"status": "success", "message": "Task A2 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "count" in task.lower() and ("wednesday" in task.lower() or "thursday" in task.lower() or "sunday" in task.lower()):
        try:
            file_path = "data/dates.txt"
            output_file = "data/dates-wednesdays.txt"
            day_map = {
                "wednesday": 2,
                "thursday": 3,
                "sunday": 6
            }

            locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
            day_name = next((day for day in day_map if day in task.lower()), None)
            if not day_name:
                return {"status": "error", "message": "Day not recognized in task"}

            target_day = day_map[day_name]
            if not os.path.exists(file_path):
                return {"status": "error", "message": "File not found"}

            with open(file_path, "r", encoding="utf-8") as file:
                dates = file.readlines()
            
            count = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == target_day)

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(str(count))

            return {"status": "success", "message": f"Task A3 completed: {count} {day_name}s counted"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "count" in task.lower() and "occurrences" in task.lower():
        try:
            input_file = "data/words.txt"
            output_file = "data/word-count.txt"

            if not os.path.exists(input_file):
                return {"status": "error", "message": "File not found"}

            with open(input_file, "r", encoding="utf-8") as file:
                words = file.read().split()

            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1

            with open(output_file, "w", encoding="utf-8") as file:
                for word, count in word_counts.items():
                    file.write(f"{word} {count}\n")

            return {"status": "success", "message": "Task A5 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Task not recognized"}

@app.get("/read")
def read_file(path: str = Query(..., description="File path to read")):
    print(f"Attempting to read file at path: {path}")  

    if not os.path.exists(path):
        return {"status": "error", "message": "File not found"}
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    return {"status": "success", "content": content}
