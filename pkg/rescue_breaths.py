import os
import sqlite3
import ctypes
from datetime import datetime, timedelta
import csv


def get_db_path():
    app_data = os.getenv('APPDATA')
    if not app_data:
        raise Exception("APPDATA environment variable not found.")
    db_path = os.path.join(app_data, 'HermetoPascoal', 'db', 'vento-1.3.2.db')
    if not os.path.exists(db_path):
        raise Exception(f"Database file not found at {db_path}")
    return db_path


def get_latest_exam_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM exams ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        raise Exception("No exams found in the database.")


def get_breaths_for_exam(conn, exam_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date_time_finish
        FROM breaths
        WHERE exam_id = ? AND deleted_at IS NOT NULL
    """, (exam_id,))
    breaths = cursor.fetchall()
    return breaths  # List of tuples (id, date_time_finish)


def parse_date_string(date_string):
    # Replace space with 'T' for ISO format
    date_string = date_string.replace(' ', 'T')
    # If there is fractional seconds, ensure it has at most 6 digits
    if '.' in date_string:
        date_part, fractional_and_tz = date_string.split('.', 1)
        # Split fractional_and_tz into fractional part and timezone
        if '+' in fractional_and_tz:
            fractional_part, tz_part = fractional_and_tz.split('+', 1)
            tz_sign = '+'
        elif '-' in fractional_and_tz:
            fractional_part, tz_part = fractional_and_tz.split('-', 1)
            tz_sign = '-'
        else:
            fractional_part = fractional_and_tz
            tz_part = ''
            tz_sign = ''
        # Truncate fractional_part to 6 digits
        fractional_part = fractional_part[:6]
        new_date_string = f"{date_part}.{fractional_part}"
        if tz_sign:
            new_date_string += f"{tz_sign}{tz_part}"
    else:
        new_date_string = date_string
    dt = datetime.fromisoformat(new_date_string)
    return dt


def update_breaths(conn, breaths):
    cursor = conn.cursor()
    for idx, (breath_id, date_time_finish) in enumerate(breaths):
        if date_time_finish is None:
            raise Exception(f"date_time_finish is NULL for breath id {breath_id}")

        try:
            date_time_finish_dt = parse_date_string(date_time_finish)
        except Exception as e:
            raise Exception(f"Invalid date_time_finish format for breath id {breath_id}: {date_time_finish}") from e

        breath_confirm_dt = date_time_finish_dt + timedelta(seconds=1)
        breath_confirm_str = breath_confirm_dt.isoformat(sep=' ', timespec='microseconds')

        # If it's not the last breath, set alert_start as usual
        if idx < len(breaths) - 1:
            alert_start_dt = breath_confirm_dt + timedelta(seconds=1)
            alert_start_str = alert_start_dt.isoformat(sep=' ', timespec='microseconds')
        else:
            # Last breath: set alert_start to NULL explicitly
            alert_start_str = None

        cursor.execute("""
            UPDATE breaths
            SET deleted_at = NULL,
                breath_confirm = ?,
                alert_start = ?
            WHERE id = ?
        """, (breath_confirm_str, alert_start_str, breath_id))

    conn.commit()


def update_breath_gas(conn, breaths):
    cursor = conn.cursor()
    breath_ids = [breath_id for breath_id, _ in breaths]
    if not breath_ids:
        return
    placeholders = ','.join('?' for _ in breath_ids)
    query = f"""
        UPDATE breath_gas
        SET deleted_at = NULL
        WHERE breath_id IN ({placeholders}) AND deleted_at IS NOT NULL
    """
    cursor.execute(query, breath_ids)
    conn.commit()


def get_gas_name(gas_id):
    if gas_id == 1:
        return "H2"
    elif gas_id == 2:
        return "CH4"
    else:
        return "unknown"


def export_to_csv(conn, exam_id, output_filename):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.exam_id, b.id as breath_id, bg.id as breath_gas_id, bg.created_at, bg.gas, bg.ppm
        FROM breaths b
        JOIN breath_gas bg ON b.id = bg.breath_id
        WHERE b.exam_id = ?
        ORDER BY b.id, bg.id
    """, (exam_id,))
    rows = cursor.fetchall()

    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Exam ID', 'Breath ID', 'BreathGas ID', 'Created At', 'Gas', 'PPM'])

        for row in rows:
            exam_id, breath_id, breath_gas_id, created_at, gas_id, ppm = row
            gas_name = get_gas_name(gas_id)
            csvwriter.writerow([exam_id, breath_id, breath_gas_id, created_at, gas_name, ppm])


def rescue_breaths():
    # Define the timestamp at the start of the script
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"breaths_rescue_{timestamp}.csv"

    # add Desktop path to the output_filename
    output_filename = os.path.join(os.path.expanduser("~"), "Desktop", output_filename)

    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        exam_id = get_latest_exam_id(conn)
        breaths = get_breaths_for_exam(conn, exam_id)
        if not breaths:
            print(f"No breaths with deleted_at IS NOT NULL for exam_id {exam_id}")
            return
        update_breaths(conn, breaths)
        update_breath_gas(conn, breaths)
        export_to_csv(conn, exam_id, output_filename)
        print(f"Data exported successfully to {output_filename}")
    finally:
        conn.close()

