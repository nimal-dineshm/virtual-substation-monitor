# modbus_server/run_server.py

from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import threading
import logging
import time
import random

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def run_modbus_server():
    # Define Modbus data blocks (di, co, hr, ir)
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, [0]*100),
        ir=ModbusSequentialDataBlock(0, [0]*100)
    )
    context = ModbusServerContext(slaves=store, single=True)

    # Identification
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'VirtualSubstation'
    identity.ProductCode = 'VS'
    identity.VendorUrl = 'http://example.com'
    identity.ProductName = 'SubstationMonitor'
    identity.ModelName = 'VSv1'
    identity.MajorMinorRevision = '1.0'

    # Function to update holding registers every 2 seconds
    def updating_writer():
        while True:
            voltage = random.randint(220, 250)
            fault = random.randint(0, 1)
            context[0x00].setValues(3, 0, [voltage, fault])  # Write to holding registers 0,1
            print(f"[Modbus Server] Voltage={voltage}V | Fault={fault}")
            time.sleep(2)

    thread = threading.Thread(target=updating_writer)
    thread.start()

    # Start Modbus TCP server on localhost:5020
    StartTcpServer(context, identity=identity, address=("localhost", 5020))
