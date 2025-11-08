# mental_wellness_gui.py - FIXED LOGIN WITH VISIBLE DEMO BUTTON
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
    'password': 'kichu@2311',  # Change this to your MySQL password
    'database': 'MentalWellness'
}

# Color Scheme
COLORS = {
    'bg': '#1e1e1e',
    'sidebar': '#2d2d2d',
    'accent_primary': '#00d4ff',
    'accent_secondary': '#00bfff',
    'button_normal': '#444444',
    'button_hover': '#555555',
    'text_primary': '#e0e0e0',
    'text_secondary': '#b0b0b0',
    'error': '#ff6b6b',
    'success': '#51cf66',
    'border': '#3a3a3a',
    'table_bg': '#252525',
    'table_alternate': '#2a2a2a'
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
        self.geometry("600x600")  # Larger window
        self.configure(bg=COLORS['bg'])
        self.resizable(False, False)
        
        # Center window on screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_login_ui()
    
    def create_login_ui(self):
        # Main frame with scrolling capability
        main_frame = tk.Frame(self, bg=COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        title = tk.Label(
            main_frame,
            text="Mental Wellness",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=(0, 10))
        
        subtitle = tk.Label(
            main_frame,
            text="Management System",
            bg=COLORS['bg'],
            fg=COLORS['text_secondary'],
            font=("Segoe UI", 14)
        )
        subtitle.pack(pady=(0, 30))
        
        # Role selection
        role_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        role_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            role_frame,
            text="Login As:",
            bg=COLORS['bg'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 12, "bold")
        ).pack(side=tk.LEFT)
        
        self.role_var = tk.StringVar(value="student")
        
        student_radio = tk.Radiobutton(
            role_frame,
            text="Student",
            variable=self.role_var,
            value="student",
            bg=COLORS['bg'],
            fg=COLORS['text_primary'],
            selectcolor=COLORS['sidebar'],
            activebackground=COLORS['bg'],
            activeforeground=COLORS['accent_primary'],
            font=("Segoe UI", 10)
        )
        student_radio.pack(side=tk.LEFT, padx=20)
        
        counselor_radio = tk.Radiobutton(
            role_frame,
            text="Counselor",
            variable=self.role_var,
            value="counselor",
            bg=COLORS['bg'],
            fg=COLORS['text_primary'],
            selectcolor=COLORS['sidebar'],
            activebackground=COLORS['bg'],
            activeforeground=COLORS['accent_primary'],
            font=("Segoe UI", 10)
        )
        counselor_radio.pack(side=tk.LEFT, padx=20)
        
        # Email/ID input
        tk.Label(
            main_frame,
            text="Email/ID:",
            bg=COLORS['bg'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 11)
        ).pack(anchor=tk.W, pady=(20, 5))
        
        self.email_entry = tk.Entry(
            main_frame,
            bg=COLORS['table_bg'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['accent_primary'],
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            bd=0
        )
        self.email_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # Login button
        login_btn = tk.Button(
            main_frame,
            text="Login",
            bg=COLORS['accent_primary'],
            fg=COLORS['bg'],
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            command=self.login,
            cursor="hand2"
        )
        login_btn.pack(fill=tk.X, pady=10, ipady=10)
        
        # Demo button - STUDENT
        demo_student_btn = tk.Button(
            main_frame,
            text="Demo Login (Student)",
            bg=COLORS['button_normal'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            command=self.demo_login_student,
            cursor="hand2"
        )
        demo_student_btn.pack(fill=tk.X, pady=5, ipady=8)
        demo_student_btn.bind("<Enter>", lambda e: demo_student_btn.config(bg=COLORS['button_hover']))
        demo_student_btn.bind("<Leave>", lambda e: demo_student_btn.config(bg=COLORS['button_normal']))
        
        # Demo button - COUNSELOR
        demo_counselor_btn = tk.Button(
            main_frame,
            text="Demo Login (Counselor)",
            bg=COLORS['button_normal'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            command=self.demo_login_counselor,
            cursor="hand2"
        )
        demo_counselor_btn.pack(fill=tk.X, pady=5, ipady=8)
        demo_counselor_btn.bind("<Enter>", lambda e: demo_counselor_btn.config(bg=COLORS['button_hover']))
        demo_counselor_btn.bind("<Leave>", lambda e: demo_counselor_btn.config(bg=COLORS['button_normal']))
        
        # Info text
        info = tk.Label(
            main_frame,
            text="Sample IDs:\nStudent: 1, 2, 3, 4, 5\nCounselor: 1, 2, 3, 4, 5",
            bg=COLORS['bg'],
            fg=COLORS['text_secondary'],
            font=("Segoe UI", 9),
            justify=tk.CENTER
        )
        info.pack(pady=(30, 0))
    
    def login(self):
        email = self.email_entry.get().strip()
        role = self.role_var.get()
        
        if not email:
            messagebox.showerror("Error", "Please enter Email/ID")
            return
        
        if role == "student":
            # Try to parse as integer first, then as string
            try:
                student_id = int(email)
                query = "SELECT * FROM Student WHERE StudentID = %s"
                result = DatabaseManager.fetch_data(query, (student_id,))
            except ValueError:
                query = "SELECT * FROM Student WHERE Email = %s"
                result = DatabaseManager.fetch_data(query, (email,))
            
            if result:
                student = result[0]
                self.destroy()
                app = StudentApp(student)
                app.mainloop()
            else:
                messagebox.showerror("Error", "Student not found")
        
        else:  # counselor
            try:
                counselor_id = int(email)
                query = "SELECT * FROM Counselor WHERE CounselorID = %s"
                result = DatabaseManager.fetch_data(query, (counselor_id,))
            except ValueError:
                query = "SELECT * FROM Counselor WHERE Email = %s"
                result = DatabaseManager.fetch_data(query, (email,))
            
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

class StudentApp(tk.Tk):
    def __init__(self, student):
        super().__init__()
        
        self.student = student
        self.title(f"Mental Wellness - Student ({student['Name']})")
        self.geometry("1400x800")
        self.configure(bg=COLORS['bg'])
        
        self.create_ui()
        self.show_dashboard()
    
    def create_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=COLORS['sidebar'], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            self.sidebar,
            text=f"Welcome\n{self.student['Name']}",
            bg=COLORS['sidebar'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 11, "bold"),
            pady=20,
            wraplength=180
        )
        title_label.pack()
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Book Session", self.show_book_session),
            ("View Counselors", self.show_counselors),
            ("Resources", self.show_resources),
            ("My Sessions", self.show_my_sessions),
            ("Logout", self.logout),
        ]
        
        for btn_text, cmd in nav_buttons:
            btn = tk.Button(
                self.sidebar,
                text=btn_text,
                bg=COLORS['button_normal'],
                fg=COLORS['text_primary'],
                font=("Segoe UI", 10),
                relief=tk.FLAT,
                padx=15,
                pady=10,
                command=cmd,
                activebackground=COLORS['accent_primary'],
                activeforeground=COLORS['bg']
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS['button_normal']))
        
        # Main content area
        self.main_frame = tk.Frame(self, bg=COLORS['bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="Dashboard",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=20)
        
        # Student info
        info_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = f"""
        Name: {self.student['Name']}
        Email: {self.student['Email']}
        Department: {self.student['Department']}
        Year: {self.student['YearOfStudy']}
        """
        
        tk.Label(
            info_frame,
            text=info_text,
            bg=COLORS['table_bg'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 11),
            justify=tk.LEFT,
            padx=20,
            pady=20
        ).pack(anchor=tk.W)
        
        # Quick stats
        sessions = DatabaseManager.fetch_data(
            "SELECT COUNT(*) as count FROM Session WHERE StudentID = %s",
            (self.student['StudentID'],)
        )
        
        stress_level = DatabaseManager.fetch_data(
            "SELECT StressLevel FROM WellnessSurvey WHERE StudentID = %s ORDER BY SubmissionDate DESC LIMIT 1",
            (self.student['StudentID'],)
        )
        
        stats_frame = tk.Frame(self.main_frame, bg=COLORS['bg'])
        stats_frame.pack(fill=tk.X, pady=20)
        
        stats = [
            ("Your Sessions", sessions[0]['count'] if sessions else 0),
            ("Current Stress Level", f"{stress_level[0]['StressLevel']}/10" if stress_level else "No data"),
        ]
        
        for stat_name, stat_value in stats:
            stat_card = tk.Frame(stats_frame, bg=COLORS['table_bg'], height=80, width=250)
            stat_card.pack(side=tk.LEFT, padx=15, pady=10, fill=tk.BOTH, expand=True)
            
            tk.Label(
                stat_card,
                text=stat_name,
                bg=COLORS['table_bg'],
                fg=COLORS['text_secondary'],
                font=("Segoe UI", 10)
            ).pack(pady=5)
            
            tk.Label(
                stat_card,
                text=str(stat_value),
                bg=COLORS['table_bg'],
                fg=COLORS['accent_primary'],
                font=("Segoe UI", 18, "bold")
            ).pack(pady=5)
    
    def show_book_session(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="Book a Counseling Session",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)
        
        # Form frame
        self.form_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Session ID
        tk.Label(self.form_frame, text="Session ID:", bg=COLORS['table_bg'], fg=COLORS['text_primary']).pack(anchor=tk.W, padx=20, pady=(20, 5))
        self.session_id_entry = tk.Entry(self.form_frame, bg=COLORS['bg'], fg=COLORS['text_primary'], insertbackground=COLORS['accent_primary'])
        self.session_id_entry.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Counselor selection
        tk.Label(self.form_frame, text="Select Counselor:", bg=COLORS['table_bg'], fg=COLORS['text_primary']).pack(anchor=tk.W, padx=20, pady=(20, 5))
        self.counselor_var = tk.StringVar()
        counselors = DatabaseManager.fetch_data("SELECT CounselorID, Name, Specialization FROM Counselor")
        counselor_values = [f"{c['CounselorID']} - {c['Name']} ({c['Specialization']})" for c in counselors]
        counselor_combo = ttk.Combobox(self.form_frame, textvariable=self.counselor_var, values=counselor_values, state="readonly")
        counselor_combo.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Date selection
        tk.Label(self.form_frame, text="Session Date:", bg=COLORS['table_bg'], fg=COLORS['text_primary']).pack(anchor=tk.W, padx=20, pady=(20, 5))
        self.date_entry = DateEntry(self.form_frame, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Start time
        tk.Label(self.form_frame, text="Start Time (HH:MM:SS):", bg=COLORS['table_bg'], fg=COLORS['text_primary']).pack(anchor=tk.W, padx=20, pady=(20, 5))
        self.start_time = tk.Entry(self.form_frame, bg=COLORS['bg'], fg=COLORS['text_primary'], insertbackground=COLORS['accent_primary'])
        self.start_time.insert(0, "09:00:00")
        self.start_time.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # End time
        tk.Label(self.form_frame, text="End Time (HH:MM:SS):", bg=COLORS['table_bg'], fg=COLORS['text_primary']).pack(anchor=tk.W, padx=20, pady=(20, 5))
        self.end_time = tk.Entry(self.form_frame, bg=COLORS['bg'], fg=COLORS['text_primary'], insertbackground=COLORS['accent_primary'])
        self.end_time.insert(0, "10:00:00")
        self.end_time.pack(fill=tk.X, padx=20, pady=(0, 15))

        # Book button
        tk.Button(
            self.form_frame,
            text="Book Session",
            bg=COLORS['accent_primary'],
            fg=COLORS['bg'],
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            command=self.book
        ).pack(pady=30, ipady=10, fill=tk.X, padx=20)

    def book(self):
        try:
            if not all([self.session_id_entry.get(), self.counselor_var.get()]):
                messagebox.showerror("Error", "All fields required")
                return
            
            counselor_id = int(self.counselor_var.get().split()[0])
            session_id = int(self.session_id_entry.get())
            session_date = self.date_entry.get_date()
            start = self.start_time.get()
            end = self.end_time.get()
            
            query = """
                INSERT INTO Session (SessionID, StudentID, CounselorID, SessionDate, StartTime, EndTime, Notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                session_id,
                self.student['StudentID'],
                counselor_id,
                session_date,
                start,
                end,
                "Session booked by student"
            )
            
            if DatabaseManager.execute_query(query, params):
                messagebox.showinfo("Success", "Session booked successfully!")
                self.show_my_sessions()
            else:
                messagebox.showerror("Error", "Failed to book session")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def show_counselors(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="Available Counselors",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)
        
        # Table
        tree_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Name", "Email", "Specialization")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        widths = [50, 150, 200, 200]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)
        
        counselors = DatabaseManager.fetch_data("SELECT * FROM Counselor")
        for c in counselors:
            tree.insert("", tk.END, values=(c['CounselorID'], c['Name'], c['Email'], c['Specialization']))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_resources(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="Mental Health Resources",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)
        
        # Table
        tree_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Title", "Type", "URL")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        widths = [50, 250, 100, 300]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)
        
        resources = DatabaseManager.fetch_data("SELECT * FROM MentalHealthResource")
        for r in resources:
            tree.insert("", tk.END, values=(r['ResourceID'], r['Title'], r['ResourceType'], r['URL'] or 'N/A'))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_my_sessions(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="My Sessions",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)
        
        # Table
        tree_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("SessionID", "Counselor", "Date", "Start", "End", "Notes")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        widths = [80, 150, 100, 100, 100, 250]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)
        
        sessions = DatabaseManager.fetch_data("""
            SELECT s.SessionID, c.Name, s.SessionDate, s.StartTime, s.EndTime, s.Notes
            FROM Session s
            LEFT JOIN Counselor c ON s.CounselorID = c.CounselorID
            WHERE s.StudentID = %s
            ORDER BY s.SessionDate DESC
        """, (self.student['StudentID'],))
        
        for s in sessions:
            tree.insert("", tk.END, values=(
                s['SessionID'],
                s['Name'] or 'N/A',
                str(s['SessionDate']),
                str(s['StartTime']),
                str(s['EndTime']),
                s['Notes'] or 'N/A'
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def logout(self):
        self.destroy()
        login_app = LoginPage()
        login_app.mainloop()

class CounselorApp(tk.Tk):
    def __init__(self, counselor):
        super().__init__()
        
        self.counselor = counselor
        self.title(f"Mental Wellness - Counselor ({counselor['Name']})")
        self.geometry("1400x800")
        self.configure(bg=COLORS['bg'])
        
        self.create_ui()
        self.show_dashboard()
    
    def create_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=COLORS['sidebar'], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            self.sidebar,
            text=f"Welcome\n{self.counselor['Name']}",
            bg=COLORS['sidebar'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 11, "bold"),
            pady=20,
            wraplength=180
        )
        title_label.pack()
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Sessions", self.show_sessions),
            ("Wellness Surveys", self.show_surveys),
            ("Mental Health Logs", self.show_logs),
            ("Resources", self.show_resources),
            ("Logout", self.logout),
        ]
        
        for btn_text, cmd in nav_buttons:
            btn = tk.Button(
                self.sidebar,
                text=btn_text,
                bg=COLORS['button_normal'],
                fg=COLORS['text_primary'],
                font=("Segoe UI", 10),
                relief=tk.FLAT,
                padx=15,
                pady=10,
                command=cmd,
                activebackground=COLORS['accent_primary'],
                activeforeground=COLORS['bg']
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS['button_normal']))
        
        # Main content area
        self.main_frame = tk.Frame(self, bg=COLORS['bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="Dashboard",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=20)
        
        # Counselor info
        info_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = f"""
        Name: {self.counselor['Name']}
        Email: {self.counselor['Email']}
        Specialization: {self.counselor['Specialization']}
        """
        
        tk.Label(
            info_frame,
            text=info_text,
            bg=COLORS['table_bg'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 11),
            justify=tk.LEFT,
            padx=20,
            pady=20
        ).pack(anchor=tk.W)
        
        # Quick stats
        sessions = DatabaseManager.fetch_data(
            "SELECT COUNT(*) as count FROM Session WHERE CounselorID = %s",
            (self.counselor['CounselorID'],)
        )
        
        students = DatabaseManager.fetch_data(
            """SELECT COUNT(DISTINCT StudentID) as count FROM Session WHERE CounselorID = %s""",
            (self.counselor['CounselorID'],)
        )
        
        stats_frame = tk.Frame(self.main_frame, bg=COLORS['bg'])
        stats_frame.pack(fill=tk.X, pady=20)
        
        stats = [
            ("Total Sessions", sessions[0]['count'] if sessions else 0),
            ("Students Counseled", students[0]['count'] if students else 0),
        ]
        
        for stat_name, stat_value in stats:
            stat_card = tk.Frame(stats_frame, bg=COLORS['table_bg'], height=80, width=250)
            stat_card.pack(side=tk.LEFT, padx=15, pady=10, fill=tk.BOTH, expand=True)
            
            tk.Label(
                stat_card,
                text=stat_name,
                bg=COLORS['table_bg'],
                fg=COLORS['text_secondary'],
                font=("Segoe UI", 10)
            ).pack(pady=5)
            
            tk.Label(
                stat_card,
                text=str(stat_value),
                bg=COLORS['table_bg'],
                fg=COLORS['accent_primary'],
                font=("Segoe UI", 18, "bold")
            ).pack(pady=5)
    
    def show_sessions(self):
        self.clear_main_frame()
        
        header = tk.Frame(self.main_frame, bg=COLORS['bg'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header,
            text="My Sessions",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 18, "bold")
        ).pack(side=tk.LEFT)
        
        # Table
        tree_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("SessionID", "Student", "Date", "Start", "End", "Notes")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        widths = [80, 150, 100, 100, 100, 250]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)
        
        sessions = DatabaseManager.fetch_data("""
            SELECT s.SessionID, st.Name, s.SessionDate, s.StartTime, s.EndTime, s.Notes
            FROM Session s
            LEFT JOIN Student st ON s.StudentID = st.StudentID
            WHERE s.CounselorID = %s
            ORDER BY s.SessionDate DESC
        """, (self.counselor['CounselorID'],))
        
        for s in sessions:
            tree.insert("", tk.END, values=(
                s['SessionID'],
                s['Name'] or 'N/A',
                str(s['SessionDate']),
                str(s['StartTime']),
                str(s['EndTime']),
                s['Notes'] or 'N/A'
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_surveys(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="Wellness Surveys - All Students",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)
        
        # Table
        tree_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("SurveyID", "Student", "Date", "Stress Level", "Sleep Hours")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        widths = [80, 150, 120, 120, 120]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)
        
        surveys = DatabaseManager.fetch_data("""
            SELECT ws.SurveyID, s.Name, ws.SubmissionDate, ws.StressLevel, ws.SleepHours
            FROM WellnessSurvey ws
            LEFT JOIN Student s ON ws.StudentID = s.StudentID
            ORDER BY ws.SubmissionDate DESC
        """)
        
        for sur in surveys:
            tree.insert("", tk.END, values=(
                sur['SurveyID'],
                sur['Name'] or 'N/A',
                str(sur['SubmissionDate']),
                sur['StressLevel'],
                sur['SleepHours']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_logs(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="Mental Health Logs - All Students",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)
        
        # Table
        tree_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("LogID", "Student", "Date", "Mood", "Notes")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        widths = [80, 150, 120, 120, 300]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)
        
        logs = DatabaseManager.fetch_data("""
            SELECT mhl.LogID, s.Name, mhl.LogDate, mhl.Mood, mhl.Notes
            FROM MentalHealthLog mhl
            LEFT JOIN Student s ON mhl.StudentID = s.StudentID
            ORDER BY mhl.LogDate DESC
        """)
        
        for log in logs:
            tree.insert("", tk.END, values=(
                log['LogID'],
                log['Name'] or 'N/A',
                str(log['LogDate']),
                log['Mood'],
                log['Notes'] or 'N/A'
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_resources(self):
        self.clear_main_frame()
        
        title = tk.Label(
            self.main_frame,
            text="Mental Health Resources",
            bg=COLORS['bg'],
            fg=COLORS['accent_primary'],
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)
        
        # Table
        tree_frame = tk.Frame(self.main_frame, bg=COLORS['table_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Title", "Type", "URL")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        widths = [50, 250, 100, 300]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, anchor=tk.W)
            tree.heading(col, text=col)
        
        resources = DatabaseManager.fetch_data("SELECT * FROM MentalHealthResource")
        for r in resources:
            tree.insert("", tk.END, values=(r['ResourceID'], r['Title'], r['ResourceType'], r['URL'] or 'N/A'))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def logout(self):
        self.destroy()
        login_app = LoginPage()
        login_app.mainloop()

if __name__ == "__main__":
    login_app = LoginPage()
    login_app.mainloop()
