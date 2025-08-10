# 📡 RFID-Based Attendance System using Raspberry Pi & MariaDB

## 📖 Overview
This project is an **RFID-based attendance tracking system** built around a **Raspberry Pi** and **MariaDB** database.  
It allows for automatic recording of attendance by scanning RFID cards/tags, storing details such as:
- User identity
- Time of check-in and check-out
- Attendance status (Present / Checked Out)

The system integrates **RFID hardware**, a **Python backend**, and a **MariaDB database** to provide a reliable, real-time attendance monitoring solution.

---

## 🛠 Components Used
- **Raspberry Pi 4B** 
- **RFID Reader Module** (e.g., RC522) connected via SPI
- **RFID Tags/Cards**
- **MariaDB** database server (installed on the Raspberry Pi)
- **Python 3** with required libraries:
  - `mfrc522` or `SimpleMFRC522` (for RFID)
  - `mysql.connector` or `pymysql` (for MariaDB access)
- **VS Code** with **Remote SSH** for development

---
### Software & Libraries
- **Raspberry Pi OS** (Bookworm/Bullseye)
- **MariaDB** (database backend)
- **Python 3**
- Python Libraries:
  - `mfrc522` (for RC522 reader)
  - `spidev`
  - `RPi.GPIO`
  - `mysql-connector-python` or `pymysql`

## 🗄 Database Structure (MariaDB)
Database Name: `attendance_db`

### 1️⃣ Users Table
Stores registered users and their RFID UIDs.

| Column      | Type         | Description                     |
|-------------|-------------|---------------------------------|
| user_id     | INT (PK, AI) | Unique ID for the user          |
| user_name   | VARCHAR      | Full name of the user           |
| rfid_uid    | BIGINT       | RFID UID linked to the user     |

**Example Data:**
| user_id | user_name      | rfid_uid       |
|---------|---------------|----------------|
| 1       | Alice Johnson | 123456789012   |
| 2       | Bob Smith     | 234567890123   |

Example entries:
```sql
INSERT INTO Users(user_name, rfid_uid) VALUES
('Alice Johnson', 123456789012),
('Charlie Brown', 345678901234),
('Bob Smith', 234567890123)
```

---

### 2️⃣ Attendance Table
Logs attendance events for users.

| Column        | Type         | Description                         |
|---------------|-------------|-------------------------------------|
| attendance_id | INT (PK, AI) | Unique ID for the attendance record |
| user_id       | INT (FK)     | Links to `Users.user_id`            |
| rfid_uid      | BIGINT       | UID of the scanned card             |
| date          | DATE         | Date of the record                  |
| time_in       | TIME         | Time when the user checked in       |
| time_out      | TIME         | Time when the user checked out      |
| status        | VARCHAR      | "Present" / "Checked Out"           |

---
