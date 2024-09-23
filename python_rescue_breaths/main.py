import os
import sqlite3
import ctypes
from datetime import datetime, timedelta

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
    for breath_id, date_time_finish in breaths:
        if date_time_finish is None:
            raise Exception(f"date_time_finish is NULL for breath id {breath_id}")
        try:
            date_time_finish_dt = parse_date_string(date_time_finish)
        except Exception as e:
            raise Exception(f"Invalid date_time_finish format for breath id {breath_id}: {date_time_finish}") from e
        breath_confirm_dt = date_time_finish_dt + timedelta(seconds=1)
        breath_confirm_str = breath_confirm_dt.isoformat(sep=' ', timespec='microseconds')
        alert_start_dt = breath_confirm_dt + timedelta(seconds=1)
        alert_start_str = alert_start_dt.isoformat(sep=' ', timespec='microseconds')
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

def print_breaths(conn, exam_id, output_file=None):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM breaths WHERE exam_id = ? ORDER BY id", (exam_id,))
    breaths = cursor.fetchall()
    for (breath_id,) in breaths:
        output_line = f"breaths.id {breath_id}"
        print(output_line)
        if output_file:
            output_file.write(output_line + '\n')
        cursor.execute("SELECT gas, ppm FROM breath_gas WHERE breath_id = ?", (breath_id,))
        gases = cursor.fetchall()
        for gas_id, ppm in gases:
            gas_name = get_gas_name(gas_id)
            output_line = f"- breath_gas.gas {gas_name} | breath_gas.ppm {ppm}"
            print(output_line)
            if output_file:
                output_file.write(output_line + '\n')

def main():
    # Define the timestamp at the start of the script
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"breaths_rescue_{timestamp}.txt"
    
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
        # Open the output file with the timestamped filename
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            print_breaths(conn, exam_id, output_file)
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        error_message = ''.join(traceback.format_exception(None, e, e.__traceback__))
        print(f"Error: {e}")
        # Bring the message box to the foreground (doesn't work)
        MB_ICONHAND = 0x00000010
        MB_TOPMOST = 0x00040000
        MB_SETFOREGROUND = 0x00010000
        uType = MB_ICONHAND | MB_TOPMOST | MB_SETFOREGROUND
        ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "Script Error", uType)

