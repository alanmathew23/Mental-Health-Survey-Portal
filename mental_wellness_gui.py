# mental_wellness_gui.py - RECTANGULAR LOGIN BUTTONS VERSION
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime, time
import mysql.connector
from mysql.connector import Error
import threading

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'alan@20820',
    'database': 'MentalWellness'
}

# Color Scheme
COLORS = {
    'bg': '#fff8e7',             # cream background
    'sidebar': '#1a1f71',        # navy blue sidebar
    'accent_primary': "#50538D", # navy blue highlights/titles
    'accent_secondary': "#3b3f8e", # lighter navy for hover/highlight
    'button_normal': '#e6dfc5',  # light beige buttons
    'button_hover': '#d8cfa8',   # slightly darker beige on hover
    'text_primary': "#9a9ee9",   # navy text
    'text_secondary': "#565aa6", # lighter navy text
    'error': "#A50E0E",           # red for errors
    'success': "#257833",         # green for success messages
    'border': '#c0b9a0',          # beige border for frames/tables
    'table_bg': '#fef9ef',        # cream table background
    'table_alternate': '#f5f0e1'  # slightly darker cream alternate rows
}

MOODS = ["Stressed", "Anxious", "Confused", "Tired", "Optimistic", "Reflective", "Calm"]
DEPARTMENTS = ["CSE", "ECE", "ME", "EEE", "Civil"]
RESOURCE_TYPES = ["Article", "Video", "Podcast", "Guide"]

class DatabaseManager:
    @staticmethod
    def get_connection():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except Error as e:
            messagebox.showerror("Database Error", f"Connection failed: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None):
        conn = DatabaseManager.get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Query Error", str(e))
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def fetch_data(query, params=None):
        conn = DatabaseManager.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            data = cursor.fetchall()
            return data
        except Error as e:
            messagebox.showerror("Query Error", str(e))
            return []
        finally:
            cursor.close()
            conn.close()

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Mental Wellness - Login")
        self.geometry("600x600")
        self.configure(bg=COLORS['bg'])
        self.resizable(False, False)
        
        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_login_ui()

    def create_login_ui(self):
        main_frame = tk.Frame(self, bg=COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        tk.Label(main_frame, text="Mental Wellness", bg=COLORS['bg'], fg=COLORS['accent_primary'], font=("Segoe UI", 28, "bold")).pack(pady=(0, 10))
        tk.Label(main_frame, text="Management System", bg=COLORS['bg'], fg=COLORS['text_secondary'], font=("Segoe UI", 14)).pack(pady=(0, 30))
        
        # Role selection
        role_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        role_frame.pack(fill=tk.X, pady=20)
        tk.Label(role_frame, text="Login As:", bg=COLORS['bg'], fg=COLORS['text_primary'], font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)
        self.role_var = tk.StringVar(value="student")
        tk.Radiobutton(role_frame, text="Student", variable=self.role_var, value="student",
                       bg=COLORS['bg'], fg=COLORS['text_primary'], selectcolor=COLORS['sidebar'],
                       activebackground=COLORS['bg'], activeforeground=COLORS['accent_primary'],
                       font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=20)
        tk.Radiobutton(role_frame, text="Counselor", variable=self.role_var, value="counselor",
                       bg=COLORS['bg'], fg=COLORS['text_primary'], selectcolor=COLORS['sidebar'],
                       activebackground=COLORS['bg'], activeforeground=COLORS['accent_primary'],
                       font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=20)
        
        # Email input
        tk.Label(main_frame, text="Email/ID:", bg=COLORS['bg'], fg=COLORS['text_primary'], font=("Segoe UI", 11)).pack(anchor=tk.W, pady=(20,5))
        self.email_entry = tk.Entry(main_frame, bg=COLORS['table_bg'], fg=COLORS['text_primary'], insertbackground=COLORS['accent_primary'], font=("Segoe UI", 11), relief=tk.FLAT, bd=0)
        self.email_entry.pack(fill=tk.X, pady=(0,20), ipady=8)
        
        # Rectangular Buttons
        button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Login", bg=COLORS['accent_primary'], fg=COLORS['bg'], font=("Segoe UI", 12, "bold"),
                  command=self.login, width=20, height=2).pack(pady=5)
        tk.Button(button_frame, text="Demo Student", bg=COLORS['button_normal'], fg=COLORS['text_primary'], font=("Segoe UI", 12),
                  command=self.demo_login_student, width=20, height=2).pack(pady=5)
        tk.Button(button_frame, text="Demo Counselor", bg=COLORS['button_normal'], fg=COLORS['text_primary'], font=("Segoe UI", 12),
                  command=self.demo_login_counselor, width=20, height=2).pack(pady=5)
        
        # Info text
        tk.Label(main_frame, text="Sample IDs:\nStudent: 1, 2, 3, 4, 5\nCounselor: 1, 2, 3, 4, 5",
                 bg=COLORS['bg'], fg=COLORS['text_secondary'], font=("Segoe UI", 9), justify=tk.CENTER).pack(pady=(30,0))

    # --- login methods ---
    def login(self):
        email = self.email_entry.get().strip()
        role = self.role_var.get()
        
        if not email:
            messagebox.showerror("Error", "Please enter Email/ID")
            return
        
        if role == "student":
            try:
                student_id = int(email)
                result = DatabaseManager.fetch_data("SELECT * FROM Student WHERE StudentID = %s", (student_id,))
            except ValueError:
                result = DatabaseManager.fetch_data("SELECT * FROM Student WHERE Email = %s", (email,))
            if result:
                student = result[0]
                self.destroy()
                app = StudentApp(student)
                app.mainloop()
            else:
                messagebox.showerror("Error", "Student not found")
        else:
            try:
                counselor_id = int(email)
                result = DatabaseManager.fetch_data("SELECT * FROM Counselor WHERE CounselorID = %s", (counselor_id,))
            except ValueError:
                result = DatabaseManager.fetch_data("SELECT * FROM Counselor WHERE Email = %s", (email,))
            if result:
                counselor = result[0]
                self.destroy()
                app = CounselorApp(counselor)
                app.mainloop()
            else:
                messagebox.showerror("Error", "Counselor not found")
    
    def demo_login_student(self):
        self.role_var.set("student")
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, "1")
        self.login()
    
    def demo_login_counselor(self):
        self.role_var.set("counselor")
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, "1")
        self.login()

# --- Placeholder StudentApp & CounselorApp classes ---
class StudentApp(tk.Tk):
    def __init__(self, student):
        super().__init__()
        self.title(f"Student Dashboard - {student['StudentID']}")
        self.geometry("600x400")
        tk.Label(self, text=f"Welcome, {student.get('Name', 'Student')}", font=("Segoe UI", 16)).pack(pady=20)

class CounselorApp(tk.Tk):
    def __init__(self, counselor):
        super().__init__()
        self.title(f"Counselor Dashboard - {counselor['CounselorID']}")
        self.geometry("600x400")
        tk.Label(self, text=f"Welcome, {counselor.get('Name', 'Counselor')}", font=("Segoe UI", 16)).pack(pady=20)

if __name__ == "__main__":
    login_app = LoginPage()
    login_app.mainloop()
