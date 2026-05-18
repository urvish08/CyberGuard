# 🔐 CyberGuard – Web Vulnerability Scanner with GUI and Real-Time Reporting

<p align="center">
CyberGuard is a Python-based desktop application built to simplify website security analysis through an interactive graphical interface.
It combines scanning, reporting, log management, and dashboard visualization into one organized platform.
</p>

---

# 💡 Project Overview

CyberGuard was created with the goal of making security analysis easier to understand and easier to use.

Instead of manually checking website activity and handling multiple tools separately, CyberGuard provides a centralized interface where users can:

✔ Scan websites  
✔ View scan reports  
✔ Track scan history  
✔ Manage logs  
✔ Visualize previous scan data  
✔ Customize application settings  

The application focuses on usability and clear presentation of results.

---

# 🚀 Main Features

## 🔍 Website Scanning
- Enter target website URL
- Start scans directly from GUI
- Displays scan activity
- Shows generated results

---

## 📄 Report Generation
- Export scan reports into PDF format
- Makes results easier to save and share

---

## 📧 Email Report Support
- Send generated reports through email

---

## 📊 Dashboard Visualization
- View previously scanned data
- Displays stored scan records
- Provides visual overview of scan activities

---

## 📁 Logs Management
- Store scan history
- View previous scans
- Manage collected logs

---

## ⚙ Settings Management

Customize application behavior:

- Theme selection
- Sound alert settings
- Auto-save logs
- Scan timeout configuration

Available themes:

- Dark Theme
- Light Theme
- Blue Theme

---

# 🖥 Application Screens

## 🏠 Home Screen

Main landing page of CyberGuard providing navigation to all modules.

![Home](CybderguardS/home.png)

---

## 🔍 Scan Screen

Allows users to enter a target URL and start website scanning.

Features:
- URL input
- Start Scan button
- Scan output area
- Export PDF button

![Start Scan](CybderguardS/start_scan.png)

---

## 📄 Report Viewer

Displays previously generated reports.

Features:
- Recent scanned URLs
- Report viewing
- Email report support

![View Reports](CybderguardS/view_report.png)

---

## 📁 Logs Screen

Displays previous scan activities.

Features:
- Log records
- Scan history
- Log management

![Logs](CybderguardS/logs.png)

---

## ⚙ Settings Screen

Customize application preferences.

Features:
- Theme selection
- Sound settings
- Scan timeout settings

![Settings](CybderguardS/settings.png)

---

## 📊 Dashboard Screen

Provides a visual overview of previous scan activities.

Features:
- Scan summary
- Dashboard visualization

![Dashboard](CybderguardS/dashboard.png)

---

# 🛠 Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Core application |
| Tkinter | GUI development |
| Requests | HTTP requests |
| BeautifulSoup | HTML parsing |
| FPDF | PDF generation |
| smtplib | Email support |
| JSON | Data storage |
| Matplotlib | Dashboard charts |
| Pillow (PIL) | Image handling |

---

# 📂 Project Structure

```bash
CyberGuard/
│
├── home.py
├── start_scan.py
├── view_report.py
├── dashboard.py
├── logs.py
├── settings.py
├── requirements.txt
├── README.md
├── screenshots/
│     ├── home.png
│     ├── start_scan.png
│     ├── view_report.png
│     ├── logs.png
│     ├── settings.png
│     └── dashboard.png
│
└── assets/
```

# 📦 Installation

Clone repository:

```bash
git clone https://github.com/YOUR-USERNAME/CyberGuard.git
```

Go into project folder:

```bash
cd CyberGuard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
python home.py
```

---

# 🎯 Intended Users

CyberGuard can be useful for:

- Cybersecurity students
- Web developers
- Security learners
- Python learners
- Security enthusiasts

---

# 👨‍💻 Developer

**Urvishkumar Prajapati**

Python Developer | Cybersecurity Enthusiast

---

# ⭐ Support

If you found this project useful, give it a ⭐ on GitHub.

CyberGuard — Simplifying Website Security Analysis
