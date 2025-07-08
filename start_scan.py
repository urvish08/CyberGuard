import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from fpdf import FPDF
from datetime import datetime
import threading
import requests
import re
import json
import os
from bs4 import BeautifulSoup

class ScanPage:
    def __init__(self, root, parent_frame, controller=None):
        self.root = root
        self.parent_frame = parent_frame
        self.controller = controller
        self.report_data = []
        self.create_scan_ui()

    def clear_frame(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def create_scan_ui(self):
        self.clear_frame()
        self.scan_frame = tk.Frame(self.parent_frame, bg="#0D1117")
        self.scan_frame.pack(fill="both", expand=True)

        top_frame = tk.Frame(self.scan_frame, bg="#161B22", height=70)
        top_frame.pack(fill="x")
        logo_img = Image.open("C:/Coding/CyberGuard-Scanner/cyberguard_logo.png")
        logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        tk.Label(top_frame, image=self.logo_photo, bg="#161B22").pack(side="left", padx=10)
        tk.Label(top_frame, text="CYBERGUARD", fg="#58A6FF", bg="#161B22",
                 font=('Segoe UI Black', 20)).pack(side="left")

        tk.Label(self.scan_frame, text="🔍 Web Vulnerability Scan", font=("Segoe UI", 20, "bold"),
                 fg="#58A6FF", bg="#0D1117").pack(pady=20)

        entry_frame = tk.Frame(self.scan_frame, bg="#0D1117")
        entry_frame.pack(pady=10)
        tk.Label(entry_frame, text="Target URL:", font=("Segoe UI", 13),
                 fg="#C9D1D9", bg="#0D1117").pack(side="left", padx=5)
        self.url_entry = ttk.Entry(entry_frame, width=40)
        self.url_entry.pack(side="left", padx=5)
        self.start_button = ttk.Button(entry_frame, text="Start Scan", command=self.start_scan)
        self.start_button.pack(side="left", padx=10)

        self.progress = ttk.Progressbar(self.scan_frame, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(pady=15)

        tk.Label(self.scan_frame, text="Scan Report:", font=("Segoe UI", 13, "bold"),
                 fg="#58A6FF", bg="#0D1117").pack(pady=5)
        self.report_area = ScrolledText(self.scan_frame, width=100, height=18,
                                        bg="#161B22", fg="#C9D1D9",
                                        font=("Consolas", 10), insertbackground="white")
        self.report_area.pack(pady=5)

        ttk.Button(self.scan_frame, text="📄 Export PDF Report", command=self.export_report_pdf).pack(pady=10)

        if self.controller:
            home_btn = ttk.Button(self.scan_frame, text="🏠 Back to Home",
                                  command=lambda: self.controller.show_frame("home"))
            home_btn.pack(pady=10)

    def start_scan(self):
        url = self.url_entry.get()
        if not url.startswith("http"):
            messagebox.showerror("Invalid URL", "Please enter a full valid URL (including http/https).")
            return

        self.report_area.delete("1.0", tk.END)
        self.report_data.clear()
        self.progress.start(10)
        self.start_button.config(state="disabled")
        threading.Thread(target=self.perform_scan, args=(url,)).start()

    def perform_scan(self, url):
        self.append_report(f"🔍 Scanning URL: {url}\n\n")

        # 1. SQL Injection Check
        payload_url = url + "?id=' OR 1=1--"
        try:
            r = requests.get(payload_url, timeout=10)
            if any(err in r.text.lower() for err in ["sql", "syntax", "query", "mysql", "error"]):
                self.add_finding("SQL Injection", "High", "❌ Vulnerable", "Use parameterized queries.")
            else:
                self.add_finding("SQL Injection", "High", "✅ Secure", "")
        except:
            self.add_finding("SQL Injection", "High", "⚠️ Error", "Could not connect.")

        # 2. XSS Check
        try:
            test = "<script>alert('XSS')</script>"
            xss_url = url + f"?test={test}"
            r = requests.get(xss_url, timeout=10)
            if test in r.text:
                self.add_finding("Cross-Site Scripting (XSS)", "Medium", "❌ Vulnerable", "Sanitize user inputs.")
            else:
                self.add_finding("Cross-Site Scripting (XSS)", "Medium", "✅ Secure", "")
        except:
            self.add_finding("Cross-Site Scripting (XSS)", "Medium", "⚠️ Error", "Could not connect.")

        # 3. Open Redirect Check
        try:
            redirect_url = url + "?next=http://evil.com"
            r = requests.get(redirect_url, allow_redirects=False)
            if "evil.com" in r.headers.get("Location", ""):
                self.add_finding("Open Redirect", "Low", "❌ Vulnerable", "Validate redirect URLs.")
            else:
                self.add_finding("Open Redirect", "Low", "✅ Secure", "")
        except:
            self.add_finding("Open Redirect", "Low", "⚠️ Error", "Could not connect.")

        # 4. Security Headers Check
        try:
            r = requests.get(url, timeout=10)
            headers = r.headers
            issues = []
            required = ['X-Frame-Options', 'Content-Security-Policy', 'X-XSS-Protection']
            for h in required:
                if h not in headers:
                    issues.append(h)
            if issues:
                self.add_finding("Security Headers", "Medium", "❌ Vulnerable", f"Missing headers: {', '.join(issues)}")
            else:
                self.add_finding("Security Headers", "Medium", "✅ Secure", "")
        except:
            self.add_finding("Security Headers", "Medium", "⚠️ Error", "Could not connect.")

        # 5. CSRF Token Check
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            forms = soup.find_all("form")
            tokens = 0
            for form in forms:
                if form.find("input", {"type": "hidden", "name": re.compile("csrf", re.I)}):
                    tokens += 1
            if tokens == 0:
                self.add_finding("CSRF Protection", "Medium", "❌ Vulnerable", "Use CSRF tokens in forms.")
            else:
                self.add_finding("CSRF Protection", "Medium", "✅ Secure", "")
        except:
            self.add_finding("CSRF Protection", "Medium", "⚠️ Error", "Could not connect.")

        self.append_report("✅ Scan Completed.\n")
        self.progress.stop()
        self.start_button.config(state="normal")
        self.save_scan_result(url)

    def add_finding(self, name, severity, status, remediation):
        self.report_data.append((name, severity, status, remediation))
        self.append_report(f"• {name} [{severity}]: {status}\n")
        if "Vulnerable" in status:
            self.append_report(f"  ↪ Remediation: {remediation}\n\n")
        elif "Secure" in status:
            self.append_report("  ↪ No action needed.\n\n")
        else:
            self.append_report(f"  ↪ Info: {remediation}\n\n")

    def append_report(self, text):
        self.report_area.insert(tk.END, text)
        self.report_area.see(tk.END)

    def save_scan_result(self, url):
        entry = {
            "url": url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "results": [
                {
                    "name": name,
                    "severity": severity,
                    "status": status,
                    "remediation": fix
                }
                for name, severity, status, fix in self.report_data
            ]
        }
        file_path = "scan_history.json"
        history = []
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                history = json.load(f)
        history.insert(0, entry)
        history = history[:5]
        with open(file_path, "w") as f:
            json.dump(history, f, indent=4)

    def export_report_pdf(self):
        if not self.report_data:
            messagebox.showinfo("No Report", "Run a scan before exporting.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(200, 10, "CyberGuard - Vulnerability Report", ln=True, align='C')
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        for name, severity, status, fix in self.report_data:
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 10, f"{name} [{severity}]: {status}")
            if "Vulnerable" in status:
                pdf.set_text_color(200, 0, 0)
                pdf.multi_cell(0, 10, f"Remediation: {fix}")
            else:
                pdf.set_text_color(0, 128, 0)
                pdf.multi_cell(0, 10, "No action needed.")
            pdf.ln(1)

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Exported", f"PDF report saved to {file_path}")
