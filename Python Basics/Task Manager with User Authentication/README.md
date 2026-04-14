# Task Manager with User Authentication

This project is a command-line task manager written in Python. It supports user registration, login, task creation, viewing tasks, marking tasks as completed, and deleting tasks.

## Files

- `tm.py`: Main Python application
- `task_data.json`: Stores registered users and task data
- `.gitignore`: Ignores project PDF, PNG, and Jupyter checkpoint files

## Features

- Register a new user
- Log in with a username and password
- Add tasks for the logged-in user
- View tasks that belong to the logged-in user
- Mark a task as completed
- Delete a task

## Data Storage

The program stores data in `task_data.json` using this structure:

- `users`: a dictionary of usernames and hashed passwords
- `tasks`: a list of task objects

Each task includes:

- `id`
- `user`
- `description`
- `status`

## Authentication

Passwords are hashed using SHA-256 before being saved. The script uses `hashlib.sha256()` to store a hashed version of the password instead of plain text.

## Main Functions

- `load_data()`: Loads JSON data or returns a default structure
- `save_data(data)`: Saves users and tasks to `task_data.json`
- `hash_password(password)`: Hashes passwords with SHA-256
- `register()`: Creates a new user account
- `login()`: Authenticates an existing user
- `add_task(username)`: Adds a task for the logged-in user
- `view_tasks(username)`: Shows tasks for the logged-in user
- `mark_completed(username)`: Marks a task as completed
- `delete_task(username)`: Deletes a task by ID
- `auth_menu()`: Displays the authentication menu
- `task_menu(username)`: Displays the task manager menu after login

## Menu Flow

When the program starts, it shows the authentication menu:

1. Register
2. Login
3. Exit

After login, it shows the task menu:

1. Add Task
2. View Tasks
3. Mark a Task as Completed
4. Delete a Task
5. Logout

## Run The Program

From the `Task Manager with User Authentication` directory:

```powershell
python tm.py
```

## Notes

- Task IDs are generated with `uuid.uuid4().hex`
- If `task_data.json` does not exist or is invalid, the program creates or uses an empty default data structure
- Tasks are filtered by username when viewed
- The current delete logic compares total tasks against the logged-in user's task count, so deletion feedback may not always be accurate if multiple users exist
- `auth_menu()` currently passes the login result directly to `task_menu()`, so a failed login may still enter the task menu with `None`
