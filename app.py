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
    conn.execute(
        "INSERT INTO tasks (title, done, created) VALUES (?, 0, ?)",
        (title, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()
    print(f'✅ Aufgabe hinzugefügt: "{title}"')


def list_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT id, title, done, created FROM tasks ORDER BY id").fetchall()
    conn.close()

    if not rows:
        print("📭 Keine Aufgaben vorhanden.")
        return

    print("\n📋 Aufgabenliste:")
    print("-" * 50)
    for row in rows:
        id_, title, done, created = row
        status = "✅" if done else "⬜"
        print(f"  [{id_}] {status}  {title}  ({created})")
    print("-" * 50)
    print()


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        print(f"❌ Aufgabe #{task_id} nicht gefunden.")
    else:
        print(f"🎉 Aufgabe #{task_id} als erledigt markiert!")


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        print(f"❌ Aufgabe #{task_id} nicht gefunden.")
    else:
        print(f"🗑️  Aufgabe #{task_id} gelöscht.")


def show_help():
    print("""
🛠️  Task Tracker – Verwendung:

  python3 app.py add "Aufgabe"   → Neue Aufgabe hinzufügen
  python3 app.py list            → Alle Aufgaben anzeigen
  python3 app.py done <id>       → Aufgabe als erledigt markieren
  python3 app.py delete <id>     → Aufgabe löschen
  python3 app.py help            → Hilfe anzeigen
""")


def main():
    args = sys.argv[1:]

    if not args or args[0] == "help":
        show_help()

    elif args[0] == "add":
        if len(args) < 2:
            print('❌ Verwendung: python3 app.py add "Deine Aufgabe"')
        else:
            add_task(" ".join(args[1:]))

    elif args[0] == "list":
        list_tasks()

    elif args[0] == "done":
        if len(args) < 2 or not args[1].isdigit():
            print("❌ Verwendung: python3 app.py done <id>")
        else:
            complete_task(int(args[1]))

    elif args[0] == "delete":
        if len(args) < 2 or not args[1].isdigit():
            print("❌ Verwendung: python3 app.py delete <id>")
        else:
            delete_task(int(args[1]))

    else:
        print(f'❌ Unbekannter Befehl: "{args[0]}"')
        show_help()


if __name__ == "__main__":
    main()
