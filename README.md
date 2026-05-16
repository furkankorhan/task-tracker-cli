# Task Tracker CLI

A small command-line task tracker built with Python and SQLite.

This is a beginner-friendly project for practicing:

- Python functions
- command-line arguments
- SQLite database persistence
- basic CRUD operations
- simple terminal output

## Why I Built This

I built this project as a first practical Python + SQLite exercise. The goal was not to create a complex productivity app, but to understand how a small program can store data, read commands from the terminal, and update records in a local database.

## Features

- Add a new task
- List all tasks
- Mark a task as done
- Delete a task
- Store tasks locally in SQLite

## Tech Stack

- Python 3
- SQLite

No external packages are required.

## Usage

Clone the repository and run the commands from the project folder:

```bash
python3 app.py help
```

Add a task:

```bash
python3 app.py add "Learn Python basics"
```

List tasks:

```bash
python3 app.py list
```

Mark a task as done:

```bash
python3 app.py done 1
```

Delete a task:

```bash
python3 app.py delete 1
```

## Example Output

```text
Aufgabenliste:
--------------------------------------------------
  [1] done  Learn Python basics  (2026-05-17 00:39)
  [2] open  Write README  (2026-05-17 00:40)
--------------------------------------------------
```

## What I Learned

- How to create and connect to a SQLite database from Python
- How to create a database table automatically if it does not exist
- How to insert, update, delete and read records
- How to structure a small CLI program with functions
- How command-line arguments work with `sys.argv`

## Next Improvements

- Add due dates
- Add priorities
- Add categories
- Add search and filtering
- Improve error handling
- Add tests

## Project Status

First working version.

