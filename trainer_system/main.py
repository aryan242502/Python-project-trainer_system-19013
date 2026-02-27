import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

# ================= COLORS =================
BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#e2e8f0"
ACCENT = "#38bdf8"
GREEN = "#22c55e"
RED = "#ef4444"
YELLOW = "#f59e0b"

# ================= DATABASE =================
def connect_db():
    return sqlite3.connect("gym.db")

def create_tables():
    conn = connect_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS trainers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        specialization TEXT,
        experience TEXT,
        salary TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        trainer_id INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trainer_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# ================= LOGIN WINDOW =================
login_window = tk.Tk()
login_window.title("Admin Login")
login_window.geometry("360x500")
login_window.configure(bg=BG)

login_user = tk.StringVar()
login_pass = tk.StringVar()

tk.Label(login_window, text="Gym Admin",
         font=("Segoe UI", 18, "bold"),
         bg=BG, fg=ACCENT).pack(pady=20)

frame_login = tk.Frame(login_window, bg=CARD, padx=20, pady=20)
frame_login.pack(pady=10, fill="x", padx=20)

tk.Label(frame_login, text="Username", bg=CARD, fg=TEXT).pack(anchor="w")
tk.Entry(frame_login, textvariable=login_user).pack(fill="x", pady=5)

tk.Label(frame_login, text="Password", bg=CARD, fg=TEXT).pack(anchor="w")
tk.Entry(frame_login, textvariable=login_pass, show="*").pack(fill="x", pady=5)

def check_login():
    if login_user.get() == "admin" and login_pass.get() == "1234":
        login_window.destroy()
        open_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

tk.Button(login_window, text="LOGIN",
          bg=ACCENT, fg="black",
          font=("Segoe UI", 10, "bold"),
          command=check_login).pack(pady=15, fill="x", padx=40)

