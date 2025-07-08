import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import start_scan
import dashboard
import view_report
import logs
import settings
from utils import load_theme  # Import theme loader

class CyberGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberGuard - Web Security Scanner")
        self.root.geometry("1000x650")
        self.root.configure(bg="#0D1117")

        self.theme = load_theme()  # Load current theme
        self.bg_color = self.theme["bg"]
        self.fg_color = self.theme["fg"]
        self.accent_color = self.theme["accent"]
        self.button_bg = self.theme["button_bg"]
        self.font_color = self.theme["font_color"]

        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Button style configuration
        self.style.configure('TButton', 
                             font=('Segoe UI', 11, 'bold'),
                             foreground='white',
                             background=self.button_bg,
                             borderwidth=1,
                             focuscolor=self.button_bg)
        
        # Define button hover effect
        self.style.map('TButton', 
                       background=[('active', self.accent_color)])

        self.style.configure('TLabel', background=self.bg_color, foreground=self.font_color, font=('Segoe UI', 12))

        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill="both", expand=True)

        self.create_topbar()
        self.show_frame("home")  # Start from home

        self.update_clock()  # Start clock

    def create_topbar(self):
        topbar = tk.Frame(self.root, bg="#161B22", height=80)
        topbar.pack(side="top", fill="x")

        # Logo
        logo_img = Image.open("C:/Coding/CyberGuard-Scanner/cyberguard_logo.png")  # Your existing logo path
        logo_img = logo_img.resize((60, 60), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        tk.Label(topbar, image=self.logo_photo, bg="#161B22").pack(side="left", padx=10)

        # Tool Name
        tk.Label(topbar, text="CYBERGUARD", fg=self.accent_color, bg="#161B22", font=('Segoe UI Black', 22)).pack(side="left", padx=10)

        # Real-time Clock
        self.time_label = tk.Label(topbar, text="", bg="#161B22", fg="#A5D6FF", font=('Consolas', 12))
        self.time_label.pack(side="right", padx=20)

    def update_clock(self):
        now = datetime.now().strftime("%A, %d %B %Y | %H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def show_frame(self, page_name):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if page_name == "home":
            frame = self.create_home()
        elif page_name == "scan":
            frame = start_scan.ScanPage(self.root, self.main_frame, self)
        elif page_name == "dashboard":
            frame = dashboard.DashboardPage(self.root, self.main_frame, self)
        elif page_name == "report":
            frame = view_report.ReportPage(self.root, self.main_frame, self)
        elif page_name == "logs":
            frame = logs.LogsPage(self.root, self.main_frame, self)
        elif page_name == "settings":
            frame = settings.SettingsPage(self.root, self.main_frame, self)

        frame.pack(fill="both", expand=True)

    def create_home(self):
        home_frame = tk.Frame(self.main_frame, bg=self.bg_color, padx=30, pady=20)
        home_frame.pack(fill="both", expand=True)

        # Welcome Heading
        tk.Label(home_frame, text="Welcome to CyberGuard", font=("Segoe UI", 24, "bold"),
                 fg=self.accent_color, bg=self.bg_color).pack(pady=10)

        # Tool Description
        tk.Label(
            home_frame,
            text="CyberGuard is an advanced web vulnerability scanner designed to detect, analyze,\nand report potential threats in web applications.",
            font=("Segoe UI", 13),
            fg=self.font_color,
            bg=self.bg_color,
            justify="center"
        ).pack(pady=10)

        # Navigation Buttons
        tab_frame = tk.Frame(home_frame, bg=self.bg_color)
        tab_frame.pack(pady=30)

        tabs = [
            ("Start Scan", lambda: self.show_frame("scan")),
            ("Dashboard", lambda: self.show_frame("dashboard")),
            ("View Reports", lambda: self.show_frame("report")),
            ("Logs", lambda: self.show_frame("logs")),
            ("Settings", lambda: self.show_frame("settings"))
        ]

        for text, command in tabs:
            ttk.Button(tab_frame, text=text, command=command, width=20).pack(pady=5)

        return home_frame

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberGuardApp(root)
    root.mainloop()
