import os
import json
import hashlib
import uuid

file_name = "task_data.json"

# ===== load and save file=====
def load_data():
    if not os.path.exists(file_name):
        return {"users": {}, "tasks": []}
    with open(file_name, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"users": {}, "tasks": []}


def save_data(data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


# ===== 1. User Authentication:=====
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    print('\n==Registration:==\n')
    data = {}
    data = load_data()
    
    while True:
        username = input("Enter an username: ").strip()
        if username:
            break
        print("Username cannot be empty.")
    if username in data["users"]:
        print("Error: Username already exists.")
        return
    while True:
        password = input("Enter a password: ").strip()
        if password:
            break
        print("Password cannot be empty.")
    data["users"][username] = hash_password(password)
    save_data(data)
    print("Registration successful!")


def login():
    print("\n==Login==\n")
    data = load_data()
    username = input("username: ").strip()
    password = input("password: ").strip()
    hashed_pw = hash_password(password)

    if data["users"].get(username) == hashed_pw:
        print(f"\nLog in Successful!, {username}!")
        return username
    
    print("Invalid username or password")
    return None


# ===== 2. Add a Task:=====
def add_task(username):
    print("\n==Add a Task==\n")
    data = load_data()

    while True:
        description = input("Enter task description: ")
        if description:
            break
        print("Task description cannot be empty.")

    task_id = uuid.uuid4().hex
    new_task = {
        "id": task_id,
        "user": username,
        "description": description,
        "status": "Pending"
    }
    
    data["tasks"].append(new_task)
    save_data(data)
    print(f"Task added! (ID: {task_id})")


# ===== 3. View Tasks:=====
def view_tasks(username):
    print("\n==View Tasks==\n")
    data = load_data()
    user_tasks = [t for t in data["tasks"] if t["user"] == username]
    if not user_tasks:
        print("You do not have any task.")
    for t in user_tasks:
        print(f"ID: {t['id']}, Description: {t['description']}, Status: {t['status']}")


# ===== 4.Mark a Task as Completed:=====
def mark_completed(username):
    print("\n==Mark a Task as Completed==\n")
    data = load_data()
    user_tasks = [t for t in data["tasks"] if t["user"] == username]
    if not user_tasks:
        print("You do not have any task.")
        return
    task_id = input("Enter Task ID to complete: ")
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = "Completed"
            save_data(data)
            print("Task marked as completed!")
            return


# ===== 5.Delete a Task:=====
def delete_task(username):
    print("\n==Delete a Task==\n")
    data = load_data()
    user_tasks = [t for t in data["tasks"] if t["user"] == username]
    if not user_tasks:
        print("You do not have any task.")
        return
    task_id = input("Enter Task ID to delete: ")
    data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]
    if len(data["tasks"]) < len(user_tasks):
        save_data(data)
        print("Task deleted.")
    else:
        print("Task ID not found.")


def auth_menu():
    while True:
        print("\n<<User Authentication>>\n")
        print("1) Add Register")
        print("2) Login")
        print("3) Exit")
        choice = input("Choose an option (1-3): ").strip()
  
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            task_menu(user)
        elif choice == "3":
            break
        else:
            print("Invalid option.")


def task_menu(username):
    
    while True:
        print("\n<<Task Manager>>\n")
        print("1) Add Task")
        print("2) View Tasks")
        print("3) Mark a Task as Completed")
        print("4) Delete a Task")
        print("5) Logout")

        choice = input("Choose an option: ")
        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option.")


def main():
    auth_menu()
    
        
    
if __name__ == "__main__":
    main()