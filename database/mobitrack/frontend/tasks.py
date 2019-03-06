from __future__ import print_function
from ctypes import c_void_p, cast, POINTER
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
from threading import Event
from sys import argv
import os

from frontend.mobitrack import Mobitrack
from frontend.metawear_state import State

from celery.utils.log import get_task_logger
from celery import task


logger = get_task_logger(__name__)

@task(bind=True)
def stopTracking(self, mac_address):
    sleep(7)
    return True

m = Mobitrack()
m.data_folder = "/home/jason/git/Mobitrack/data"
status = {}

@task(bind=True)
def startTracking(self, macAddress, location, patientID):
    device = MetaWear(macAddress)
    m.clear()
    global status
    status[macAddress] = "PENDING"

    try:
        self.update_state(state='CONNECTING')
        status[macAddress] = "CONNECTING"
        print("Connecting to " + macAddress)
        device.connect()
        state = State(device, m)

        print("Configuring %s" % (macAddress))
        state.setup()

        print("Connected to " + macAddress)
        self.update_state(state='CONNECTED')
        status[macAddress] = "CONNECTED"


        print('Starting wearing session for patient %s on device %s' % (patientID, macAddress))
        state.start()

        while(status[macAddress] == 'CONNECTED'):
            pass

        m.endSession()
        m.plotData()
        m.writeData()
        m.clear()

        self.update_state(state='DISCONNECTING')
        status[macAddress] = "DISCONNECTING"

        print("Disconnecting device")
        event = Event()

        state.device.on_disconnect = lambda s: event.set()
        libmetawear.mbl_mw_debug_reset(state.device.board)
        event.wait()

        self.update_state(state='DISCONNECTED')
        status[macAddress] = "DISCONNECTED"
    except:
        self.update_state(state='DISCONNECTED')
        status[macAddress] = "DISCONNECTED"
    return 1

@task(bind=True)
def stopTracking(self, macAddress):
    global status
    status[macAddress] = "DISCONNECTED"
    return