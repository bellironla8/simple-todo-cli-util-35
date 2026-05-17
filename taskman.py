import json
import argparse
from pathlib import Path

DATA_FILE = Path(__file__).parent / "todos.json"

def load_todos():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

def save_todos(todos):
    DATA_FILE.write_text(json.dumps(todos, indent=2))

def cmd_add(args):
    todos = load_todos()
    todos.append({"text": args.text, "done": False})
    save_todos(todos)
    print(f"Added: {args.text}")

def cmd_list(args):
    todos = load_todos()
    if not todos:
        print("No tasks yet!")
        return
    for i, task in enumerate(todos, 1):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}. {task['text']}")

def cmd_done(args):
    todos = load_todos()
    if 1 <= args.number <= len(todos):
        todos[args.number - 1]["done"] = True
        save_todos(todos)
        print(f"Done: {todos[args.number - 1]['text']}")
    else:
        print(f"Invalid task number: {args.number}")

def cmd_delete(args):
    todos = load_todos()
    if 1 <= args.number <= len(todos):
        removed = todos.pop(args.number - 1)
        save_todos(todos)
        print(f"Deleted: {removed['text']}")
    else:
        print(f"Invalid task number: {args.number}")

def main():
    parser = argparse.ArgumentParser(description="Todo CLI Manager")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("text", help="Task description")
    add_p.set_defaults(func=cmd_add)

    list_p = subparsers.add_parser("list", help="List all tasks")
    list_p.set_defaults(func=cmd_list)

    done_p = subparsers.add_parser("done", help="Mark task as done")
    done_p.add_argument("number", type=int, help="Task number")
    done_p.set_defaults(func=cmd_done)

    del_p = subparsers.add_parser("delete", help="Delete a task")
    del_p.add_argument("number", type=int, help="Task number")
    del_p.set_defaults(func=cmd_delete)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
