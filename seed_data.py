from db import get_db_connection

def seed():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS bookings')
    cursor.execute('DROP TABLE IF EXISTS shows')

    cursor.execute('''
        CREATE TABLE shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            venue TEXT NOT NULL,
            total_seats INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            show_id INTEGER NOT NULL,
            tickets INTEGER NOT NULL,
            FOREIGN KEY (show_id) REFERENCES shows(id)
        )
    ''')

    shows = [
        ("Coldplay Live", "2025-05-10", "Wembley Stadium, London", 100),
        ("Arijit Singh Night", "2025-06-12", "Jio Garden, Mumbai", 80),
        ("Imagine Dragons", "2025-07-01", "Madison Square Garden, New York", 120),
        ("KK Tribute Show", "2025-08-01", "Habitat Centre, Delhi", 50),
        ("AP Dhillon World Tour", "2025-08-20", "NSCI Dome, Mumbai", 70),
        ("Shreya Ghoshal Evening", "2025-09-05", "Siri Fort Auditorium, Delhi", 60),
        ("The Weeknd Tour", "2025-09-25", "Staples Center, Los Angeles", 110),
        ("B Praak Live", "2025-10-10", "Tagore Theatre, Chandigarh", 45),
        ("EDM Night ft. Nucleya", "2025-10-30", "Phoenix Arena, Hyderabad", 85),
        ("A.R. Rahman Symphony", "2025-11-15", "Jawaharlal Nehru Stadium, Chennai", 100),
    ]

    cursor.executemany("INSERT INTO shows (title, date, venue, total_seats) VALUES (?, ?, ?, ?)", shows)

    conn.commit()
    conn.close()
    print("✅ Database seeded with 10 concerts!")

if __name__ == "__main__":
    seed()
