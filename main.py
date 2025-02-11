import os
import json
import sqlite3
import requests
import uvicorn
import duckdb
import markdown2
import pandas as pd
import cv2
import numpy as np
import openai
from fastapi import FastAPI, HTTPException
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import Image
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Get AI Proxy Token
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    raise ValueError("Missing AIPROXY_TOKEN. Set it in an environment variable.")

openai.api_key = AIPROXY_TOKEN

# Function to call LLM
def call_llm(prompt, instruction):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{instruction}\n{prompt}"}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Function to read a file securely
def read_file(path):
    base_dir = "/data/"
    abs_path = os.path.abspath(path)

    if not abs_path.startswith(base_dir):  # Prevent directory traversal attacks
        raise HTTPException(status_code=403, detail="Access denied.")

    if os.path.exists(abs_path):
        with open(abs_path, "r", encoding="utf-8") as file:
            return file.read()
    
    return None

# Function to execute tasks using LLM-based parsing
def execute_task(task: str):
    """Uses LLM to interpret the task and execute the correct function."""
    instructions = """
    Identify which predefined function should handle the given task description.
    Return ONLY the function name (e.g., count_wednesdays, sort_contacts, extract_email) without any explanation.
    If unsure, return 'unknown_task'.
    """
    function_name = call_llm(task, instructions)

    task_mapping = {
        "get_markdown": get_markdown,
        "format_markdown": format_markdown,
        "count_wednesdays": count_wednesdays,
        "sort_contacts": sort_contacts,
        "extract_recent_logs": extract_recent_logs,
        "index_markdown_files": index_markdown_files,
        "extract_email": extract_email,
        "extract_credit_card": extract_credit_card,
        "find_similar_comments": find_similar_comments,
        "compute_sales": compute_sales,
        "fetch_api_data": fetch_api_data,
        "clone_git_repo": clone_git_repo,
        "run_sql_query": run_sql_query,
        "scrape_website": scrape_website,
        "compress_image": compress_image,
        "transcribe_audio": transcribe_audio,
        "convert_markdown": convert_markdown,
        "filter_csv": filter_csv,
    }

    if function_name in task_mapping:
        return task_mapping[function_name](task) if "datagen" in function_name else task_mapping[function_name]()
    else:
        raise ValueError(f"Task '{task}' not recognized by the agent.")

# **Phase A Tasks**
def get_markdown(email: str):
    """Installs uv (if required) and runs datagen.py with only the provided email as an argument."""
    if not email:
        raise ValueError("Email is required to run datagen.py")

    os.system("pip install uv")  # Ensure uv is installed
    os.system(f"uv run https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py \"{email}\"")
    
    return f"Datagen script executed for {email}."

def format_markdown():
    os.system("npx prettier@3.4.2 --write /data/format.md")
    return "Markdown formatted."

def count_wednesdays():
    date_formats = ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]
    
    with open("/data/dates.txt", "r") as file:
        dates = file.readlines()

    wednesday_count = 0
    for date in dates:
        for fmt in date_formats:
            try:
                if datetime.strptime(date.strip(), fmt).weekday() == 2:
                    wednesday_count += 1
                break
            except ValueError:
                continue
    
    with open("/data/dates-wednesdays.txt", "w") as file:
        file.write(str(wednesday_count))
    
    return "Wednesdays counted."

def sort_contacts():
    with open("/data/contacts.json", "r") as file:
        contacts = json.load(file)
    contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))
    with open("/data/contacts-sorted.json", "w") as file:
        json.dump(contacts, file, indent=4)
    return "Sorted contacts saved."

def extract_recent_logs():
    log_files = sorted([f for f in os.listdir("/data/logs/") if f.endswith(".log")], key=lambda x: os.path.getmtime(f"/data/logs/{x}"), reverse=True)
    with open("/data/logs-recent.txt", "w") as file:
        for log in log_files[:10]:
            with open(f"/data/logs/{log}", "r") as log_file:
                file.write(log_file.readline() + "\n")
    return "Extracted recent logs."

def index_markdown_files():
    index = {}
    for root, _, files in os.walk("/data/docs"):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            index[file] = line[2:].strip()
                            break
    with open("/data/docs/index.json", "w") as file:
        json.dump(index, file, indent=4)
    return "Markdown indexed."

def extract_email():
    with open("/data/email.txt", "r") as file:
        email_content = file.read()
    email_address = call_llm(email_content, "Extract the sender's email.")
    with open("/data/email-sender.txt", "w") as file:
        file.write(email_address)
    return "Extracted email sender."

def extract_credit_card():
    image = cv2.imread("/data/credit-card.png")
    card_number = call_llm(image, "Extract the credit card number.")
    with open("/data/credit-card.txt", "w") as file:
        file.write(card_number.replace(" ", ""))
    return "Extracted credit card number."

def find_similar_comments():
    with open("/data/comments.txt", "r") as file:
        comments = file.readlines()
    similar_pair = call_llm("\n".join(comments), "Find the most similar pair of comments.")
    with open("/data/comments-similar.txt", "w") as file:
        file.write("\n".join(similar_pair))
    return "Similar comments saved."

def compute_sales():
    conn = sqlite3.connect("/data/ticket-sales.db")
    df = pd.read_sql_query("SELECT SUM(price * units) FROM tickets WHERE type = 'Gold'", conn)
    conn.close()
    with open("/data/ticket-sales-gold.txt", "w") as file:
        file.write(str(df.iloc[0, 0]))
    return "Total sales computed."

# **Phase B Tasks**
def fetch_api_data():
    response = requests.get("https://api.example.com/data")
    with open("/data/api-data.json", "w") as file:
        json.dump(response.json(), file, indent=4)
    return "API data fetched."

def clone_git_repo():
    os.system("git clone https://github.com/example/repo.git /data/repo")
    return "Git repository cloned."

def run_sql_query():
    conn = duckdb.connect("/data/sample.db")
    df = conn.execute("SELECT * FROM table_name LIMIT 10").fetchdf()
    df.to_csv("/data/sql_output.csv", index=False)
    conn.close()
    return "SQL query executed."

def scrape_website():
    response = requests.get("https://example.com")
    soup = BeautifulSoup(response.text, "html.parser")
    with open("/data/web-scraped.txt", "w") as file:
        file.write(soup.title.string)
    return "Website scraped."

def compress_image():
    image = Image.open("/data/sample.jpg")
    image.save("/data/sample_compressed.jpg", "JPEG", quality=50)
    return "Image compressed."

def transcribe_audio():
    transcript = call_llm("/data/sample.mp3", "Transcribe this audio.")
    with open("/data/transcript.txt", "w") as file:
        file.write(transcript)
    return "Audio transcribed."

def convert_markdown():
    with open("/data/sample.md", "r") as file:
        md_content = file.read()
    html_content = markdown2.markdown(md_content)
    with open("/data/sample.html", "w") as file:
        file.write(html_content)
    return "Markdown converted."

def filter_csv():
    column_details = call_llm("Filter CSV file in /data/sample.csv", "Extract column name and value for filtering.")
    
    match = re.search(r"column\s*'(\w+)'\s*with\s*value\s*'(\w+)'", column_details)
    if not match:
        raise ValueError("Could not extract column name and value.")

    column_name, value = match.groups()
    df = pd.read_csv("/data/sample.csv")
    filtered_df = df[df[column_name] == value]
    filtered_df.to_json("/data/filtered.json", orient="records")
    return "CSV filtered."

# API Endpoints
@app.post("/run")
async def run_task(task: str):
    return {"status": "success", "output": execute_task(task)}

@app.get("/read")
async def read(path: str):
    return {"content": read_file(path)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
