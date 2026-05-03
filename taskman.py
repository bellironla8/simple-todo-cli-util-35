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
    if not todos:
        print("No tasks yet!")
        return
    for i, task in enumerate(todos, 1):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}. {task['text']}")

def mark_done(idx):
    todos = load_todos()
    if 1 <= idx <= len(todos):
        todos[idx - 1]["done"] = True
        save_todos(todos)
        print(f"Done: {todos[idx - 1]['text']}")
    else:
        print(f"Invalid task number: {idx}")

def delete_task(idx):
    todos = load_todos()
    if 1 <= idx <= len(todos):
        removed = todos.pop(idx - 1)
        save_todos(todos)
        print(f"Deleted: {removed['text']}")
    else:
        print(f"Invalid task number: {idx}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_tasks()
    elif sys.argv[1] == "add":
        add_task(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "list":
        list_tasks()
    elif sys.argv[1] == "done":
        mark_done(int(sys.argv[2]))
    elif sys.argv[1] == "delete":
        delete_task(int(sys.argv[2]))
    else:
        print(f"Unknown command: {sys.argv[1]}")
