import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os

class LogsPage:
    def __init__(self, root, parent_frame, controller=None):
        self.root = root
        self.parent_frame = parent_frame
        self.controller = controller
        self.scan_data = []
        self.filtered_data = []
        self.create_logs_ui()

    def clear_frame(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def create_logs_ui(self):
        self.clear_frame()

        self.logs_frame = tk.Frame(self.parent_frame, bg="#0D1117")
        self.logs_frame.pack(fill="both", expand=True)

        # Top bar with logo and title
        top_frame = tk.Frame(self.logs_frame, bg="#161B22", height=70)
        top_frame.pack(fill="x")

        logo_img = Image.open("C:/Coding/CyberGuard-Scanner/cyberguard_logo.png")
        logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        tk.Label(top_frame, image=self.logo_photo, bg="#161B22").pack(side="left", padx=10)

        tk.Label(top_frame, text="CYBERGUARD LOGS", fg="#58A6FF", bg="#161B22",
                 font=('Segoe UI Black', 20)).pack(side="left")

        # Title and Search bar
        title_frame = tk.Frame(self.logs_frame, bg="#0D1117")
        title_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(title_frame, text="📁 Scan Logs", font=("Segoe UI", 20, "bold"),
                 fg="#58A6FF", bg="#0D1117").pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_logs())

        search_entry = tk.Entry(title_frame, textvariable=self.search_var, width=40,
                                font=("Segoe UI", 11), bg="#161B22", fg="white",
                                insertbackground='white', relief="flat")
        search_entry.pack(side="right", padx=10)

        # Table area
        table_frame = tk.Frame(self.logs_frame, bg="#0D1117")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0D1117", foreground="white",
                        fieldbackground="#0D1117", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#161B22", foreground="#58A6FF",
                        font=("Segoe UI", 10, "bold"))
        style.map('Treeview', background=[('selected', '#58A6FF')], foreground=[('selected', 'black')])

        self.tree = ttk.Treeview(table_frame, columns=("URL", "Timestamp", "Vulnerabilities"), show="headings")
        self.tree.heading("URL", text="URL")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Vulnerabilities", text="Vulnerabilities Found")
        self.tree.column("URL", width=320)
        self.tree.column("Timestamp", width=180)
        self.tree.column("Vulnerabilities", width=180)
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.view_full_log)

        # Action buttons
        button_frame = tk.Frame(self.logs_frame, bg="#0D1117")
        button_frame.pack(pady=10)

        button_style = {"font": ("Segoe UI", 10, "bold"), "bg": "#161B22", "fg": "#58A6FF",
                        "activebackground": "#21262D", "activeforeground": "#58A6FF", "relief": "flat"}

        tk.Button(button_frame, text="View Selected", command=self.view_full_log, **button_style).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_selected, **button_style).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Clear All Logs", command=self.clear_all_logs, **button_style).grid(row=0, column=2, padx=10)

        # Home button at bottom
        bottom_frame = tk.Frame(self.logs_frame, bg="#0D1117")
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        if self.controller:
            tk.Button(bottom_frame, text="🏠 Home", command=lambda: self.controller.show_frame("home"), **button_style).pack()

        self.load_logs()

    def load_logs(self):
        file_path = "scan_history.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.scan_data = json.load(f)
                self.filtered_data = self.scan_data.copy()
                self.refresh_table()
        else:
            self.scan_data = []
            self.filtered_data = []
            self.tree.insert("", tk.END, values=("No logs found", "", ""))

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for entry in self.filtered_data:
            url = entry["url"]
            timestamp = entry["timestamp"]
            vuln_count = sum(1 for r in entry["results"] if "Vulnerable" in r["status"])
            self.tree.insert("", tk.END, values=(url, timestamp, vuln_count))

    def filter_logs(self):
        search = self.search_var.get().lower()
        if not search:
            self.filtered_data = self.scan_data.copy()
        else:
            self.filtered_data = [entry for entry in self.scan_data if search in entry["url"].lower()]
        self.refresh_table()

    def view_full_log(self, event=None):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a log entry.")
            return
        index = self.tree.index(selected)
        if index >= len(self.filtered_data):
            return
        entry = self.filtered_data[index]
        log_window = tk.Toplevel(self.root)
        log_window.title("Full Scan Log")
        log_window.geometry("700x500")
        log_window.configure(bg="#0D1117")
        text_area = tk.Text(log_window, wrap="word", bg="#161B22", fg="white", font=("Courier", 10),
                            insertbackground='white')
        text_area.insert("1.0", json.dumps(entry, indent=4))
        text_area.pack(fill="both", expand=True, padx=10, pady=10)

    def delete_selected(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a log entry.")
            return
        index = self.tree.index(selected)
        if index >= len(self.filtered_data):
            return
        log_to_delete = self.filtered_data[index]
        self.scan_data.remove(log_to_delete)
        self.filtered_data.remove(log_to_delete)
        self.save_logs()
        self.refresh_table()
        messagebox.showinfo("Deleted", "Selected log entry has been deleted.")

    def clear_all_logs(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to delete all logs?"):
            self.scan_data = []
            self.filtered_data = []
            self.save_logs()
            self.refresh_table()
            messagebox.showinfo("Cleared", "All log entries have been deleted.")

    def save_logs(self):
        with open("scan_history.json", "w") as f:
            json.dump(self.scan_data, f, indent=4)
