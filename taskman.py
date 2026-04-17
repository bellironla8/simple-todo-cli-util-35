import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent / "todos.json"

def load_todos():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

def save_todos(todos):
    DATA_FILE.write_text(json.dumps(todos, indent=2))

def add_task(text):
    todos = load_todos()
    todos.append({"text": text, "done": False})
    save_todos(todos)
    print(f"Added: {text}")

def list_tasks():
    todos = load_todos()
    for i, task in enumerate(todos, 1):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}. {task['text']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_tasks()
    elif sys.argv[1] == "add":
        add_task(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "list":
        list_tasks()
