"""
Storage utilities for task persistence.
"""
import json
from pathlib import Path
from datetime import datetime

DEFAULT_FILE = Path(__file__).parent / "todos.json"

class TaskStorage:
    def __init__(self, filepath=None):
        self.filepath = Path(filepath) if filepath else DEFAULT_FILE

    def load(self):
        if self.filepath.exists():
            try:
                return json.loads(self.filepath.read_text())
            except json.JSONDecodeError:
                return []
        return []

    def save(self, todos):
        self.filepath.write_text(json.dumps(todos, indent=2))

    def add(self, text, priority="normal"):
        todos = self.load()
        task = {
            "text": text,
            "done": False,
            "priority": priority,
            "created": datetime.now().isoformat(),
        }
        todos.append(task)
        self.save(todos)
        return task

    def get_all(self):
        return self.load()

    def mark_done(self, idx):
        todos = self.load()
        if 1 <= idx <= len(todos):
            todos[idx - 1]["done"] = True
            todos[idx - 1]["completed"] = datetime.now().isoformat()
            self.save(todos)
            return todos[idx - 1]
        return None

    def delete(self, idx):
        todos = self.load()
        if 1 <= idx <= len(todos):
            removed = todos.pop(idx - 1)
            self.save(todos)
            return removed
        return None

    def clear_done(self):
        todos = self.load()
        remaining = [t for t in todos if not t["done"]]
        removed_count = len(todos) - len(remaining)
        self.save(remaining)
        return removed_count
