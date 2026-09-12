import json
from pathlib import Path
from datetime import datetime
from getpass import getpass


# ============================================================
# LIFE OS
# ============================================================

DATABASE = "lifeos_data.json"
FILES_DIR = Path("lifeos_files")


# ============================================================
# DEFAULT DATABASE
# ============================================================

data = {
    "profile": []
}


# ============================================================
# LOAD DATABASE
# ============================================================

if Path(DATABASE).exists():

    try:
        with open(DATABASE, "r", encoding="utf-8") as f:
            content = f.read()

            if content.strip():
                data = json.loads(content)

    except json.JSONDecodeError:
        print("Database file is corrupted. Starting with empty database.")
        data = {"profile": []}


# ============================================================
# SAVE DATABASE
# ============================================================

def save():
    with open(DATABASE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ============================================================
# DECORATOR
# ============================================================

def decorator(func):

    def wrapper(*args, **kwargs):

        print("\n")
        print("------------------ Life OS ------------------")

        result = func(*args, **kwargs)

        print("---------------------------------------------")

        return result

    return wrapper


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def pause():

    input("\nPress Enter to continue...")


def get_number(message):

    while True:

        try:
            return int(input(message))

        except ValueError:
            print("Please enter a valid number.")


def get_float(message):

    while True:

        try:
            return float(input(message))

        except ValueError:
            print("Please enter a valid amount.")


# ============================================================
# LIFE OS
# ============================================================

class LifeOS:

    def show_dashboard(self, account):

        while True:

            print("""
==================================================
                    LIFE OS
==================================================

Welcome to your Personal Life Dashboard

1. Profile
2. Task Manager
3. Expense Manager
4. Notes Manager
5. Habit Tracker
6. File Manager
7. Dashboard & Statistics
8. Settings
9. Logout
10. Edit Profile
11. Exit

==================================================
""")

            choice = get_number("Choose input between 1-11: ")

            # ---------------------------------------------
            # PROFILE
            # ---------------------------------------------

            if choice == 1:

                account_actions.view_profile(account)
                pause()

            # ---------------------------------------------
            # TASK MANAGER
            # ---------------------------------------------

            elif choice == 2:

                taskmanager.menu(account)

            # ---------------------------------------------
            # EXPENSE MANAGER
            # ---------------------------------------------

            elif choice == 3:

                expensemanager.menu(account)

            # ---------------------------------------------
            # NOTES MANAGER
            # ---------------------------------------------

            elif choice == 4:

                notesmanager.menu(account)

            # ---------------------------------------------
            # HABIT TRACKER
            # ---------------------------------------------

            elif choice == 5:

                habitmanager.menu(account)

            # ---------------------------------------------
            # FILE MANAGER
            # ---------------------------------------------

            elif choice == 6:

                filemanager.menu(account)

            # ---------------------------------------------
            # DASHBOARD
            # ---------------------------------------------

            elif choice == 7:

                dashboard.show(account)
                pause()

            # ---------------------------------------------
            # SETTINGS
            # ---------------------------------------------

            elif choice == 8:

                settings.menu(account)

            # ---------------------------------------------
            # LOGOUT
            # ---------------------------------------------

            elif choice == 9:

                account_actions.logout()
                break

            # ---------------------------------------------
            # EDIT PROFILE
            # ---------------------------------------------

            elif choice == 10:

                account_actions.edit_profile(account)

            # ---------------------------------------------
            # EXIT
            # ---------------------------------------------

            elif choice == 11:

                print("\nExiting Life OS...")
                print("See you next time 👋")
                exit()

            else:

                print("Please choose between 1 and 11.")


# ============================================================
# ACCOUNT PROFILE
# ============================================================

class AccountProfileActions:

    @decorator
    def create_acc(self):

        print("\n========== CREATE ACCOUNT ==========\n")

        name = input("Enter your name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        age = get_number("Enter your age: ")

        if age <= 0:
            print("Age must be greater than 0.")
            return

        gender = input("Enter your gender: ").strip()

        gmail = input("Enter your gmail: ").strip().lower()

        if not gmail:
            print("Gmail cannot be empty.")
            return

        # ---------------------------------------------
        # CHECK EMAIL
        # ---------------------------------------------

        for account in data["profile"]:

            if account["gmail"] == gmail:

                print("An account with this Gmail already exists.")
                return

        # ---------------------------------------------
        # PASSWORD
        # ---------------------------------------------

        password = getpass("Enter your password: ")

        confirm_password = getpass("Confirm your password: ")

        if password != confirm_password:

            print("Password does not match.")
            return

        # ---------------------------------------------
        # CREATE ACCOUNT
        # ---------------------------------------------

        new_account = {

            "name": name,

            "age": age,

            "gender": gender,

            "gmail": gmail,

            "password": password,

            "tasks": {},

            "expenses": {},

            "notes": {},

            "habits": {},

            "settings": {

                "theme": "dark",

                "notifications": True

            },

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        data["profile"].append(new_account)

        save()

        print("\nAccount created successfully! 🎉")

        print("You can now login.")

    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        print("\n========== LOGIN ==========\n")

        confirm_gmail = input(
            "Enter your gmail: "
        ).strip().lower()

        confirm_password = getpass(
            "Enter password: "
        )

        for account in data["profile"]:

            if (
                confirm_gmail == account["gmail"]
                and
                confirm_password == account["password"]
            ):

                print("\nSuccessfully logged in! ✅")

                lifeos.show_dashboard(account)

                return

        print("\nInvalid credentials ❌")

    # ========================================================
    # VIEW PROFILE
    # ========================================================

    def view_profile(self, account):

        print("""
========== PROFILE ==========
""")

        print(f"Name       : {account['name']}")
        print(f"Age        : {account['age']}")
        print(f"Gender     : {account['gender']}")
        print(f"Gmail      : {account['gmail']}")
        print(f"Created At : {account['created_at']}")

        print("============================")

    # ========================================================
    # EDIT PROFILE
    # ========================================================

    def edit_profile(self, account):

        while True:

            print("""
========== EDIT PROFILE ==========

1. Change Name
2. Change Age
3. Change Gender
4. Change Gmail
5. Change Password
6. Back

===================================
""")

            choice = get_number("Choose: ")

            # ---------------------------------------------

            if choice == 1:

                name = input("Enter new name: ").strip()

                if name:

                    account["name"] = name
                    save()

                    print("Name updated successfully.")

            # ---------------------------------------------

            elif choice == 2:

                age = get_number("Enter new age: ")

                if age > 0:

                    account["age"] = age
                    save()

                    print("Age updated successfully.")

            # ---------------------------------------------

            elif choice == 3:

                gender = input(
                    "Enter new gender: "
                ).strip()

                account["gender"] = gender

                save()

                print("Gender updated successfully.")

            # ---------------------------------------------

            elif choice == 4:

                new_gmail = input(
                    "Enter new gmail: "
                ).strip().lower()

                exists = False

                for other in data["profile"]:

                    if (
                        other is not account
                        and
                        other["gmail"] == new_gmail
                    ):

                        exists = True
                        break

                if exists:

                    print(
                        "This Gmail is already being used."
                    )

                else:

                    account["gmail"] = new_gmail

                    save()

                    print(
                        "Gmail updated successfully."
                    )

            # ---------------------------------------------

            elif choice == 5:

                old_password = getpass(
                    "Enter current password: "
                )

                if old_password != account["password"]:

                    print("Incorrect password.")

                else:

                    new_password = getpass(
                        "Enter new password: "
                    )

                    confirm = getpass(
                        "Confirm new password: "
                    )

                    if new_password == confirm:

                        account["password"] = new_password

                        save()

                        print(
                            "Password changed successfully."
                        )

                    else:

                        print(
                            "Passwords do not match."
                        )

            # ---------------------------------------------

            elif choice == 6:

                break

            else:

                print("Invalid choice.")

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        print("\nLogged out successfully. 👋")


# ============================================================
# TASK MANAGER
# ============================================================

class TaskManager:

    def menu(self, account):

        while True:

            print("""
========== TASK MANAGER ==========

1. Create Task
2. View Tasks
3. Update Task Status
4. Delete Task
5. Back

===================================
""")

            choice = get_number("Choose: ")

            if choice == 1:

                self.create_task(account)

            elif choice == 2:

                self.view_tasks(account)

            elif choice == 3:

                self.update_task(account)

            elif choice == 4:

                self.delete_task(account)

            elif choice == 5:

                break

            else:

                print("Invalid choice.")

    # ========================================================

    def create_task(self, account):

        task = input(
            "\nWhat is your task? "
        ).strip()

        if not task:

            print("Task cannot be empty.")
            return

        if task in account["tasks"]:

            print("Task already exists.")
            return

        account["tasks"][task] = {

            "status": "not completed",

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        save()

        print("Task added successfully! ✅")

    # ========================================================

    def view_tasks(self, account):

        tasks = account["tasks"]

        if not tasks:

            print("\nNo tasks found.")
            return

        print("\n========== YOUR TASKS ==========\n")

        for index, (task, info) in enumerate(
            tasks.items(), 1
        ):

            print(
                f"{index}. {task} "
                f"[{info['status']}]"
            )

    # ========================================================

    def update_task(self, account):

        tasks = list(account["tasks"].keys())

        if not tasks:

            print("No tasks available.")
            return

        self.view_tasks(account)

        number = get_number(
            "\nEnter task number: "
        )

        if number < 1 or number > len(tasks):

            print("Invalid task number.")
            return

        task = tasks[number - 1]

        print("""
1. Completed
2. Not Completed
""")

        status = get_number("Choose status: ")

        if status == 1:

            account["tasks"][task]["status"] = "completed"

        elif status == 2:

            account["tasks"][task]["status"] = "not completed"

        else:

            print("Invalid status.")
            return

        save()

        print("Task status updated.")

    # ========================================================

    def delete_task(self, account):

        tasks = list(account["tasks"].keys())

        if not tasks:

            print("No tasks available.")
            return

        self.view_tasks(account)

        number = get_number(
            "\nEnter task number to delete: "
        )

        if number < 1 or number > len(tasks):

            print("Invalid task number.")
            return

        task = tasks[number - 1]

        del account["tasks"][task]

        save()

        print("Task deleted successfully.")


# ============================================================
# EXPENSE MANAGER
# ============================================================

class ExpenseManager:

    def menu(self, account):

        while True:

            print("""
========== EXPENSE MANAGER ==========

1. Add Expense
2. View Expenses
3. Delete Expense
4. Total Expenses
5. Back

======================================
""")

            choice = get_number("Choose: ")

            if choice == 1:

                self.add_expense(account)

            elif choice == 2:

                self.view_expenses(account)

            elif choice == 3:

                self.delete_expense(account)

            elif choice == 4:

                self.total_expenses(account)

            elif choice == 5:

                break

            else:

                print("Invalid choice.")

    # ========================================================

    def add_expense(self, account):

        title = input(
            "\nExpense name: "
        ).strip()

        if not title:

            print("Expense name cannot be empty.")
            return

        amount = get_float(
            "Amount: ₹"
        )

        if amount <= 0:

            print("Amount must be greater than 0.")
            return

        category = input(
            "Category: "
        ).strip()

        expense_id = str(
            len(account["expenses"]) + 1
        )

        account["expenses"][expense_id] = {

            "title": title,

            "amount": amount,

            "category": category,

            "date": datetime.now().strftime(
                "%Y-%m-%d"
            )
        }

        save()

        print("Expense added successfully.")

    # ========================================================

    def view_expenses(self, account):

        expenses = account["expenses"]

        if not expenses:

            print("\nNo expenses found.")
            return

        print("\n========== EXPENSES ==========\n")

        for expense_id, expense in expenses.items():

            print(
                f"{expense_id}. "
                f"{expense['title']} - "
                f"₹{expense['amount']:.2f} - "
                f"{expense['category']} - "
                f"{expense['date']}"
            )

    # ========================================================

    def delete_expense(self, account):

        if not account["expenses"]:

            print("No expenses available.")
            return

        self.view_expenses(account)

        expense_id = input(
            "\nEnter expense ID: "
        ).strip()

        if expense_id in account["expenses"]:

            del account["expenses"][expense_id]

            save()

            print("Expense deleted.")

        else:

            print("Invalid expense ID.")

    # ========================================================

    def total_expenses(self, account):

        total = sum(
            expense["amount"]
            for expense in account["expenses"].values()
        )

        print(
            f"\nTotal Expenses: ₹{total:.2f}"
        )


# ============================================================
# NOTES MANAGER
# ============================================================

class NotesManager:

    def menu(self, account):

        while True:

            print("""
========== NOTES MANAGER ==========

1. Create Note
2. View Notes
3. Delete Note
4. Back

====================================
""")

            choice = get_number("Choose: ")

            if choice == 1:

                self.create_note(account)

            elif choice == 2:

                self.view_notes(account)

            elif choice == 3:

                self.delete_note(account)

            elif choice == 4:

                break

            else:

                print("Invalid choice.")

    # ========================================================

    def create_note(self, account):

        title = input(
            "\nNote title: "
        ).strip()

        if not title:

            print("Title cannot be empty.")
            return

        content = input(
            "Write your note: "
        ).strip()

        account["notes"][title] = {

            "content": content,

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        save()

        print("Note saved successfully. 📝")

    # ========================================================

    def view_notes(self, account):

        notes = account["notes"]

        if not notes:

            print("\nNo notes found.")
            return

        print("\n========== NOTES ==========\n")

        for title, note in notes.items():

            print(f"Title: {title}")
            print(f"Content: {note['content']}")
            print(f"Created: {note['created_at']}")
            print("----------------------------")

    # ========================================================

    def delete_note(self, account):

        if not account["notes"]:

            print("No notes available.")
            return

        self.view_notes(account)

        title = input(
            "\nEnter note title to delete: "
        ).strip()

        if title in account["notes"]:

            del account["notes"][title]

            save()

            print("Note deleted.")

        else:

            print("Note not found.")


# ============================================================
# HABIT MANAGER
# ============================================================

class HabitManager:

    def menu(self, account):

        while True:

            print("""
========== HABIT TRACKER ==========

1. Add Habit
2. View Habits
3. Mark Habit Complete
4. Delete Habit
5. Back

====================================
""")

            choice = get_number("Choose: ")

            if choice == 1:

                self.add_habit(account)

            elif choice == 2:

                self.view_habits(account)

            elif choice == 3:

                self.complete_habit(account)

            elif choice == 4:

                self.delete_habit(account)

            elif choice == 5:

                break

            else:

                print("Invalid choice.")

    # ========================================================

    def add_habit(self, account):

        habit = input(
            "\nHabit name: "
        ).strip()

        if not habit:

            print("Habit cannot be empty.")
            return

        if habit in account["habits"]:

            print("Habit already exists.")
            return

        account["habits"][habit] = {

            "completed_dates": [],

            "created_at": datetime.now().strftime(
                "%Y-%m-%d"
            )
        }

        save()

        print("Habit added successfully. 🔥")

    # ========================================================

    def view_habits(self, account):

        if not account["habits"]:

            print("\nNo habits found.")
            return

        print("\n========== HABITS ==========\n")

        for habit, info in account["habits"].items():

            count = len(
                info["completed_dates"]
            )

            print(
                f"{habit} | "
                f"Completed: {count} days"
            )

    # ========================================================

    def complete_habit(self, account):

        habits = list(account["habits"].keys())

        if not habits:

            print("No habits available.")
            return

        self.view_habits(account)

        habit_number = get_number(
            "\nEnter habit number: "
        )

        if (
            habit_number < 1
            or
            habit_number > len(habits)
        ):

            print("Invalid habit number.")
            return

        habit = habits[habit_number - 1]

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        completed_dates = account[
            "habits"
        ][habit]["completed_dates"]

        if today in completed_dates:

            print(
                "You already completed this habit today."
            )

            return

        completed_dates.append(today)

        save()

        print(
            f"🔥 {habit} completed today!"
        )

    # ========================================================

    def delete_habit(self, account):

        if not account["habits"]:

            print("No habits available.")
            return

        self.view_habits(account)

        habit = input(
            "\nEnter habit name to delete: "
        ).strip()

        if habit in account["habits"]:

            del account["habits"][habit]

            save()

            print("Habit deleted.")

        else:

            print("Habit not found.")


# ============================================================
# FILE MANAGER
# ============================================================

class FileManager:

    def __init__(self):

        FILES_DIR.mkdir(exist_ok=True)

    # ========================================================

    def menu(self, account):

        while True:

            print("""
========== FILE MANAGER ==========

1. Create File
2. List Files
3. Read File
4. Delete File
5. Back

==================================
""")

            choice = get_number("Choose: ")

            if choice == 1:

                self.create_file()

            elif choice == 2:

                self.list_files()

            elif choice == 3:

                self.read_file()

            elif choice == 4:

                self.delete_file()

            elif choice == 5:

                break

            else:

                print("Invalid choice.")

    # ========================================================

    def create_file(self):

        filename = input(
            "\nEnter filename: "
        ).strip()

        if not filename:

            print("Filename cannot be empty.")
            return

        file_path = FILES_DIR / filename

        content = input(
            "Enter file content: "
        )

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(content)

            print("File created successfully.")

        except OSError as e:

            print(
                f"Could not create file: {e}"
            )

    # ========================================================

    def list_files(self):

        files = list(FILES_DIR.iterdir())

        if not files:

            print("\nNo files found.")
            return

        print("\n========== FILES ==========\n")

        for index, file in enumerate(files, 1):

            if file.is_file():

                print(
                    f"{index}. {file.name}"
                )

    # ========================================================

    def read_file(self):

        filename = input(
            "\nEnter filename: "
        ).strip()

        file_path = FILES_DIR / filename

        if not file_path.exists():

            print("File not found.")
            return

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

            print("\n========== FILE CONTENT ==========\n")
            print(content)

        except OSError as e:

            print(
                f"Could not read file: {e}"
            )

    # ========================================================

    def delete_file(self):

        filename = input(
            "\nEnter filename to delete: "
        ).strip()

        file_path = FILES_DIR / filename

        if not file_path.exists():

            print("File not found.")
            return

        try:

            file_path.unlink()

            print("File deleted successfully.")

        except OSError as e:

            print(
                f"Could not delete file: {e}"
            )


# ============================================================
# DASHBOARD & STATISTICS
# ============================================================

class DashboardStatistics:

    def show(self, account):

        tasks = account["tasks"]

        expenses = account["expenses"]

        notes = account["notes"]

        habits = account["habits"]

        total_tasks = len(tasks)

        completed_tasks = sum(
            1
            for task in tasks.values()
            if task["status"] == "completed"
        )

        pending_tasks = (
            total_tasks - completed_tasks
        )

        total_expenses = sum(
            expense["amount"]
            for expense in expenses.values()
        )

        total_notes = len(notes)

        total_habits = len(habits)

        habit_completions = sum(
            len(habit["completed_dates"])
            for habit in habits.values()
        )

        print("""
==================================================
              DASHBOARD & STATISTICS
==================================================
""")

        print(f"👤 User              : {account['name']}")

        print()

        print("---------- TASKS ----------")

        print(
            f"Total Tasks          : {total_tasks}"
        )

        print(
            f"Completed Tasks      : {completed_tasks}"
        )

        print(
            f"Pending Tasks        : {pending_tasks}"
        )

        print()

        print("---------- EXPENSES ----------")

        print(
            f"Total Expenses       : ₹{total_expenses:.2f}"
        )

        print()

        print("---------- NOTES ----------")

        print(
            f"Total Notes          : {total_notes}"
        )

        print()

        print("---------- HABITS ----------")

        print(
            f"Total Habits         : {total_habits}"
        )

        print(
            f"Total Completions    : {habit_completions}"
        )

        print("""
==================================================
""")


# ============================================================
# SETTINGS
# ============================================================

class Settings:

    def menu(self, account):

        while True:

            print("""
========== SETTINGS ==========

1. View Settings
2. Toggle Notifications
3. Change Theme
4. Back

===============================
""")

            choice = get_number("Choose: ")

            if choice == 1:

                self.view_settings(account)

            elif choice == 2:

                self.toggle_notifications(account)

            elif choice == 3:

                self.change_theme(account)

            elif choice == 4:

                break

            else:

                print("Invalid choice.")

    # ========================================================

    def view_settings(self, account):

        settings = account["settings"]

        print("\n========== SETTINGS ==========\n")

        print(
            f"Theme         : {settings['theme']}"
        )

        print(
            f"Notifications : {settings['notifications']}"
        )

    # ========================================================

    def toggle_notifications(self, account):

        current = account[
            "settings"
        ]["notifications"]

        account[
            "settings"
        ]["notifications"] = not current

        save()

        print(
            "Notifications:",
            account["settings"]["notifications"]
        )

    # ========================================================

    def change_theme(self, account):

        print("""
1. Dark
2. Light
""")

        choice = get_number("Choose theme: ")

        if choice == 1:

            account["settings"]["theme"] = "dark"

        elif choice == 2:

            account["settings"]["theme"] = "light"

        else:

            print("Invalid choice.")
            return

        save()

        print("Theme updated successfully.")


# ============================================================
# CREATE OBJECTS
# ============================================================

lifeos = LifeOS()

account_actions = AccountProfileActions()

taskmanager = TaskManager()

expensemanager = ExpenseManager()

notesmanager = NotesManager()

habitmanager = HabitManager()

filemanager = FileManager()

dashboard = DashboardStatistics()

settings = Settings()


# ============================================================
# START LIFE OS
# ============================================================

def start():

    print("""
==================================================
                 WELCOME TO LIFE OS
==================================================
""")

    # --------------------------------------------------------
    # If accounts exist
    # --------------------------------------------------------

    if data["profile"]:

        while True:

            print("""
1. Login
2. Create New Account
3. Exit
""")

            choice = get_number(
                "Choose: "
            )

            if choice == 1:

                account_actions.login()

                break

            elif choice == 2:

                account_actions.create_acc()

                # Login after account creation

                if data["profile"]:

                    account_actions.login()

                break

            elif choice == 3:

                print(
                    "Exiting Life OS..."
                )

                break

            else:

                print(
                    "Please choose 1-3."
                )

    # --------------------------------------------------------
    # No account
    # --------------------------------------------------------

    else:

        print(
            "No account found. "
            "Please create an account."
        )

        account_actions.create_acc()

        if data["profile"]:

            account_actions.login()


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    start()