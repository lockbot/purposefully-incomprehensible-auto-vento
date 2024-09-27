import os
import sqlite3
import ctypes
import uuid
from datetime import datetime


def cleanup_excess_breaths():
    """
    Deletes breaths beyond the 100th for each exam (actual delete, not soft delete).
    If any breaths are deleted, displays a message to the user in English and Spanish.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        breaths_deleted = False  # Flag to check if any breaths were deleted

        # Get all exam_ids
        cursor.execute("SELECT id FROM exams")
        exam_ids = [row[0] for row in cursor.fetchall()]

        for exam_id in exam_ids:
            # Replace exam.s_uuid with 00000000-0000-0000-0000-000000000000
            cursor.execute("""
                UPDATE exams
                SET s_uuid = '00000000-0000-0000-0000-000000000000'
                WHERE id = ?
            """, (exam_id,))
            conn.commit()
            # Get breath IDs for this exam_id ordered by id
            cursor.execute("""
                SELECT id
                FROM breaths
                WHERE exam_id = ?
                ORDER BY id
            """, (exam_id,))
            breaths = cursor.fetchall()
            breath_ids = [row[0] for row in breaths]
            num_breaths = len(breath_ids)

            if num_breaths > 100:
                # Delete breaths beyond the 100th
                excess_breath_ids = breath_ids[100:]  # breaths after the first 100
                placeholders = ','.join('?' for _ in excess_breath_ids)
                # Delete from breath_gas
                cursor.execute(f"""
                    DELETE FROM breath_gas
                    WHERE breath_id IN ({placeholders})
                """, excess_breath_ids)
                # Delete from breaths
                cursor.execute(f"""
                    DELETE FROM breaths
                    WHERE id IN ({placeholders})
                """, excess_breath_ids)
                breaths_deleted = True  # Set the flag
                conn.commit()
        if breaths_deleted:
            # Display message to user in English and Spanish
            message = ("Because you over-used the same exam in previous tests, "
                       "we have deleted some breaths. If you have the CSV for these, "
                       "use that to document it, but we really have to do it to avoid breaking the application.\n\n"
                       "Debido a que ha utilizado en exceso el mismo examen en pruebas anteriores, "
                       "hemos eliminado algunas respiraciones. Si tiene el CSV de estos datos, "
                       "utilícelo para documentarlo, pero realmente tenemos que hacerlo para evitar que la aplicación falle.")
            ctypes.windll.user32.MessageBoxW(0, message, "Breaths Deleted", 0)
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, str(e), "Error", 0)
        print(f"Error in cleanup_excess_breaths: {e}")
        raise e
    finally:
        conn.close()


def get_db_path():
    """Get the path to the SQLite database."""
    app_data = os.getenv('APPDATA')
    if not app_data:
        raise Exception("APPDATA environment variable not found.")
    db_path = os.path.join(app_data, 'HermetoPascoal', 'db', 'vento-1.3.2.db')
    if not os.path.exists(db_path):
        raise Exception(f"Database file not found at {db_path}")
    return db_path


def copy_last_exam():
    """Copy the last exam in the 'exams' table using SQL, modifying necessary fields."""

    # Connect to the SQLite database
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Fetch the last exam based on the maximum 'id'
        cursor.execute("SELECT id FROM exams WHERE deleted_at IS NULL ORDER BY id DESC LIMIT 1")
        last_exam = cursor.fetchone()

        if not last_exam:
            ctypes.windll.user32.MessageBoxW(0, "No exams found in the 'exams' table.", "Error", 0)
            raise Exception("No exams found in the 'exams' table.")

        last_exam_id = last_exam[0]

        # Generate new UUIDs and timestamps
        new_uuid = str(uuid.uuid4())
        new_s_uuid = '00000000-0000-0000-0000-000000000000'
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Copy the last exam using SQL, and update only necessary fields (uuid, s_uuid, timestamps)
        cursor.execute("""
            INSERT INTO exams (
                uuid, s_uuid, created_at, updated_at, date_time_start,
                exam_data, patient_uuid, patient_s_uuid, exam_preset_uuid, 
                user_uuid, user_s_uuid
            )
            SELECT
                ?, ?, ?, ?, ?, 
                jsonb(exam_data), patient_uuid, patient_s_uuid, exam_preset_uuid, 
                user_uuid, user_s_uuid
            FROM exams
            WHERE id = ?
            """, (new_uuid, new_s_uuid, current_timestamp, current_timestamp, current_timestamp, last_exam_id))

        conn.commit()

        print("Successfully copied the last exam and inserted a new one.")

    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, str(e), "Error", 0)
        print(f"Error in copying last exam: {e}")
        raise

    finally:
        # Clean up database resources
        cursor.close()
        conn.close()
