from db import get_db_connection

def show_all_shows():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM shows")
        shows = cursor.fetchall()

        print(f"📊 Found {len(shows)} show(s):")
        for show in shows:
            print(f"{show['id']}: {show['title']} on {show['date']} at {show['venue']}")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    show_all_shows()
