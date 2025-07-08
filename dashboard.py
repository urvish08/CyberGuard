import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import os

class DashboardPage:
    def __init__(self, root, parent_frame, controller=None):
        self.root = root
        self.parent_frame = parent_frame
        self.controller = controller
        self.scan_data = []
        self.create_dashboard_ui()

    def clear_frame(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def create_dashboard_ui(self):
        self.clear_frame()

        self.dashboard_frame = tk.Frame(self.parent_frame, bg="#0D1117")
        self.dashboard_frame.pack(fill="both", expand=True)

        # Top Bar
        top_frame = tk.Frame(self.dashboard_frame, bg="#161B22", height=70)
        top_frame.pack(fill="x")
        logo_img = Image.open("C:/Coding/CyberGuard-Scanner/cyberguard_logo.png")
        logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        tk.Label(top_frame, image=self.logo_photo, bg="#161B22").pack(side="left", padx=10)
        tk.Label(top_frame, text="CYBERGUARD", fg="#58A6FF", bg="#161B22", font=('Segoe UI Black', 20)).pack(side="left")

        # Title
        tk.Label(self.dashboard_frame, text="📊 Vulnerability Dashboard", font=("Segoe UI", 20, "bold"),
                 fg="#58A6FF", bg="#0D1117").pack(pady=10)

        # URL List
        tk.Label(self.dashboard_frame, text="Select a Recent Scan:", font=("Segoe UI", 13, "bold"),
                 fg="#C9D1D9", bg="#0D1117").pack(pady=5)
        self.url_listbox = tk.Listbox(self.dashboard_frame, width=70, height=5, bg="#161B22",
                                      fg="white", font=("Segoe UI", 11))
        self.url_listbox.pack(pady=5)
        self.url_listbox.bind("<<ListboxSelect>>", self.load_selected_scan)

        # Chart + Summary Container
        self.content_frame = tk.Frame(self.dashboard_frame, bg="#0D1117")
        self.content_frame.pack(fill="both", expand=True)

        # Chart Area
        self.chart_frame = tk.Frame(self.content_frame, bg="#0D1117")
        self.chart_frame.pack(side="left", padx=10, pady=10, expand=True, fill="both")

        # Summary Box
        self.summary_box = tk.LabelFrame(self.content_frame, text="Scan Summary", font=("Segoe UI", 12, "bold"),
                                         bg="#161B22", fg="white", bd=2, relief="groove", labelanchor="n")
        self.summary_box.pack(side="right", padx=10, pady=10, fill="y")

        # Home Button (always visible at bottom)
        if self.controller:
            bottom_frame = tk.Frame(self.dashboard_frame, bg="#0D1117")
            bottom_frame.pack(fill="x", pady=5)
            ttk.Button(bottom_frame, text="🏠 Back to Home", command=lambda: self.controller.show_frame("home")).pack(pady=10)

        self.load_scan_history()

    def load_scan_history(self):
        file_path = "scan_history.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.scan_data = json.load(f)
            self.url_listbox.delete(0, tk.END)
            for entry in self.scan_data:
                self.url_listbox.insert(tk.END, f"{entry['url']}  —  {entry['timestamp']}")
        else:
            self.url_listbox.insert(tk.END, "No scan history found.")

    def load_selected_scan(self, event):
        selection = event.widget.curselection()
        if not selection:
            return
        index = selection[0]
        if index >= len(self.scan_data):
            return
        entry = self.scan_data[index]
        self.display_chart(entry)
        self.display_summary(entry)

    def display_chart(self, entry):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        labels = [item['name'] for item in entry['results']]
        values = [1 if "Vulnerable" in item['status'] else 0 for item in entry['results']]

        fig = Figure(figsize=(6, 4), dpi=100)

        # Bar Chart
        ax1 = fig.add_subplot(121)
        ax1.barh(labels, values, color=["#E55353" if x else "#2ECC71" for x in values])
        ax1.set_xlim(0, 1)
        ax1.set_title("Threat Status")
        ax1.set_xticks([0, 1])
        ax1.set_xticklabels(['Secure', 'Vulnerable'])
        ax1.set_facecolor("#0D1117")
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.title.set_color("white")

        # Pie Chart
        ax2 = fig.add_subplot(122)
        total = len(values)
        vuln = sum(values)
        secure = total - vuln
        ax2.pie([vuln, secure], labels=["Vulnerable", "Secure"], autopct='%1.1f%%',
                colors=["#E55353", "#2ECC71"], startangle=140)
        ax2.set_title("Vulnerability Distribution", color="white")
        fig.patch.set_facecolor('#0D1117')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def display_summary(self, entry):
        for widget in self.summary_box.winfo_children():
            widget.destroy()

        total = len(entry['results'])
        vulnerable = sum(1 for r in entry['results'] if "Vulnerable" in r['status'])
        secure = total - vulnerable

        summary_items = [
            ("URL", entry['url'], "#58A6FF"),
            ("Scanned At", entry['timestamp'], "#C9D1D9"),
            ("Total Tests Run", str(total), "#C9D1D9"),
            ("Vulnerabilities Found", str(vulnerable), "#E55353"),
            ("Secure Tests Passed", str(secure), "#2ECC71")
        ]

        for label, value, color in summary_items:
            tk.Label(self.summary_box, text=f"{label}: {value}", font=("Segoe UI", 11),
                     fg=color, bg="#161B22").pack(anchor="w", padx=10, pady=2)
