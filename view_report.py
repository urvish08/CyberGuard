import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ReportPage:
    def __init__(self, root, parent_frame, controller=None):
        self.root = root
        self.parent_frame = parent_frame
        self.controller = controller
        self.history_data = []
        self.create_report_ui()

    def clear_frame(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

    def create_report_ui(self):
        self.clear_frame()
        self.report_frame = tk.Frame(self.parent_frame, bg="#0D1117")
        self.report_frame.pack(fill="both", expand=True)

        # Logo and Tool Name
        top_frame = tk.Frame(self.report_frame, bg="#161B22", height=70)
        top_frame.pack(fill="x")
        logo_img = Image.open("C:/Coding/CyberGuard-Scanner/cyberguard_logo.png")
        logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        tk.Label(top_frame, image=self.logo_photo, bg="#161B22").pack(side="left", padx=10)
        tk.Label(top_frame, text="CYBERGUARD", fg="#58A6FF", bg="#161B22",
                 font=('Segoe UI Black', 20)).pack(side="left")

        # Heading
        tk.Label(self.report_frame, text="🗂 View Scan Reports", font=("Segoe UI", 20, "bold"),
                 fg="#58A6FF", bg="#0D1117").pack(pady=10)

        # History list
        tk.Label(self.report_frame, text="Recent Scanned URLs:", font=("Segoe UI", 13, "bold"),
                 fg="#C9D1D9", bg="#0D1117").pack(pady=5)
        self.url_listbox = tk.Listbox(self.report_frame, width=70, height=6, bg="#161B22", fg="white",
                                      font=("Segoe UI", 11))
        self.url_listbox.pack(pady=5)
        self.url_listbox.bind("<<ListboxSelect>>", self.load_selected_report)

        self.report_box = ScrolledText(self.report_frame, width=100, height=18, bg="#161B22",
                                       fg="#C9D1D9", font=("Consolas", 10), insertbackground="white")
        self.report_box.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(self.report_frame, bg="#0D1117")
        btn_frame.pack(pady=10)
        send_email_btn = ttk.Button(btn_frame, text="📧 Email Report", command=self.open_email_popup)
        send_email_btn.pack(side="left", padx=5)

        if self.controller:
            home_btn = ttk.Button(btn_frame, text="🏠 Back to Home",
                                  command=lambda: self.controller.show_frame("home"))
            home_btn.pack(side="left", padx=5)

        self.load_history()

    def load_history(self):
        self.url_listbox.delete(0, tk.END)
        file_path = "scan_history.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.history_data = json.load(f)
            for entry in self.history_data:
                self.url_listbox.insert(tk.END, f"{entry['url']}  —  {entry['timestamp']}")
        else:
            self.url_listbox.insert(tk.END, "No scan history found.")

    def load_selected_report(self, event):
        selection = event.widget.curselection()
        if not selection:
            return
        index = selection[0]
        if index >= len(self.history_data):
            return
        entry = self.history_data[index]
        self.display_report(entry)

    def display_report(self, entry):
        self.report_box.delete("1.0", tk.END)
        self.report_box.insert(tk.END, f"🔍 Scan Report for {entry['url']}\n")
        self.report_box.insert(tk.END, f"🕒 Scanned At: {entry['timestamp']}\n\n")
        for item in entry["results"]:
            self.report_box.insert(tk.END, f"• {item['name']} [{item['severity']}]: {item['status']}\n")
            if "Vulnerable" in item["status"]:
                self.report_box.insert(tk.END, f"  ↪ Remediation: {item['remediation']}\n\n")
            else:
                self.report_box.insert(tk.END, f"  ↪ No action needed.\n\n")
        self.report_box.insert(tk.END, "✅ Report Loaded Successfully.\n")

    def open_email_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Send Report via Email")
        popup.configure(bg="#0D1117")
        popup.geometry("400x350")

        tk.Label(popup, text="Recipient Email:", bg="#0D1117", fg="#C9D1D9",
                 font=("Segoe UI", 10)).pack(pady=5)
        to_entry = tk.Entry(popup, width=40)
        to_entry.pack(pady=5)

        tk.Label(popup, text="Subject:", bg="#0D1117", fg="#C9D1D9",
                 font=("Segoe UI", 10)).pack(pady=5)
        subject_entry = tk.Entry(popup, width=40)
        subject_entry.insert(0, "CyberGuard Scan Report")
        subject_entry.pack(pady=5)

        tk.Label(popup, text="Message:", bg="#0D1117", fg="#C9D1D9",
                 font=("Segoe UI", 10)).pack(pady=5)
        msg_text = ScrolledText(popup, width=40, height=6)
        msg_text.insert(tk.END, "Please find the scan report attached below.")
        msg_text.pack(pady=5)

        ttk.Button(popup, text="Send Email",
                   command=lambda: self.send_email(
                       to_entry.get(),
                       subject_entry.get(),
                       msg_text.get("1.0", tk.END))
                   ).pack(pady=10)

    def send_email(self, to_email, subject, body):
        try:
            sender_email = "up423713@gmail.com"
            sender_password = "wmzqpghsuvagtink"  # Use app password for Gmail

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = to_email
            msg["Subject"] = subject

            full_body = body + "\n\n" + self.report_box.get("1.0", tk.END)
            msg.attach(MIMEText(full_body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)

            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email.\n\n{str(e)}")
