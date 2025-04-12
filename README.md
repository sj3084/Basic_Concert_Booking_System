# 🎵 Concert Booking System

A simple web-based Concert Booking System built using **Python** and **Flask**, backed by an SQLite database. This application allows users to browse available concerts, book tickets, and view their booking history.

---

## 🚀 Features

- View upcoming concerts
- Book tickets for concerts
- View booking history
- Simple web UI with HTML templates
- Lightweight SQLite backend

---

## 🗂️ Project Structure

```
concert_booking/
│
├── app.py               # Main Flask app
├── db.py                # Database connection and setup
├── seed_data.py         # Seed initial concert data into the DB
├── check_shows.py       # Show availability logic
├── database.db          # SQLite database
├── templates/           # HTML templates
│   ├── index.html
│   ├── home.html
│   ├── book.html
│   ├── history.html
│   └── success.html
```

---

## 🛠️ Setup Instructions

### 1. Clone or extract the repository

Unzip the project folder or clone the repository if using version control.

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

This project uses Flask. Install it using pip:

```bash
pip install flask
```

### 4. Seed the database (optional)

If starting from scratch or resetting the data:

```bash
python seed_data.py
```

### 5. Run the application

```bash
python app.py
```

### 6. Open in browser

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to use the app.

---

## ✅ Requirements

- Python 3.7 or higher
- Flask

---
