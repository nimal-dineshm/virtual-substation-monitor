# run_all.py - Runs the full Virtual Substation Monitoring System

import threading
import time

from modbus_server.run_server import run_modbus_server
from logger.log_to_db import log_to_db
from ml_anomaly_detector.detect_anomaly import anomaly_detection

if __name__ == "__main__":
    print("[System] Starting Virtual Substation Monitoring System...")

    # Start Modbus server
    t1 = threading.Thread(target=run_modbus_server)
    t1.start()

    # Give server time to initialize
    time.sleep(2)

    # Start logger and ML threads
    t2 = threading.Thread(target=log_to_db)
    t3 = threading.Thread(target=anomaly_detection)

    t2.start()
    t3.start()

    # Keep main thread alive
    t1.join()
    t2.join()
    t3.join()
