import sqlite3
import sys
from datetime import datetime

DB_FILE = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT    NOT NULL,
            done    INTEGER NOT NULL DEFAULT 0,
            created TEXT    NOT NULL
        )
    """)
    conn.commit()
    return conn


def add_task(title):
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn.execute(
        "INSERT INTO tasks (title, done, created) VALUES (?, 0, ?)",
        (title, now)
    )
    conn.commit()
    conn.close()
    print(f'Added task: "{title}"')


def list_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT id, title, done, created FROM tasks ORDER BY id").fetchall()
    conn.close()

    if not rows:
        print("No tasks yet.")
        return

    print("\nTask list:")
    print("-" * 50)
    for row in rows:
        id_, title, done, created = row
        status = "[x]" if done else "[ ]"
        print(f"  [{id_}] {status}  {title}  ({created})")
    print("-" * 50)
    print()


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        print(f"Task #{task_id} was not found.")
    else:
        print(f"Marked task #{task_id} as done.")


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        print(f"Task #{task_id} was not found.")
    else:
        print(f"Deleted task #{task_id}.")


def show_help():
    print("""
Task Tracker - usage:

  python3 app.py add "Task title"  Add a new task
  python3 app.py list              Show all tasks
  python3 app.py done <id>         Mark a task as done
  python3 app.py delete <id>       Delete a task
  python3 app.py help              Show this help message
""")


def main():
    args = sys.argv[1:]

    if not args or args[0] == "help":
        show_help()

    elif args[0] == "add":
        if len(args) < 2:
            print('Usage: python3 app.py add "Task title"')
        else:
            # Join all remaining words so the task title can contain spaces.
            add_task(" ".join(args[1:]))

    elif args[0] == "list":
        list_tasks()

    elif args[0] == "done":
        if len(args) < 2 or not args[1].isdigit():
            print("Usage: python3 app.py done <id>")
        else:
            complete_task(int(args[1]))

    elif args[0] == "delete":
        if len(args) < 2 or not args[1].isdigit():
            print("Usage: python3 app.py delete <id>")
        else:
            delete_task(int(args[1]))

    else:
        print(f'Unknown command: "{args[0]}"')
        show_help()


if __name__ == "__main__":
    main()
