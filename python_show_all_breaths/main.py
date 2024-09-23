import os
import sqlite3
import csv
from datetime import datetime


def get_db_path():
    app_data = os.getenv('APPDATA')
    if not app_data:
        raise Exception("APPDATA environment variable not found.")
    db_path = os.path.join(app_data, 'HermetoPascoal', 'db', 'vento-1.3.2.db')
    if not os.path.exists(db_path):
        raise Exception(f"Database file not found at {db_path}")
    return db_path


def get_all_breaths(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.exam_id, b.id as breath_id, bg.id as breath_gas_id, bg.created_at, bg.gas, bg.ppm
        FROM breaths b
        JOIN breath_gas bg ON b.id = bg.breath_id
        WHERE b.deleted_at IS NULL
        ORDER BY b.exam_id, b.id, bg.id
    """)
    return cursor.fetchall()


def get_gas_name(gas_id):
    if gas_id == 1:
        return "H2"
    elif gas_id == 2:
        return "CH4"
    else:
        return "unknown"


def export_to_csv(conn, output_filename):
    breaths = get_all_breaths(conn)

    if not breaths:
        print("No breath data found where deleted_at is NULL.")
        return

    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the headers
        csvwriter.writerow(['Exam ID', 'Breath ID', 'BreathGas ID', 'Created At', 'Gas', 'PPM'])

        for row in breaths:
            exam_id, breath_id, breath_gas_id, created_at, gas_id, ppm = row
            gas_name = get_gas_name(gas_id)
            csvwriter.writerow([exam_id, breath_id, breath_gas_id, created_at, gas_name, ppm])


def main():
    # Define the timestamp at the start of the script
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"all_breaths_{timestamp}.csv"

    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        export_to_csv(conn, output_filename)
        print(f"Data exported successfully to {output_filename}")
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback

        error_message = ''.join(traceback.format_exception(None, e, e.__traceback__))
        print(f"Error: {e}")
