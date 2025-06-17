# logger/log_to_db.py

import sqlite3
import time
from pymodbus.client.sync import ModbusTcpClient

def log_to_db():
    # Connect to or create the SQLite database
    conn = sqlite3.connect('database/substation_data.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            timestamp TEXT,
            voltage INTEGER,
            fault INTEGER
        )
    ''')
    conn.commit()

    # Connect to Modbus server running on localhost
    client = ModbusTcpClient('localhost', port=5020)
    client.connect()

    print("[Logger] Connected to Modbus server")

    while True:
        # Read 2 holding registers starting at address 0
        rr = client.read_holding_registers(0, 2, unit=1)
        if rr.isError():
            print("[Logger] Modbus read error")
            time.sleep
