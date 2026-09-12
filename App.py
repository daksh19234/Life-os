import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import pandas as pd


# ============================================================
# CONFIG
# ============================================================

DATABASE = "lifeos_data.json"
FILES_DIR = Path("lifeos_files")

FILES_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="Life OS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE
# ============================================================

def load_database():

    default_data = {
        "profile": []
    }

    if not Path(DATABASE).exists():
        return default_data

    try:
        with open(DATABASE, "r", encoding="utf-8") as f:

            content = f.read()

            if content.strip():
                return json.loads(content)

    except (json.JSONDecodeError, OSError):
        pass

    return default_data


data = load_database()


def save_database():

    with open(DATABASE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# CSS
# ============================================================

def apply_theme():

    account = st.session_state.account

    theme = "dark"

    if account:
        theme = account.get("settings", {}).get("theme", "dark")

    if theme == "dark":

        st.markdown(
            """
            <style>

            .stApp {
                background-color: #0b0f19;
                color: #f1f5f9;
            }

            [data-testid="stSidebar"] {
                background-color: #111827;
            }

            .life-card {
                background: #111827;
                border: 1px solid #263244;
                border-radius: 18px;
                padding: 22px;
                margin-bottom: 15px;
            }

            .metric-card {
                background: #111827;
                border: 1px solid #263244;
                border-radius: 18px;
                padding: 20px;
                text-align: center;
            }

            .metric-number {
                font-size: 30px;
                font-weight: 700;
            }

            .metric-label {
                color: #94a3b8;
                font-size: 14px;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <style>

            .stApp {
                background-color: #f8fafc;
                color: #0f172a;
            }

            [data-testid="stSidebar"] {
                background-color: #ffffff;
            }

            .life-card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 22px;
                margin-bottom: 15px;
            }

            .metric-card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 20px;
                text-align: center;
            }

            .metric-number {
                font-size: 30px;
                font-weight: 700;
            }

            .metric-label {
                color: #64748b;
                font-size: 14px;
            }

            </style>
            """,
            unsafe_allow_html=True
        )


apply_theme()


# ============================================================
# HELPERS
# ============================================================

def current_account():

    return st.session_state.account


def refresh_account():

    gmail = st.session_state.account["gmail"]

    for account in data["profile"]:

        if account["gmail"] == gmail:

            st.session_state.account = account
            return account

    return st.session_state.account


def metric_card(label, value, icon):

    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size:25px">{icon}</div>
            <div class="metric-number">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def success(message):

    st.success(message)


# ============================================================
# LOGIN / REGISTER
# ============================================================

def authentication():

    st.markdown(
        """
        <div style="text-align:center; padding:50px 0 20px 0">
            <h1>🚀 LIFE OS</h1>
            <p style="font-size:18px">
                Your Personal Life Dashboard
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )

    # ========================================================
    # LOGIN
    # ========================================================

    with tab1:

        with st.form("login_form"):

            gmail = st.text_input(
                "Gmail",
                placeholder="you@gmail.com"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

            if submitted:

                gmail = gmail.strip().lower()

                account_found = None

                for account in data["profile"]:

                    if (
                        account.get("gmail") == gmail
                        and
                        account.get("password") == password
                    ):
                        account_found = account
                        break

                if account_found:

                    st.session_state.logged_in = True
                    st.session_state.account = account_found
                    st.session_state.page = "Dashboard"

                    st.success(
                        "Successfully logged in! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid Gmail or password."
                    )

    # ========================================================
    # CREATE ACCOUNT
    # ========================================================

    with tab2:

        with st.form("register_form"):

            name = st.text_input("Name")

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=18
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Prefer not to say",
                    "Male",
                    "Female",
                    "Other"
                ]
            )

            gmail = st.text_input(
                "Gmail"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if submitted:

                name = name.strip()
                gmail = gmail.strip().lower()

                if not name:

                    st.error("Name cannot be empty.")

                elif not gmail:

                    st.error("Gmail cannot be empty.")

                elif not password:

                    st.error("Password cannot be empty.")

                elif password != confirm_password:

                    st.error("Passwords do not match.")

                elif any(
                    a.get("gmail") == gmail
                    for a in data["profile"]
                ):

                    st.error(
                        "An account with this Gmail already exists."
                    )

                else:

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

                        "created_at":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                    }

                    data["profile"].append(
                        new_account
                    )

                    save_database()

                    st.success(
                        "Account created successfully! 🎉"
                    )

                    st.info(
                        "Go to the Login tab to sign in."
                    )


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    account = current_account()

    st.sidebar.markdown(
        """
        # 🚀 Life OS
        """
    )

    st.sidebar.markdown(
        f"### 👋 {account['name']}"
    )

    st.sidebar.caption(
        account["gmail"]
    )

    st.sidebar.divider()

    pages = {
        "🏠 Dashboard": "Dashboard",
        "👤 Profile": "Profile",
        "✅ Tasks": "Tasks",
        "💰 Expenses": "Expenses",
        "📝 Notes": "Notes",
        "🔥 Habits": "Habits",
        "📁 Files": "Files",
        "⚙️ Settings": "Settings"
    }

    for label, page in pages.items():

        if st.sidebar.button(
            label,
            use_container_width=True
        ):

            st.session_state.page = page
            st.rerun()

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.account = None
        st.session_state.page = "Dashboard"

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    account = refresh_account()

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

    habit_completions = sum(
        len(habit["completed_dates"])
        for habit in habits.values()
    )

    st.title("🏠 Dashboard")

    st.caption(
        f"Welcome back, {account['name']} 👋"
    )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Total Tasks",
            total_tasks,
            "✅"
        )

    with c2:
        metric_card(
            "Completed",
            completed_tasks,
            "🎯"
        )

    with c3:
        metric_card(
            "Expenses",
            f"₹{total_expenses:,.2f}",
            "💰"
        )

    with c4:
        metric_card(
            "Habit Streaks",
            habit_completions,
            "🔥"
        )

    st.write("")

    left, right = st.columns(2)

    # ========================================================
    # TASK SUMMARY
    # ========================================================

    with left:

        st.subheader("📋 Task Overview")

        if total_tasks == 0:

            st.info("No tasks yet.")

        else:

            task_data = pd.DataFrame(
                {
                    "Status": [
                        "Completed",
                        "Pending"
                    ],
                    "Count": [
                        completed_tasks,
                        pending_tasks
                    ]
                }
            )

            st.bar_chart(
                task_data.set_index("Status")
            )

    # ========================================================
    # EXPENSE SUMMARY
    # ========================================================

    with right:

        st.subheader("💰 Expense Overview")

        if expenses:

            category_totals = {}

            for expense in expenses.values():

                category = (
                    expense.get("category")
                    or "Other"
                )

                category_totals[category] = (
                    category_totals.get(category, 0)
                    + expense["amount"]
                )

            expense_df = pd.DataFrame(
                {
                    "Category":
                        list(category_totals.keys()),

                    "Amount":
                        list(category_totals.values())
                }
            )

            st.bar_chart(
                expense_df.set_index("Category")
            )

        else:

            st.info("No expenses yet.")

    # ========================================================
    # RECENT TASKS
    # ========================================================

    st.subheader("📝 Recent Tasks")

    if tasks:

        for task, info in list(
            tasks.items()
        )[-5:]:

            if info["status"] == "completed":

                st.success(
                    f"✅ {task}"
                )

            else:

                st.warning(
                    f"⏳ {task}"
                )

    else:

        st.info("Create your first task.")


# ============================================================
# PROFILE
# ============================================================

def profile_page():

    account = refresh_account()

    st.title("👤 Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="life-card">

            ### 👤 Personal Information

            **Name:** {account['name']}

            **Age:** {account['age']}

            **Gender:** {account['gender']}

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="life-card">

            ### 📧 Account Information

            **Gmail:** {account['gmail']}

            **Created:** {account['created_at']}

            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("✏️ Edit Profile")

    with st.form("profile_edit"):

        name = st.text_input(
            "Name",
            value=account["name"]
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=int(account["age"])
        )

        gender = st.text_input(
            "Gender",
            value=account["gender"]
        )

        gmail = st.text_input(
            "Gmail",
            value=account["gmail"]
        ).strip().lower()

        submitted = st.form_submit_button(
            "Save Changes",
            use_container_width=True
        )

        if submitted:

            duplicate = any(
                other is not account
                and other.get("gmail") == gmail
                for other in data["profile"]
            )

            if duplicate:

                st.error(
                    "This Gmail is already being used."
                )

            elif not name.strip():

                st.error(
                    "Name cannot be empty."
                )

            else:

                account["name"] = name.strip()
                account["age"] = age
                account["gender"] = gender.strip()
                account["gmail"] = gmail

                save_database()

                st.success(
                    "Profile updated successfully! ✅"
                )

                st.rerun()

    st.subheader("🔑 Change Password")

    with st.form("password_change"):

        old_password = st.text_input(
            "Current Password",
            type="password"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm New Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Change Password"
        )

        if submitted:

            if old_password != account["password"]:

                st.error(
                    "Incorrect current password."
                )

            elif new_password != confirm:

                st.error(
                    "Passwords do not match."
                )

            elif not new_password:

                st.error(
                    "Password cannot be empty."
                )

            else:

                account["password"] = new_password

                save_database()

                st.success(
                    "Password changed successfully! 🔐"
                )


# ============================================================
# TASKS
# ============================================================

def tasks_page():

    account = refresh_account()

    st.title("✅ Task Manager")

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Create",
            "📋 Tasks",
            "🗑️ Manage"
        ]
    )

    # ========================================================
    # CREATE
    # ========================================================

    with tab1:

        with st.form("create_task"):

            task = st.text_input(
                "Task",
                placeholder="Finish Python project..."
            )

            submitted = st.form_submit_button(
                "Add Task",
                use_container_width=True
            )

            if submitted:

                task = task.strip()

                if not task:

                    st.error(
                        "Task cannot be empty."
                    )

                elif task in account["tasks"]:

                    st.error(
                        "Task already exists."
                    )

                else:

                    account["tasks"][task] = {

                        "status": "not completed",

                        "created_at":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                    }

                    save_database()

                    st.success(
                        "Task added successfully! 🎯"
                    )

    # ========================================================
    # VIEW
    # ========================================================

    with tab2:

        if not account["tasks"]:

            st.info(
                "No tasks found. Create one!"
            )

        else:

            for task, info in account[
                "tasks"
            ].items():

                col1, col2, col3 = st.columns(
                    [5, 2, 1]
                )

                with col1:

                    if info["status"] == "completed":

                        st.markdown(
                            f"~~{task}~~"
                        )

                    else:

                        st.write(
                            f"**{task}**"
                        )

                with col2:

                    st.caption(
                        info["status"]
                    )

                with col3:

                    if st.button(
                        "🔄",
                        key=f"task_{task}"
                    ):

                        if (
                            info["status"]
                            == "completed"
                        ):

                            info["status"] = (
                                "not completed"
                            )

                        else:

                            info["status"] = (
                                "completed"
                            )

                        save_database()
                        st.rerun()

    # ========================================================
    # DELETE
    # ========================================================

    with tab3:

        if account["tasks"]:

            task = st.selectbox(
                "Select task",
                list(account["tasks"].keys())
            )

            if st.button(
                "🗑️ Delete Task",
                type="secondary"
            ):

                del account["tasks"][task]

                save_database()

                st.success(
                    "Task deleted."
                )

                st.rerun()

        else:

            st.info("No tasks available.")


# ============================================================
# EXPENSES
# ============================================================

def expenses_page():

    account = refresh_account()

    st.title("💰 Expense Manager")

    total = sum(
        expense["amount"]
        for expense in account["expenses"].values()
    )

    st.metric(
        "Total Expenses",
        f"₹{total:,.2f}"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Expense",
            "📋 View Expenses",
            "📊 Analytics"
        ]
    )

    # ========================================================
    # ADD
    # ========================================================

    with tab1:

        with st.form("expense_form"):

            title = st.text_input(
                "Expense Name",
                placeholder="Coffee"
            )

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.01,
                step=10.0
            )

            category = st.selectbox(
                "Category",
                [
                    "Food",
                    "Transport",
                    "Shopping",
                    "Bills",
                    "Entertainment",
                    "Education",
                    "Health",
                    "Other"
                ]
            )

            submitted = st.form_submit_button(
                "Add Expense",
                use_container_width=True
            )

            if submitted:

                title = title.strip()

                if not title:

                    st.error(
                        "Expense name cannot be empty."
                    )

                else:

                    expense_id = str(
                        len(account["expenses"]) + 1
                    )

                    while expense_id in account[
                        "expenses"
                    ]:

                        expense_id = str(
                            int(expense_id) + 1
                        )

                    account["expenses"][
                        expense_id
                    ] = {

                        "title": title,

                        "amount": float(amount),

                        "category": category,

                        "date":
                            datetime.now().strftime(
                                "%Y-%m-%d"
                            )
                    }

                    save_database()

                    st.success(
                        "Expense added successfully! 💰"
                    )

                    st.rerun()

    # ========================================================
    # VIEW
    # ========================================================

    with tab2:

        if not account["expenses"]:

            st.info("No expenses found.")

        else:

            rows = []

            for expense_id, expense in account[
                "expenses"
            ].items():

                rows.append(
                    {
                        "ID": expense_id,
                        "Expense": expense["title"],
                        "Amount":
                            f"₹{expense['amount']:,.2f}",
                        "Category":
                            expense["category"],
                        "Date":
                            expense["date"]
                    }
                )

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            expense_id = st.selectbox(
                "Select expense to delete",
                list(
                    account["expenses"].keys()
                )
            )

            if st.button(
                "🗑️ Delete Expense"
            ):

                del account["expenses"][
                    expense_id
                ]

                save_database()

                st.success(
                    "Expense deleted."
                )

                st.rerun()

    # ========================================================
    # ANALYTICS
    # ========================================================

    with tab3:

        if not account["expenses"]:

            st.info(
                "Add expenses to see analytics."
            )

        else:

            category_totals = {}

            for expense in account[
                "expenses"
            ].values():

                category = (
                    expense.get("category")
                    or "Other"
                )

                category_totals[category] = (
                    category_totals.get(category, 0)
                    + expense["amount"]
                )

            chart_df = pd.DataFrame(
                {
                    "Category":
                        list(category_totals.keys()),

                    "Amount":
                        list(category_totals.values())
                }
            )

            st.bar_chart(
                chart_df.set_index("Category")
            )


# ============================================================
# NOTES
# ============================================================

def notes_page():

    account = refresh_account()

    st.title("📝 Notes Manager")

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ New Note",
            "📚 My Notes",
            "🗑️ Delete"
        ]
    )

    # ========================================================
    # CREATE
    # ========================================================

    with tab1:

        with st.form("note_form"):

            title = st.text_input(
                "Note Title"
            )

            content = st.text_area(
                "Note",
                height=250
            )

            submitted = st.form_submit_button(
                "Save Note",
                use_container_width=True
            )

            if submitted:

                title = title.strip()

                if not title:

                    st.error(
                        "Title cannot be empty."
                    )

                else:

                    account["notes"][title] = {

                        "content": content,

                        "created_at":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                    }

                    save_database()

                    st.success(
                        "Note saved successfully! 📝"
                    )

                    st.rerun()

    # ========================================================
    # VIEW
    # ========================================================

    with tab2:

        if not account["notes"]:

            st.info("No notes found.")

        else:

            for title, note in account[
                "notes"
            ].items():

                with st.expander(
                    f"📝 {title}"
                ):

                    st.write(
                        note["content"]
                    )

                    st.caption(
                        f"Created: {note['created_at']}"
                    )

    # ========================================================
    # DELETE
    # ========================================================

    with tab3:

        if account["notes"]:

            title = st.selectbox(
                "Select note",
                list(account["notes"].keys())
            )

            if st.button(
                "🗑️ Delete Note"
            ):

                del account["notes"][title]

                save_database()

                st.success(
                    "Note deleted."
                )

                st.rerun()

        else:

            st.info("No notes available.")


# ============================================================
# HABITS
# ============================================================

def habits_page():

    account = refresh_account()

    st.title("🔥 Habit Tracker")

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Habit",
            "🔥 My Habits",
            "🗑️ Delete"
        ]
    )

    # ========================================================
    # ADD
    # ========================================================

    with tab1:

        with st.form("habit_form"):

            habit = st.text_input(
                "Habit Name",
                placeholder="Workout"
            )

            submitted = st.form_submit_button(
                "Add Habit",
                use_container_width=True
            )

            if submitted:

                habit = habit.strip()

                if not habit:

                    st.error(
                        "Habit cannot be empty."
                    )

                elif habit in account["habits"]:

                    st.error(
                        "Habit already exists."
                    )

                else:

                    account["habits"][habit] = {

                        "completed_dates": [],

                        "created_at":
                            datetime.now().strftime(
                                "%Y-%m-%d"
                            )
                    }

                    save_database()

                    st.success(
                        "Habit added successfully! 🔥"
                    )

                    st.rerun()

    # ========================================================
    # VIEW
    # ========================================================

    with tab2:

        if not account["habits"]:

            st.info(
                "No habits yet. Add your first habit!"
            )

        else:

            for habit, info in account[
                "habits"
            ].items():

                completed_dates = info[
                    "completed_dates"
                ]

                count = len(
                    completed_dates
                )

                col1, col2, col3 = st.columns(
                    [5, 2, 2]
                )

                with col1:

                    st.markdown(
                        f"### 🔥 {habit}"
                    )

                with col2:

                    st.metric(
                        "Days",
                        count
                    )

                with col3:

                    if today in completed_dates:

                        st.success(
                            "Done today ✓"
                        )

                    else:

                        if st.button(
                            "Complete",
                            key=f"habit_{habit}"
                        ):

                            completed_dates.append(
                                today
                            )

                            save_database()

                            st.success(
                                f"{habit} completed! 🔥"
                            )

                            st.rerun()

    # ========================================================
    # DELETE
    # ========================================================

    with tab3:

        if account["habits"]:

            habit = st.selectbox(
                "Select habit",
                list(account["habits"].keys())
            )

            if st.button(
                "🗑️ Delete Habit"
            ):

                del account["habits"][habit]

                save_database()

                st.success(
                    "Habit deleted."
                )

                st.rerun()

        else:

            st.info("No habits available.")


# ============================================================
# FILE MANAGER
# ============================================================

def safe_file_path(filename):

    filename = Path(filename).name

    return FILES_DIR / filename


def files_page():

    st.title("📁 File Manager")

    files = [
        f for f in FILES_DIR.iterdir()
        if f.is_file()
    ]

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "➕ Create",
            "📋 Files",
            "📖 Read",
            "🗑️ Delete"
        ]
    )

    # ========================================================
    # CREATE
    # ========================================================

    with tab1:

        with st.form("file_create"):

            filename = st.text_input(
                "Filename",
                placeholder="my_notes.txt"
            )

            content = st.text_area(
                "File Content",
                height=250
            )

            submitted = st.form_submit_button(
                "Create File",
                use_container_width=True
            )

            if submitted:

                filename = Path(
                    filename.strip()
                ).name

                if not filename:

                    st.error(
                        "Filename cannot be empty."
                    )

                else:

                    path = safe_file_path(
                        filename
                    )

                    try:

                        with open(
                            path,
                            "w",
                            encoding="utf-8"
                        ) as f:

                            f.write(content)

                        st.success(
                            "File created successfully! 📁"
                        )

                    except OSError as e:

                        st.error(
                            f"Could not create file: {e}"
                        )

    # ========================================================
    # LIST
    # ========================================================

    with tab2:

        if not files:

            st.info("No files found.")

        else:

            for index, file in enumerate(
                files,
                1
            ):

                st.write(
                    f"**{index}.** {file.name}"
                )

    # ========================================================
    # READ
    # ========================================================

    with tab3:

        if not files:

            st.info("No files available.")

        else:

            filename = st.selectbox(
                "Select file",
                [f.name for f in files]
            )

            path = safe_file_path(
                filename
            )

            if st.button(
                "📖 Read File"
            ):

                try:

                    with open(
                        path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        content = f.read()

                    st.text_area(
                        "File Content",
                        value=content,
                        height=400
                    )

                except OSError as e:

                    st.error(
                        f"Could not read file: {e}"
                    )

    # ========================================================
    # DELETE
    # ========================================================

    with tab4:

        if not files:

            st.info("No files available.")

        else:

            filename = st.selectbox(
                "File to delete",
                [f.name for f in files],
                key="delete_file"
            )

            if st.button(
                "🗑️ Delete File"
            ):

                path = safe_file_path(
                    filename
                )

                try:

                    path.unlink()

                    st.success(
                        "File deleted successfully."
                    )

                    st.rerun()

                except OSError as e:

                    st.error(
                        f"Could not delete file: {e}"
                    )


# ============================================================
# SETTINGS
# ============================================================

def settings_page():

    account = refresh_account()

    st.title("⚙️ Settings")

    settings = account["settings"]

    st.subheader("🎨 Appearance")

    current_theme = settings.get(
        "theme",
        "dark"
    )

    theme = st.radio(
        "Theme",
        ["dark", "light"],
        index=(
            0
            if current_theme == "dark"
            else 1
        ),
        horizontal=True
    )

    st.subheader("🔔 Notifications")

    notifications = st.toggle(
        "Enable Notifications",
        value=settings.get(
            "notifications",
            True
        )
    )

    if st.button(
        "💾 Save Settings",
        use_container_width=True
    ):

        settings["theme"] = theme
        settings["notifications"] = notifications

        save_database()

        st.success(
            "Settings saved successfully! ⚙️"
        )

        st.rerun()

    st.divider()

    st.subheader("ℹ️ Life OS Information")

    st.write(
        "Life OS is your personal productivity dashboard."
    )

    st.caption(
        "Data is stored locally in lifeos_data.json."
    )


# ============================================================
# STATISTICS
# ============================================================

def statistics_page():

    account = refresh_account()

    st.title("📊 Dashboard & Statistics")

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

    total_completions = sum(
        len(h["completed_dates"])
        for h in habits.values()
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Tasks",
            total_tasks,
            "📋"
        )

    with c2:
        metric_card(
            "Completed",
            completed_tasks,
            "🎯"
        )

    with c3:
        metric_card(
            "Notes",
            total_notes,
            "📝"
        )

    with c4:
        metric_card(
            "Habits",
            total_habits,
            "🔥"
        )

    st.write("")

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("📋 Task Statistics")

        task_df = pd.DataFrame(
            {
                "Status": [
                    "Completed",
                    "Pending"
                ],

                "Tasks": [
                    completed_tasks,
                    pending_tasks
                ]
            }
        )

        st.bar_chart(
            task_df.set_index("Status")
        )

    with c2:

        st.subheader("💰 Expense Statistics")

        if expenses:

            category_totals = {}

            for expense in expenses.values():

                category = (
                    expense.get("category")
                    or "Other"
                )

                category_totals[category] = (
                    category_totals.get(
                        category,
                        0
                    )
                    + expense["amount"]
                )

            df = pd.DataFrame(
                {
                    "Category":
                        list(
                            category_totals.keys()
                        ),

                    "Amount":
                        list(
                            category_totals.values()
                        )
                }
            )

            st.bar_chart(
                df.set_index("Category")
            )

        else:

            st.info("No expenses.")

    st.divider()

    st.subheader("🔥 Habit Statistics")

    st.metric(
        "Total Habit Completions",
        total_completions
    )

    st.metric(
        "Total Money Spent",
        f"₹{total_expenses:,.2f}"
    )


# ============================================================
# MAIN APP
# ============================================================

def main():

    if not st.session_state.logged_in:

        authentication()

        return

    sidebar()

    page = st.session_state.page

    if page == "Dashboard":

        dashboard_page()

    elif page == "Profile":

        profile_page()

    elif page == "Tasks":

        tasks_page()

    elif page == "Expenses":

        expenses_page()

    elif page == "Notes":

        notes_page()

    elif page == "Habits":

        habits_page()

    elif page == "Files":

        files_page()

    elif page == "Settings":

        settings_page()

    elif page == "Statistics":

        statistics_page()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()

