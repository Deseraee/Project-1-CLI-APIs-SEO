import sqlite3


def create_tables():
    connection = sqlite3.connect("mydatabase.db")
    curr = connection.cursor()

    curr.execute("""
        CREATE TABLE IF NOT EXISTS OutSafeUsers (
            username TEXT PRIMARY KEY,
            last_login TEXT
        )
    """)

    curr.execute("""
        CREATE TABLE IF NOT EXISTS OutSafeGolfReports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            location TEXT,
            holes TEXT,
            vehicle TEXT,
            report_time TEXT,
            current_temperature REAL,
            current_weather TEXT,
            humidity INTEGER,
            aqi INTEGER,
            uv_index REAL,
            verdict TEXT,
            reasons TEXT,
            forecast_time TEXT,
            forecast_temperature REAL,
            forecast_weather TEXT,
            better_tee_time TEXT,
            better_tee_temperature REAL,
            better_tee_weather TEXT,
            summary TEXT
        )
    """)

    connection.commit()
    connection.close()


def get_last_login(username):
    create_tables()

    connection = sqlite3.connect("mydatabase.db")
    curr = connection.cursor()

    curr.execute("""
        SELECT last_login
        FROM OutSafeUsers
        WHERE username = ?
    """, (username,))

    result = curr.fetchone()
    connection.close()

    if result is None:
        return None

    return result[0]


def login_user(username, login_time):
    create_tables()

    connection = sqlite3.connect("mydatabase.db")
    curr = connection.cursor()

    curr.execute("""
        INSERT OR REPLACE INTO OutSafeUsers (username, last_login)
        VALUES (?, ?)
    """, (username, login_time))

    connection.commit()
    connection.close()


def save_report(username, location, holes, vehicle, report_time, temp, description, humidity, aqi, uv, verdict, reasons, forecast_time, forecast_temp, forecast_description, better_tee_time, better_tee_temp, better_tee_weather, summary):
    create_tables()

    connection = sqlite3.connect("mydatabase.db")
    curr = connection.cursor()

    curr.execute("""
        INSERT INTO OutSafeGolfReports (
            username,
            location,
            holes,
            vehicle,
            report_time,
            current_temperature,
            current_weather,
            humidity,
            aqi,
            uv_index,
            verdict,
            reasons,
            forecast_time,
            forecast_temperature,
            forecast_weather,
            better_tee_time,
            better_tee_temperature,
            better_tee_weather,
            summary
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        location,
        holes,
        vehicle,
        report_time,
        temp,
        description,
        humidity,
        aqi,
        uv,
        verdict,
        "; ".join(reasons),
        forecast_time,
        forecast_temp,
        forecast_description,
        better_tee_time,
        better_tee_temp,
        better_tee_weather,
        summary
    ))

    connection.commit()
    connection.close()


def view_recent_reports(username):
    create_tables()

    connection = sqlite3.connect("mydatabase.db")
    curr = connection.cursor()

    curr.execute("""
        SELECT location, holes, vehicle, report_time, current_temperature, aqi, uv_index, verdict, better_tee_time
        FROM OutSafeGolfReports
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 5
    """, (username,))

    reports = curr.fetchall()
    connection.close()

    return reports