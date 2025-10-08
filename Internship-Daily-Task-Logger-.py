import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import date
import os

# -------------------- Database Setup --------------------
def init_db():
    conn = sqlite3.connect("intern_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            tags TEXT,
            time_spent REAL
        )
    """)
    conn.commit()
    conn.close()

# -------------------- Add Task --------------------
def add_task():
    task_date = date_entry.get()
    desc = desc_entry.get("1.0", tk.END).strip()
    tags = tags_entry.get()
    time_spent = time_entry.get()

    if not task_date or not desc or not time_spent:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        conn = sqlite3.connect("intern_logs.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (date, description, tags, time_spent) VALUES (?, ?, ?, ?)",
                       (task_date, desc, tags, time_spent))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Task added successfully!")
        clear_entries()
        view_logs()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# -------------------- View Logs --------------------
def view_logs():
    for row in log_table.get_children():
        log_table.delete(row)

    conn = sqlite3.connect("intern_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        log_table.insert("", tk.END, values=row)

# -------------------- Export to CSV --------------------
def export_csv():
    # Get Desktop path
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop, "intern_logs.csv")

    conn = sqlite3.connect("intern_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Description", "Tags", "Time Spent"])
        writer.writerows(rows)

    messagebox.showinfo("Exported", f"Logs exported to {file_path}")
# -------------------- Clear Form --------------------
def clear_entries():
    date_entry.delete(0, tk.END)
    desc_entry.delete("1.0", tk.END)
    tags_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    date_entry.insert(0, str(date.today()))

# -------------------- GUI Setup --------------------
root = tk.Tk()
root.title("Internship Daily Task Logger")
root.geometry("750x500")

# Input Frame
frame = tk.LabelFrame(root, text="Add New Task", padx=10, pady=10)
frame.pack(fill="x", padx=10, pady=5)

tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
date_entry = tk.Entry(frame, width=20)
date_entry.grid(row=0, column=1, padx=5, pady=5)
date_entry.insert(0, str(date.today()))

tk.Label(frame, text="Description:").grid(row=1, column=0, sticky="nw")
desc_entry = tk.Text(frame, width=40, height=3)
desc_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Tags (comma separated):").grid(row=2, column=0, sticky="w")
tags_entry = tk.Entry(frame, width=40)
tags_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Time Spent (hours):").grid(row=3, column=0, sticky="w")
time_entry = tk.Entry(frame, width=20)
time_entry.grid(row=3, column=1, padx=5, pady=5)

add_btn = tk.Button(frame, text="Add Task", command=add_task, bg="#4CAF50", fg="white")
add_btn.grid(row=4, column=0, columnspan=2, pady=10)

# Log Table
log_frame = tk.LabelFrame(root, text="Task Logs", padx=10, pady=10)
log_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("ID", "Date", "Description", "Tags", "Time Spent")
log_table = ttk.Treeview(log_frame, columns=columns, show="headings")
for col in columns:
    log_table.heading(col, text=col)
    log_table.column(col, width=100 if col != "Description" else 250)

log_table.pack(fill="both", expand=True)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

view_btn = tk.Button(btn_frame, text="View Logs", command=view_logs)
view_btn.grid(row=0, column=0, padx=5)

export_btn = tk.Button(btn_frame, text="Export to CSV", command=export_csv)
export_btn.grid(row=0, column=1, padx=5)

# Initialize DB and Run
init_db()
view_logs()
root.mainloop()
