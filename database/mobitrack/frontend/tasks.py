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
def startTracking(self, macAddress, location, patientID):
    m = Mobitrack()
    m.data_folder = "/home/jason/git/Mobitrack/data"
    m.patientID = patientID
    m.wearLocation = location
    device = MetaWear(macAddress)
    state = State(device, m)

    try:
        # Create lock file
        lock_folder = "/home/jason/git/Mobitrack/lock"
        if not os.path.exists(lock_folder):
            os.mkdir(lock_folder)
        lock_file = os.path.join(lock_folder, macAddress + "_lock.txt")
        if os.path.isfile(lock_file):
            raise ValueError('Device %s already in use' % (macAddress) )

        # Connect to device
        self.update_state(state='CONNECTING')
        print("Connecting to " + macAddress)
        device.connect()

        print("Configuring %s" % (macAddress))
        state.setup()

        print("Connected to " + macAddress)
        self.update_state(state='CONNECTED')

        # Create lock file
        if not os.path.isfile(lock_file):
            with open(lock_file, 'x'):
                os.utime(lock_file, None)

        print('Starting wearing session for patient %s on device %s' % (patientID, macAddress))
        state.start()

        while(os.path.isfile(lock_file)):
            pass

        self.update_state(state='DISCONNECTING')
        print("Disconnecting device")

        m.endSession()
        m.writeData()
        m.plotData()

        time.sleep(100)

        event = Event()

        state.device.on_disconnect = lambda s: event.set()
        libmetawear.mbl_mw_debug_reset(state.device.board)
        event.wait()

        self.update_state(state='DISCONNECTED')
        print("Disconnected")
    except:
        self.update_state(state='DISCONNECTING')

        print("Disconnecting device")
        event = Event()

        state.device.on_disconnect = lambda s: event.set()
        libmetawear.mbl_mw_debug_reset(state.device.board)
        event.wait()

        self.update_state(state='DISCONNECTED')
        print("Disconnected")
    return 1

@task(bind=True)
def stopTracking(self, macAddress):
    lock_folder = "/home/jason/git/Mobitrack/lock"
    lock_file = os.path.join(lock_folder, macAddress + "_lock.txt")

    try:
        if os.path.isfile(lock_file):
            os.remove(lock_file)
    except:
        print("Error removing lock file:", lock_file)
    return