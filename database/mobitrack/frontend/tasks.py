from __future__ import print_function
from ctypes import c_void_p, cast, POINTER
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
from mbientlab.metawear.cbindings import *
from threading import Event
from sys import argv
import os

from frontend.mobitrack import Mobitrack
from frontend.metawear_state import State

from celery.utils.log import get_task_logger
from celery import task

from pathlib import Path
from time import sleep


logger = get_task_logger(__name__)

@task(bind=True)
def startTrackingMock(self, macAddress, location, patientID, led_on, target_angle):
    path_MAC = macAddress.replace(":", "-")
    m = Mobitrack()
    m.data_folder = os.path.join(Path(os.path.dirname( __file__ )).parents[2], "data")
    m.patientID = patientID
    m.wearLocation = location

    fake_states = ['CONNECTED', 'CONNECTING', 'DISCONNECTING', 'ANDREA']

    try:
        print("in try")
        # Create lock file
        lock_folder = os.path.join(Path(os.path.dirname( __file__ )).parents[2], "lock")
        if not os.path.exists(lock_folder):
            os.mkdir(lock_folder)
        lock_file = os.path.join(lock_folder, path_MAC + "_lock.txt")
        if os.path.isfile(lock_file):
            raise ValueError('Device %s already in use' % (macAddress) )

        print("making file")
        print("task id: " + self.request.id)

        # Create lock file
        if not os.path.isfile(lock_file):
            with open(lock_file, 'w') as f:
                f.write(self.request.id)

        print("made file")


        # Mock some random state changes
        i = 0
        print("above while")
        while(os.path.isfile(lock_file)):
            print("in while")
            sleep(2)
            new_state = fake_states[i]
            print(new_state)
            self.update_state(state=new_state)
            i = i + 1
            if (i == len(fake_states)):
                i = 0

    except (Exception, ArithmeticError) as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
        print("Exception occured: ")
        return 0
        
    return 1



@task(bind=True)
def startTracking(self, macAddress, location, patientID, led_on, target_angle):
    path_MAC = macAddress.replace(":", "-")
    m = Mobitrack()
    m.data_folder = os.path.join(Path(os.path.dirname( __file__ )).parents[2], "data")
    m.patientID = patientID
    m.wearLocation = location

    minROM_slack = 5
    m.minROM = target_angle - minROM_slack
    if m.minROM <= 5.:
        min.ROM = 5.
    if m.minROM >= 120.:
        min.ROM = 120.
    device = MetaWear(macAddress)
    state = State(device, m)
    state.led = led_on

    try:
        # Create lock file
        lock_folder = os.path.join(Path(os.path.dirname( __file__ )).parents[2], "lock")
        if not os.path.exists(lock_folder):
            os.mkdir(lock_folder)
        lock_file = os.path.join(lock_folder, path_MAC + "_lock.txt")
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
        m.plotDataGyro()

        state.stop()

        event = Event()

        state.device.on_disconnect = lambda s: event.set()
        libmetawear.mbl_mw_debug_reset(state.device.board)
        event.wait()

        self.update_state(state='DISCONNECTED')
        print("Disconnected")
    except (Exception, ArithmeticError) as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
        print("Exception occured: ")
        
        self.update_state(state='DISCONNECTING')
        state.stop()

        print("Disconnecting device")
        event = Event()

        state.device.on_disconnect = lambda s: event.set()
        libmetawear.mbl_mw_debug_reset(state.device.board)
        event.wait()

        stopTracking(macAddress)

        self.update_state(state='DISCONNECTED')
        print("Disconnected")
    return 1

@task(bind=True)
def stopTracking(self, macAddress):
    path_MAC = macAddress.replace(":", "-")
    lock_folder = os.path.join(Path(os.path.dirname( __file__ )).parents[2], "lock")
    lock_file = os.path.join(lock_folder, path_MAC + "_lock.txt")

    try:
        if os.path.isfile(lock_file):
            os.remove(lock_file)
    except:
        print("Error removing lock file:", lock_file)
    return