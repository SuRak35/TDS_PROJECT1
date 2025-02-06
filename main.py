import os
import subprocess
import requests
import sqlite3
import json
from fastapi import FastAPI, Query
from email.message import Message
import email
from PIL import Image
import pytesseract

app = FastAPI()

# A1 to A6 are implemented earlier.

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

    elif "count" in task.lower() and "wednesday" in task.lower():
        try:
            file_path = "/data/dates.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            wednesdays = sum(1 for line in lines if line.strip() and 'Wednesday' in line)

            with open("/data/dates-wednesdays.txt", "w", encoding="utf-8") as output_file:
                output_file.write(str(wednesdays))
            
            return {"status": "success", "message": "Task A3 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "sort contacts" in task.lower():
        try:
            with open("/data/contacts.json", "r", encoding="utf-8") as file:
                contacts = json.load(file)

            sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))

            with open("/data/contacts-sorted.json", "w", encoding="utf-8") as output_file:
                json.dump(sorted_contacts, output_file, indent=4)

            return {"status": "success", "message": "Task A4 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "recent logs" in task.lower():
        try:
            log_files = [f for f in os.listdir("/data/logs/") if f.endswith(".log")]
            log_files.sort(key=lambda x: os.path.getmtime(os.path.join("/data/logs/", x)), reverse=True)

            recent_logs = []
            for log_file in log_files[:10]:
                with open(os.path.join("/data/logs/", log_file), "r", encoding="utf-8") as file:
                    recent_logs.append(file.readline().strip())

            with open("/data/logs-recent.txt", "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(recent_logs))

            return {"status": "success", "message": "Task A5 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "extract titles" in task.lower():
        try:
            md_files = [f for f in os.listdir("/data/docs/") if f.endswith(".md")]
            index = {}
            for md_file in md_files:
                with open(os.path.join("/data/docs/", md_file), "r", encoding="utf-8") as file:
                    for line in file:
                        if line.startswith("# "):
                            title = line.strip().replace("# ", "")
                            index[md_file] = title
                            break

            with open("/data/docs/index.json", "w", encoding="utf-8") as output_file:
                json.dump(index, output_file, indent=4)

            return {"status": "success", "message": "Task A6 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "extract email" in task.lower():
        try:
            with open("/data/email.txt", "r", encoding="utf-8") as file:
                msg = email.message_from_string(file.read())

            sender_email = msg["From"].split("<")[1].split(">")[0]

            with open("/data/email-sender.txt", "w", encoding="utf-8") as output_file:
                output_file.write(sender_email)

            return {"status": "success", "message": "Task A7 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "extract credit card" in task.lower():
        try:
            img = Image.open("/data/credit-card.png")
            text = pytesseract.image_to_string(img)
            card_number = "".join(filter(str.isdigit, text))

            with open("/data/credit-card.txt", "w", encoding="utf-8") as output_file:
                output_file.write(card_number)

            return {"status": "success", "message": "Task A8 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "similar comments" in task.lower():
        try:
            with open("/data/comments.txt", "r", encoding="utf-8") as file:
                comments = file.readlines()

            # Here we can use embeddings to find the most similar comments (This is a simplified example)
            max_similarity = 0
            most_similar_pair = []

            for i, comment1 in enumerate(comments):
                for j, comment2 in enumerate(comments[i + 1:], start=i + 1):
                    similarity = compute_similarity(comment1, comment2)  # Placeholder function
                    if similarity > max_similarity:
                        max_similarity = similarity
                        most_similar_pair = [comment1.strip(), comment2.strip()]

            with open("/data/comments-similar.txt", "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(most_similar_pair))

            return {"status": "success", "message": "Task A9 completed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif "gold ticket sales" in task.lower():
        try:
            conn = sqlite3.connect("/data/ticket-sales.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
            total_sales = cursor.fetchone()[0]

            with open("/data/ticket-sales-gold.txt", "w", encoding="utf-8") as output_file:
                output_file.write(str(total_sales))

            return {"status": "success", "message": "Task A10 completed successfully"}
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