# ================= MAIN APP =================
def open_main_app():
    root = tk.Tk()
    root.title("Trainer Management")
    root.geometry("360x640")
    root.configure(bg=BG)

    canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
    scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg=BG)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")

    canvas.configure(yscrollcommand=scroll_y.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    tk.Label(frame, text="Trainer Management",
             font=("Segoe UI", 16, "bold"),
             bg=BG, fg=ACCENT).pack(pady=10)

    # ================= FORM =================
    form = tk.Frame(frame, bg=CARD, padx=15, pady=15)
    form.pack(fill="x", padx=10, pady=5)

    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    spec_var = tk.StringVar()
    exp_var = tk.StringVar()
    salary_var = tk.StringVar()
    selected_id = tk.StringVar()

    def validate_phone(P):
        return (P.isdigit() and len(P) <= 10) or P == ""

    def validate_salary(P):
        return P.isdigit() or P == ""

    vcmd_phone = (root.register(validate_phone), "%P")
    vcmd_salary = (root.register(validate_salary), "%P")

    def input_field(label, var):
        tk.Label(form, text=label, bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Entry(form, textvariable=var).pack(fill="x", pady=4)

    input_field("Name", name_var)

    tk.Label(form, text="Phone", bg=CARD, fg=TEXT).pack(anchor="w")
    tk.Entry(form, textvariable=phone_var, validate="key", validatecommand=vcmd_phone).pack(fill="x", pady=4)

    tk.Label(form, text="Specialization", bg=CARD, fg=TEXT).pack(anchor="w")
    ttk.Combobox(form, textvariable=spec_var,
                 values=["Weight Loss","Muscle Gain","Cardio","Yoga","Personal"],
                 state="readonly").pack(fill="x", pady=4)

    tk.Label(form, text="Experience", bg=CARD, fg=TEXT).pack(anchor="w")
    ttk.Combobox(form, textvariable=exp_var,
                 values=[str(i) for i in range(1,11)],
                 state="readonly").pack(fill="x", pady=4)

    tk.Label(form, text="Salary", bg=CARD, fg=TEXT).pack(anchor="w")
    tk.Entry(form, textvariable=salary_var, validate="key", validatecommand=vcmd_salary).pack(fill="x", pady=4)

    # ================= FUNCTIONS =================
    def clear():
        selected_id.set("")
        name_var.set("")
        phone_var.set("")
        spec_var.set("")
        exp_var.set("")
        salary_var.set("")

    def add():
        conn = connect_db()
        conn.execute("INSERT INTO trainers (name,phone,specialization,experience,salary) VALUES (?,?,?,?,?)",
                     (name_var.get(), phone_var.get(), spec_var.get(), exp_var.get(), salary_var.get()))
        conn.commit()
        conn.close()
        show()
        clear()

    def update():
        if selected_id.get() == "":
            return
        conn = connect_db()
        conn.execute("""UPDATE trainers SET name=?,phone=?,specialization=?,experience=?,salary=? WHERE id=?""",
                     (name_var.get(), phone_var.get(), spec_var.get(), exp_var.get(), salary_var.get(), selected_id.get()))
        conn.commit()
        conn.close()
        show()
        clear()

    def delete():
        if selected_id.get() == "":
            return
        conn = connect_db()
        conn.execute("DELETE FROM trainers WHERE id=?", (selected_id.get(),))
        conn.commit()
        conn.close()
        show()
        clear()

    tk.Button(form, text="Add Trainer", bg=GREEN, fg="white", command=add).pack(fill="x", pady=4)
    tk.Button(form, text="Update Trainer", bg=YELLOW, command=update).pack(fill="x", pady=4)
    tk.Button(form, text="Delete Trainer", bg=RED, fg="white", command=delete).pack(fill="x", pady=4)

    # ================= ATTENDANCE =================
    att_frame = tk.Frame(frame, bg=CARD, padx=15, pady=10)
    att_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(att_frame, text="Mark Attendance",
             bg=CARD, fg=ACCENT, font=("Segoe UI", 12, "bold")).pack()

    def mark_attendance(status):
        if selected_id.get() == "":
            messagebox.showwarning("Select Trainer", "Please select trainer from table")
            return

        today = datetime.date.today().strftime("%Y-%m-%d")

        conn = connect_db()
        conn.execute("INSERT INTO attendance (trainer_id, date, status) VALUES (?,?,?)",
                     (selected_id.get(), today, status))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Attendance Marked {status}")

    btn_frame = tk.Frame(att_frame, bg=CARD)
    btn_frame.pack(fill="x", pady=5)

    tk.Button(btn_frame, text="Present", bg=GREEN, fg="white",
              command=lambda: mark_attendance("Present")).pack(side="left", expand=True, fill="x", padx=5)

    tk.Button(btn_frame, text="Absent", bg=RED, fg="white",
              command=lambda: mark_attendance("Absent")).pack(side="left", expand=True, fill="x", padx=5)

    # ================= REPORT WINDOW =================
    def open_attendance_report():
        report_win = tk.Toplevel(root)
        report_win.title("Attendance Report")
        report_win.geometry("420x500")
        report_win.configure(bg=BG)

        tk.Label(report_win, text="Attendance Report",
                 font=("Segoe UI", 14, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=10)

        table_frame = tk.Frame(report_win, bg=CARD)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("Trainer", "Date", "Status")
        tree_rep = ttk.Treeview(table_frame, columns=cols, show="headings")

        for c in cols:
            tree_rep.heading(c, text=c)
            tree_rep.column(c, width=120)

        tree_rep.pack(fill="both", expand=True)

        conn = connect_db()
        query = """
        SELECT trainers.name, attendance.date, attendance.status
        FROM attendance
        JOIN trainers ON trainers.id = attendance.trainer_id
        ORDER BY attendance.date DESC
        """
        for row in conn.execute(query):
            tree_rep.insert("", tk.END, values=row)
        conn.close()

    tk.Button(frame, text="View Attendance Report",
              bg=ACCENT, fg="black",
              font=("Segoe UI", 10, "bold"),
              command=open_attendance_report).pack(fill="x", padx=10, pady=5)

    # ================= TABLE =================
    table_frame = tk.Frame(frame, bg=CARD)
    table_frame.pack(fill="both", expand=True, padx=10, pady=5)

    columns = ("ID","Name","Phone","Spec","Exp","Salary")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=90)

    tree.pack(fill="both", expand=True)

    def show():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        for row in conn.execute("SELECT * FROM trainers"):
            tree.insert("", tk.END, values=row)
        conn.close()

    def select(event):
        item = tree.focus()
        values = tree.item(item, "values")
        if values:
            selected_id.set(values[0])
            name_var.set(values[1])
            phone_var.set(values[2])
            spec_var.set(values[3])
            exp_var.set(values[4])
            salary_var.set(values[5])

    tree.bind("<ButtonRelease-1>", select)

    show()
    root.mainloop()

# ================= START =================
login_window.mainloop()