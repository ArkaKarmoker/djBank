# djBank — Bank Account Transaction Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap 5">
  <img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Chart.js-4.x-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
</p>

A secure, modern, full-featured Bank Account Transaction Management System built with **Django**, **Bootstrap 5**, and **Chart.js**, featuring modern aesthetics, dark/light theme switching, and real-time transaction tracking.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Technology Stack](#-technology-stack)
- [Key Features](#-key-features)
- [Sample Database & Demo Credentials](#-sample-database--demo-credentials)
- [Installation & Local Setup Guide](#-installation--local-setup-guide)
- [Automated Testing](#-automated-testing)
- [UI Screenshots Showcase](#-ui-screenshots-showcase)
- [Project Architecture & Directory Structure](#-project-architecture--directory-structure)

---

## 🌟 Project Overview
**djBank** is designed to provide users with an intuitive, secure banking environment to manage their funds, monitor transaction histories, analyze monthly cash flow, and export account statements. The application strictly enforces data isolation and access controls so authenticated users can only view and interact with their own financial records.

---

## 🛠️ Technology Stack

| Layer / Category | Technology / Badge | Details & Purpose |
| :--- | :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | **Python 3.10+** — Core backend programming language |
| **Backend Framework** | ![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white) | **Django 5.0+** — High-level web framework (MTV architecture, ORM, Forms, Auth, Access Control) |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) | **SQLite 3** — Relational database storing user profiles, bank accounts, and transaction ledgers |
| **Frontend Framework** | ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=flat-square&logo=bootstrap&logoColor=white) | **Bootstrap 5.3** — Responsive UI grid layout, navbars, cards, badges, and modals |
| **Data Visualization** | ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white) | **Chart.js 4.x** — Interactive financial charts (Balance Growth Trend line chart & Cashflow breakdown doughnut chart) |
| **Client Scripting** | ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) | **JavaScript (ES6+)** — Dynamic dark/light theme toggle (`localStorage` integration), interactive password toggles & chart initialization |
| **Markup & Styling** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) | **HTML5 & Vanilla CSS3** — Glassmorphism design tokens, CSS variables, smooth transitions & responsive typography |
| **Iconography & Fonts** | ![Font Awesome](https://img.shields.io/badge/Font_Awesome-528DD7?style=flat-square&logo=fontawesome&logoColor=white) | **FontAwesome 6**, **Google Fonts** (*Inter* for primary text, *JetBrains Mono* for financial values) |
| **Export & Tools** | ![CSV](https://img.shields.io/badge/CSV-Export-green?style=flat-square) | **Streaming CSV Exporter** — On-the-fly export of filtered transaction histories |
| **Testing** | ![Django Test](https://img.shields.io/badge/Django-Test_Runner-44B78B?style=flat-square&logo=django&logoColor=white) | **Django TestCase** — Automated unit testing for auth, deposit logic, withdrawal validation & overdraft checks |

---

## ✨ Key Features

### 1. User Authentication & Security
- **User Registration**: Custom registration form automatically generates a unique 10-digit bank account number and supports an optional initial deposit.
- **Password Visibility Toggle**: Interactive eye icon inside password fields on Login and Registration forms for seamless user experience.
- **Login / Logout**: Secure authentication flow with instant feedback notifications.
- **Data Isolation**: Strict access control ensuring users can never view, edit, or access another user's bank account or transaction history.

### 2. Bank Account Management
- Stores Account Holder Name, 10-Digit Unique Account Number, and Real-Time Balance.
- Interactive Account Summary Widget displayed prominently on the user dashboard.

### 3. Deposit & Withdrawal Operations
- **Deposit System**: Input validation (Amount > 0), immediate balance addition, and transaction logging.
- **Withdrawal System & Overdraft Prevention**: Strict validation preventing withdrawals that exceed current available balance.
- **Visual Color Indicators**: Deposits are highlighted in green (`+$X.XX`), while withdrawals are in red (`-$X.XX`).

### 4. Transaction History & Filtering
- **Detailed Ledger**: Records Transaction Type, Amount, Date & Time, Balance After Transaction, and Notes.
- **Newest First**: Sorted in reverse chronological order (`-timestamp`).
- **Advanced Filtering**: Filter by transaction type (All, Deposit, Withdrawal) and custom date range (Start Date to End Date).
- **Pagination**: Clean paginated transaction history table (8 items per page) with page navigation controls.
- **CSV Export**: Direct downloadable account statement in `.csv` format respecting active filters (Sample demo file included: [`statement_1002948192.csv`](./statement_1002948192.csv)).

### 5. Interactive Dashboard & Analytics
- **Summary Cards**: Quick metrics for Current Balance, Total Deposit Amount, Total Withdrawal Amount, and Total Transactions Count.
- **Monthly Summary Table**: Grouped breakdown of total deposits vs. withdrawals aggregated by month.
- **Interactive Chart Visualizations**: Powered by Chart.js displaying:
  1. Balance Growth Trend (Line Chart)
  2. Cashflow Volume Breakdown (Doughnut Chart)

### 6. Modern Glassmorphism UI & Themes
- **Responsive Design**: Styled with Bootstrap 5, custom CSS design tokens, Google Fonts (*Inter*), and FontAwesome 6 icons.
- **Dark / Light Theme Switcher**: Dynamic theme toggle with persistent preference saved in browser `localStorage`.

---

## 🗄️ Sample Database & Demo Credentials

The project comes with a pre-populated **Sample Database** (`db.sqlite3`) and an automated database seeding script (`populate_db.py`).

### Pre-populated Demo Accounts:

| Role | Username | Password | Account Number | Initial Balance | Sample Transactions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Demo User 1** | `john_doe` | `Password123` | `1002948192` | ~$20,172.39 | 35 realistic transactions |
| **Demo User 2** | `jane_smith` | `Password123` | `9876543210` | ~$12,322.21 | 25 realistic transactions |
| **Superuser / Admin** | `admin` | `admin123` | N/A | N/A | Admin access to Django admin panel |

---

## 🚀 Installation & Local Setup Guide

Follow these steps to set up and run the project locally:

### 1. Prerequisites
- **Python 3.10+** installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/ArkaKarmoker/djBank.git
cd djBank
```

### 3. Create & Activate Virtual Environment
```bash
# On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Setup & Sample Data Seeding
```bash
# Create and apply database migrations
python manage.py makemigrations
python manage.py migrate

# Seed database with sample users & transactions (Optional - pre-populated database included)
python populate_db.py
```

### 6. Start Development Server
```bash
python manage.py runserver
```

Open your web browser and navigate to: `http://127.0.0.1:8000/`

---

## 🧪 Automated Testing

The application includes unit tests covering User Authentication, Account Creation, Deposit validation, Overdraft prevention, and Transaction logging.

Run all automated unit tests:
```bash
python manage.py test
```

---

## 📸 UI Screenshots Showcase

> **Note**: All 17 high-resolution application UI and admin panel screenshots are stored inside the [`screenshots/`](./screenshots) directory in this repository.

### 🎨 Application Views (Light & Dark Mode)

#### 1. Registration Page
| Light Theme | Dark Theme |
| :---: | :---: |
| ![Registration Light](<screenshots/1. Registration Page Light.jpeg>) | ![Registration Dark](<screenshots/2. Registration Page Dark.jpeg>) |

#### 2. Login Page
| Light Theme | Dark Theme |
| :---: | :---: |
| ![Login Light](<screenshots/3. Login Page Light.jpeg>) | ![Login Dark](<screenshots/4. Login Page Dark.jpeg>) |

#### 3. Dashboard
| Light Theme | Dark Theme |
| :---: | :---: |
| ![Dashboard Light](<screenshots/5. Dashboard Light.jpeg>) | ![Dashboard Dark](<screenshots/6. Dashboard Dark.jpeg>) |

#### 4. Deposit Page
| Light Theme | Dark Theme |
| :---: | :---: |
| ![Deposit Light](<screenshots/7. Deposit Light.jpeg>) | ![Deposit Dark](<screenshots/8. Deposit Dark.jpeg>) |

#### 5. Withdraw Page
| Light Theme | Dark Theme |
| :---: | :---: |
| ![Withdraw Light](<screenshots/9. Withdraw Light.jpeg>) | ![Withdraw Dark](<screenshots/10. Withdraw Dark.jpeg>) |

#### 6. Transaction History
| Light Theme | Dark Theme |
| :---: | :---: |
| ![History Light](<screenshots/11. History Light.jpeg>) | ![History Dark](<screenshots/12. History Dark.jpeg>) |

#### 7. Responsive Mobile View
| Light Theme | Dark Theme |
| :---: | :---: |
| ![Responsive Light](<screenshots/13. Responsive Light.png>) | ![Responsive Dark](<screenshots/14. Responsive Dark.png>) |

---

### ⚙️ Django Admin Panel Views

| Bank Accounts | Users List |
| :---: | :---: |
| ![Admin Bank Accounts](<screenshots/15. Admin Panel Bank Accounts.jpeg>) | ![Admin Users](<screenshots/16. Admin Panel Users.jpeg>) |

#### Admin Transactions
![Admin Transactions](<screenshots/17. Admin Panel Transactions.jpeg>)

---

## 📁 Project Architecture & Directory Structure

```text
djBank/
├── accounts/                  # User Authentication & Account App
│   ├── models.py              # BankAccount Model definition
│   ├── views.py               # Register, Login, Logout views
│   ├── forms.py               # Registration & Login Forms
│   └── urls.py                # Accounts routing
├── transactions/              # Transaction Management App
│   ├── models.py              # Transaction Model definition
│   ├── views.py               # Deposit, Withdraw, History, CSV Export views
│   ├── forms.py               # DepositForm & WithdrawForm
│   └── urls.py                # Transaction routing
├── bank_management/           # Core Project Configuration
│   ├── settings.py            # Global Settings
│   └── urls.py                # Root URL Routing
├── templates/                 # Global Template Directory
│   ├── base.html              # Base layout with navbar, dark mode & messages
│   ├── dashboard.html         # User Dashboard & Chart visualizer
│   ├── accounts/              # Authentication templates (Login, Register)
│   └── transactions/          # Deposit, Withdraw, History templates
├── static/                    # Static Assets
│   ├── css/style.css          # Glassmorphism design system & dark mode variables
│   └── js/main.js             # Theme switcher & UI helpers
├── screenshots/               # Application UI screenshots
├── populate_db.py             # Database seeding script
├── db.sqlite3                 # Pre-populated Sample SQLite Database
├── statement_1002948192.csv   # Sample exported CSV bank statement
├── requirements.txt           # Project dependencies file
├── manage.py                  # Django CLI runner
└── README.md                  # Project Documentation
```

---

Thank you for taking the time to review the **djBank** project!

Developed by [Arka Karmoker](https://github.com/ArkaKarmoker).
