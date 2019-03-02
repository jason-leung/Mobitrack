# metamotion imports
from __future__ import print_function
from ctypes import c_void_p, cast, POINTER
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
from time import sleep
import time
from threading import Event
from sys import argv
import os

# processing imports
import numpy as np
import matplotlib.pyplot as plt

# database imports
import mysql.connector
import time
import uuid

class Mobitrack:
    # constructor
    def __init__(self, mwAddress):
        # MetaWear
        self.mwAddress = mwAddress
        self.status = 0 # 0 = disconnected, 1 = connected
        self.mw_device = None
        self.mw_callback = None
        self.mw_processor = None
    
    def startTracking(self, patientID, wearLocation):
        return
    
    def stopTracking(self):
        return

    def mw_connect(self):
        self.mw = MetaWear(self.mwAddress)
        self.mw.connect()
        print("Connected to " + self.mwAddress)

    def mw_configure(self):
        libmetawear.mbl_mw_settings_set_connection_parameters(self.mw_device.board, 7.5, 7.5, 0, 6000)
        sleep(1.5)

        e = Event()

        def processor_created(context, pointer):
            self.processor = pointer
            e.set()

        fn_wrapper = cbindings.FnVoid_VoidP_VoidP(processor_created)

        acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.mw_device.board)
        gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.mw_device.board)

        signals = (c_void_p * 1)()
        signals[0] = gyro
        libmetawear.mbl_mw_dataprocessor_fuser_create(acc, signals, 1, None, fn_wrapper)
        e.wait()
        libmetawear.mbl_mw_datasignal_subscribe(self.mw_processor, None, self.mw_callback)

    def mw_start(self):
        libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.mw_device.board)
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.mw_device.board)

        libmetawear.mbl_mw_gyro_bmi160_start(self.mw_device.board)
        libmetawear.mbl_mw_acc_start(self.mw_device.board)

    def mw_reset(self):
        e = Event()
        self.mw_device.on_disconnect = lambda s: e.set()
        libmetawear.mbl_mw_debug_reset(self.mw_device.board)
        e.wait()


print("Jason is awesome")

m = Mobitrack("F7:83:98:15:21:07")
