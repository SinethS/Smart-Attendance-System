import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
from datetime import datetime

def read_rfid():
    reader = SimpleMFRC522()
    try:
        print("Scan your RFID card...")
        rfid_uid, _ = reader.read()  # Read RFID UID
        print(f"Card ID: {rfid_uid}")
        return rfid_uid
    finally:
        GPIO.cleanup()

# Database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hdssj2003#",
    database="attendancesystem"
)
cursor = db_connection.cursor()

# Read RFID card ID
rfid_uid = read_rfid()

# Step 1: Get user_id and user_name from the `users` table using `rfid_uid`
cursor.execute("SELECT id, user_name FROM users WHERE rfid_uid = %s", (rfid_uid,))
user = cursor.fetchone()

if user is None:
    print("RFID not registered.")
    reg = input("Do you want to register this RFID? (y/n): ").strip().lower()
    if reg == "y":
        user_name = input("Enter your name: ").strip()
        
        if not user_name:
            print("Invalid name. Registration canceled.")
        else:
            cursor.execute(
                "INSERT INTO users (user_name, rfid_uid) VALUES (%s, %s)",
                (user_name, rfid_uid)
            )
            db_connection.commit()
            print(f"RFID registered for {user_name}.")
else:
    user_id, user_name = user  # Extract user details
    print(f"User found: {user_name} (ID: {user_id})")

    # Step 2: Check if there's an attendance record for today
    cursor.execute(
        "SELECT attendance_id, time_out FROM attendance WHERE user_id = %s AND date = CURDATE() ORDER BY attendance_id DESC LIMIT 1",
        (user_id,)
    )
    attendance_record = cursor.fetchone()

    if attendance_record is None:
        # No entry for today → New check-in
        cursor.execute(
            "INSERT INTO attendance (user_id, rfid_uid, date, time_in, status) VALUES (%s, %s, CURDATE(), CURTIME(), 'Present')",
            (user_id, rfid_uid)
        )
        db_connection.commit()
        print(f"{user_name} checked in.")
    else:
        attendance_id, time_out = attendance_record
        if time_out is None:
            # User is still checked in → Update time_out
            cursor.execute(
                "UPDATE attendance SET time_out = CURTIME(), status = 'Checked out' WHERE attendance_id = %s",
                (attendance_id,)
            )
            db_connection.commit()
            print(f"{user_name} checked out.")
        else:
            # User already checked out → New check-in record
            cursor.execute(
                "INSERT INTO attendance (user_id, rfid_uid, date, time_in, status) VALUES (%s, %s, CURDATE(), CURTIME(), 'Present')",
                (user_id, rfid_uid)
            )
            db_connection.commit()
            print(f"{user_name} checked in again.")

# Close the database connection
cursor.close()
db_connection.close()




