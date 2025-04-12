import time
import sqlite3
from flask import Flask, render_template, request
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search')
def search():
    city = request.args.get("city")
    try:
        conn = get_db_connection()
        shows = conn.execute("SELECT * FROM shows WHERE venue LIKE ?", ('%' + city + '%',)).fetchall()
        conn.close()
        return render_template("index.html", shows=shows, city=city)
    except Exception as e:
        return f"❌ Failed to fetch shows: {str(e)}"

def safe_book(show_id, user_name, requested_tickets, max_retries=3):
    attempt = 0
    while attempt < max_retries:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")

            cursor.execute("SELECT total_seats FROM shows WHERE id = ?", (show_id,))
            total_seats = cursor.fetchone()["total_seats"]

            cursor.execute("SELECT SUM(tickets) FROM bookings WHERE show_id = ?", (show_id,))
            booked = cursor.fetchone()[0] or 0

            available = total_seats - booked
            if requested_tickets > available:
                conn.rollback()
                return (False, available)

            cursor.execute("INSERT INTO bookings (user_name, show_id, tickets) VALUES (?, ?, ?)",
                           (user_name, show_id, requested_tickets))
            conn.commit()
            return (True, available - requested_tickets)

        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                attempt += 1
                time.sleep(0.5)
            else:
                print("❌ DB Error:", e)
                break
        finally:
            conn.close()

    return (None, None)

@app.route('/book/<int:show_id>', methods=['GET', 'POST'])
def book(show_id):
    conn = get_db_connection()
    show = conn.execute("SELECT * FROM shows WHERE id = ?", (show_id,)).fetchone()

    cursor = conn.execute("SELECT SUM(tickets) FROM bookings WHERE show_id = ?", (show_id,))
    booked = cursor.fetchone()[0] or 0
    available = show['total_seats'] - booked
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        tickets = int(request.form['tickets'])

        status, new_availability = safe_book(show_id, name, tickets)

        if status is True:
            return render_template("success.html", name=name, show=show, tickets=tickets)
        elif status is False:
            return render_template("book.html", show=show, available=available, error="❌ Not enough tickets left.")
        else:
            return render_template("book.html", show=show, available=available, error="⚠️ System busy. Try again.")

    return render_template("book.html", show=show, available=available)

@app.route('/bookings')
def booking_history():
    user_name = request.args.get('name')

    if not user_name:
        return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>View My Bookings</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body class="container py-5">
                <h2 class="text-center mb-4">📜 Booking History</h2>
                <form method="get" class="w-50 mx-auto">
                    <div class="mb-3">
                        <label for="name" class="form-label">Enter your name:</label>
                        <input type="text" name="name" id="name" class="form-control" placeholder="e.g., Prakarsh" required>
                    </div>
                    <div class="text-center">
                        <button type="submit" class="btn btn-primary">🔍 View My Bookings</button>
                    </div>
                </form>
                <div class="text-center mt-4">
                    <a href="/" class="btn btn-secondary">⬅ Back to Home</a>
                </div>
            </body>
            </html>
        '''

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.tickets, s.title, s.date, s.venue
            FROM bookings b
            JOIN shows s ON b.show_id = s.id
            WHERE b.user_name = ?
        ''', (user_name,))
        bookings = cursor.fetchall()
        conn.close()

        return render_template("history.html", name=user_name, bookings=bookings)

    except Exception as e:
        return f"❌ Failed to retrieve bookings: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
