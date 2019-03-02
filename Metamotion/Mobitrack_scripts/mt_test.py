# mbientlabs
from __future__ import print_function
from ctypes import c_void_p, cast, POINTER
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
from threading import Event
from sys import argv
import os

# threading
import logging
import threading
import time
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

# mobitrack
import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd
from datetime import datetime

filename = "test_01.txt"
data_folder_name = "../../data/"+datetime.today().strftime('%Y-%m-%d')

# classes
class Mobitrack:
    # constructor
    def __init__(self):
        
        # variable initialization
        self.rawData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.smoothData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.data = np.empty((0,3)) # time, pitch, roll
        self.numSamplesSeen = 0
        
        # storage variables
        self.frequency = 100 # Hz
        self.rawDataStorageWindowSize = 60 * 60 * self.frequency # store 60 minutes of data
        self.dataStorageWindowSize = 60 * 60 * self.frequency # store 60 minutes of data
        self.eventStorageWindowSize = 60 * 60 * self.frequency
        
        # calibration
        self.calibrationG = 9.81
        self.calibrationAsens = 1
        self.calibrationGsens = 1
        
        # preprocessing
        self.smoothWindowSize = self.frequency * 0.5 # window size for moving average filter (seconds)
        self.complementaryFilterAlpha = 0.1
        
        # peak detection
        self.last_pk = -1
        self.peaks = np.empty(0,dtype=int)
        self.valleys = np.empty(0,dtype=int)
        self.segments = np.empty(0,dtype=int)
        self.reps = np.empty(0,dtype=int)
        
        # segmentation
        self.segmentWindow = self.frequency * 1 # seconds
        self.segmentMinPkDist = self.frequency * 0.5
        self.segmentPkThr = 0.5
        self.segmentMaxPk2PkDist = self.frequency * 200 # seconds
        self.wearLocation = 'RA' # RA, LA, RL, LL
        
        # rep detection
        self.minROM = 40
        
        # exercise detection
        self.minRepsPerMin = 5
        self.minExerciseDuration = 5 # seconds
#         self.minExerciseRepSeparationTime = self.minExerciseDuration / self.minRepsPerMin # seconds
        self.minExerciseRepSeparationTime = 5 # seconds
        self.currentExercisePeriodNumReps = 0
        self.currentExercisePeriodStartIdx = -1
        
    def processStep(self, data):
        # validate data
        if(len(data) != 7):
            print("Invalid data!")
            return
        
        # calibrate data
        if self.numSamplesSeen >= self.rawDataStorageWindowSize:
            self.rawData = np.copy(self.rawData[1:])
        self.rawData = np.vstack((self.rawData, self.calibrateData(data)))
        
        # smooth data
        if self.numSamplesSeen >= self.rawDataStorageWindowSize:
            self.smoothData = np.copy(self.smoothData[1:])
        self.smoothData = np.vstack((self.smoothData, self.preprocessData()))
        
        # compute angles
        if self.numSamplesSeen >= self.dataStorageWindowSize:
            self.data = np.copy(self.data[1:])
        self.data = np.vstack((self.data, self.computeRotationAngles()))
        
        # peak detection
        isPeak = self.detectPeaks()
        
        if isPeak == 1:
            if len(self.peaks) == self.eventStorageWindowSize:
                self.peaks = np.copy(self.peaks[1:])
            self.peaks = np.append(self.peaks, self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int))
            self.last_pk = self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int)
        elif isPeak == -1:
            if len(self.valleys) == self.eventStorageWindowSize:
                self.valleys = np.copy(self.valleys[1:])
            self.valleys = np.append(self.valleys, self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int))
            self.last_pk = self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int)
        
        # detect segments
        isSegment = -1
        if isPeak != 0: isSegment = self.detectSegment()
        if isSegment != -1:
            if len(self.segments) == self.eventStorageWindowSize:
                self.segments = np.copy(self.segments[1:])
            self.segments = np.append(self.segments, isSegment)
        
        # detect repetitions
        isRep = -1
        if isSegment != -1: isRep = self.detectRepetition()
        if isRep != -1:
            if len(self.reps) == self.eventStorageWindowSize:
                self.reps = np.copy(self.reps[1:])
            self.reps = np.append(self.reps, isRep)
            print("idx:", isRep, " - Repetition Detected!")
            
        # detect exercise periods
        if isRep != -1:
            if self.currentExercisePeriodNumReps == 0:
                self.currentExercisePeriodStartIdx = self.reps[-1]
            self.currentExercisePeriodNumReps += 1
        
        if self.currentExercisePeriodNumReps > 0 and len(self.reps) > 0:
            if (isRep == -1 and self.numSamplesSeen >= self.reps[-1] + self.minExerciseRepSeparationTime * self.frequency + np.round(self.segmentWindow/2).astype(int)):
                self.endSession()
        
        # increment numSamplesSeen
        self.numSamplesSeen += 1
    
    def endSession(self):
        if self.currentExercisePeriodNumReps > 0 and len(self.reps) > 0:
            duration = (self.reps[-1] - self.currentExercisePeriodStartIdx) / self.frequency
            repsPerMin = 0
            if duration > 0: repsPerMin = self.currentExercisePeriodNumReps / (duration / 60.0)
            if duration >= self.minExerciseDuration and self.currentExercisePeriodNumReps >= self.minRepsPerMin and repsPerMin > self.minRepsPerMin:
                exercisePeriodStats = {
                    "timestamp": datetime.utcfromtimestamp(self.data[self.currentExercisePeriodStartIdx, 0]).strftime('%Y-%m-%d %H:%M:%S'),
                    "numReps": self.currentExercisePeriodNumReps,
                    "duration": duration
                }
                print("Exericse Period Detected:", exercisePeriodStats)

            self.currentExercisePeriodNumReps = 0
        return
    
    def calibrateData(self, data):
        # calibrate data by dividing by sensitivity
        data[1:4] = data[1:4] / self.calibrationAsens * self.calibrationG
        data[4:7] = data[4:7] / self.calibrationGsens
        return data
    
    def preprocessData(self):
        # smooth data with a moving average for specified window size
        smoothData = np.copy(self.rawData[-1,:])
            
        startSumIdx = 0
        if self.numSamplesSeen >= self.smoothWindowSize:
            startSumIdx = -self.smoothWindowSize
        
        for i in range(1,7):
            smoothData[i] = np.mean(self.rawData[int(startSumIdx):,i])
        return smoothData
    
    def computeRotationAngles(self):
        # compute pitch and roll using complementary filter
        
        # initialize variables
        data = self.smoothData[-1,:]
        angle_est = np.zeros(3)
        angle_est[0] = data[0]
        
        # estimate pitch and roll based on acceleration
        pitch_est_acc = np.rad2deg(np.arctan2(data[1], np.sqrt(data[2]**2 + data[3]**2))) # range [-90, 90]
        roll_est_acc = np.rad2deg(np.arctan2(data[2], np.sqrt(data[1]**2 + data[3]**2))) # range [-90, 90]
        
        # use acceleration data only for first sample
        if(self.numSamplesSeen == 0):
            angle_est[1] = pitch_est_acc
            angle_est[2] = roll_est_acc
        # use complementary filter otherwise
        else:
            # estimate pitch and roll based on gyroscope
            dt = self.smoothData[-1,0] - self.smoothData[-2,0]
            pitch_est_gyr = self.data[-1,1] + dt * data[4]
            roll_est_gyr = self.data[-1,2] + dt * data[5]
            
            # complementary filter
            angle_est[1] = (1-self.complementaryFilterAlpha) * pitch_est_gyr + self.complementaryFilterAlpha * pitch_est_acc
            angle_est[2] = (1-self.complementaryFilterAlpha) * roll_est_gyr + self.complementaryFilterAlpha * roll_est_acc
        
        return angle_est
    
    def detectPeaks(self):
        # peak detection, returns 1 if peak, -1 if valley, and 0 otherwise
        
        # check if enough samples
        if self.numSamplesSeen < self.segmentWindow: return 0
        
        # find center point
        pitch = self.data[-self.segmentWindow:,1]
        center_idx = self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int)
        center = pitch[np.round(self.segmentWindow/2).astype(int)]
        
        # check for min dist
        if (self.last_pk == -1) or (center_idx - self.last_pk) >= self.segmentMinPkDist:
            # check if max or min
            if center == np.max(pitch) and (center - np.min(pitch)) >= self.segmentPkThr:
                return 1
            elif center == np.min(pitch) and (np.max(pitch) - center) >= self.segmentPkThr:
                return -1
        return 0
    
    def detectSegment(self):
        # segment detection, returns index if segment found, -1 otherwise
        if self.wearLocation == 'RA' or self.wearLocation == 'LA':
            if len(self.peaks) >= 2 and len(self.valleys) >= 1:
                if self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int) == self.peaks[-1]:
                    if self.peaks[-1] > self.valleys[-1] and self.valleys[-1] > self.peaks[-2]:
                        if (self.peaks[-1] - self.peaks[-2]) <= self.segmentMaxPk2PkDist:
                            return self.peaks[-1]
        elif self.wearLocation == 'RL' or self.wearLocation == 'LL':
            if len(self.peaks) >= 1 and len(self.valleys) >= 2:
                if self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int) == self.valleys[-1]:
                    if self.valleys[-1] > self.peaks[-1] and self.peaks[-1] > self.valleys[-2]:
                        if (self.valleys[-1] - self.valleys[-2]) <= self.segmentMaxPk2PkDist:
                            return self.valleys[-1]
        return -1
    
    def detectRepetition(self):
        # repetition detection, returns index if rep found, -1 otherwise
        if self.wearLocation == 'RA' or self.wearLocation == 'LA':
            if len(self.peaks) >= 2 and len(self.valleys) >= 1:
                if self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int) == self.peaks[-1]:
                    ROM_f = self.data[self.peaks[-1],1] - self.data[self.valleys[-1],1]
                    ROM_b = self.data[self.peaks[-2],1] - self.data[self.valleys[-1],1]
                    print("ROM:", round(min(ROM_f, ROM_b), 2))
                    if min(ROM_f, ROM_b) >= self.minROM:
                        return self.peaks[-1]
        elif self.wearLocation == 'RL' or self.wearLocation == 'LL':
            if len(self.peaks) >= 1 and len(self.valleys) >= 2:
                if self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int) == self.valleys[-1]:
                    ROM_f = self.data[self.peaks[-1],1] - self.data[self.valleys[-1],1]
                    ROM_b = self.data[self.peaks[-1],1] - self.data[self.valleys[-2],1]
                    print("ROM:", round(min(ROM_f, ROM_b), 2))
                    if min(ROM_f, ROM_b) >= self.minROM:
                        return self.peaks[-1]
        return -1
    
    def plotData(self):
        plt.figure(figsize=(20,10))
        
        plt.plot(self.data[:,0], self.data[:,1] , label='Pitch')
        plt.plot(self.data[:,0], self.data[:,2], label='Roll')
        
        plt.plot(self.data[self.peaks,0], self.data[self.peaks,1], 'yx', label='Peaks')
        plt.plot(self.data[self.valleys,0], self.data[self.valleys,1], 'mx', label='Valleys')
        plt.plot(self.data[self.reps,0], self.data[self.reps,1], 'g.', label='Reps')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Angle')
        plt.legend()
        
        plt.savefig((data_folder_name+filename).replace('.txt', '.png'))
        
        plt.show()

    def plotRawData(self):
        plt.figure(figsize=(20,10))
        
        plt.plot(self.rawData[:,0], self.rawData[:,1], label='ax')
        plt.plot(self.rawData[:,0], self.rawData[:,2], label='ay')
        plt.plot(self.rawData[:,0], self.rawData[:,3], label='az')
        plt.plot(self.rawData[:,0], self.rawData[:,4], label='gx')
        plt.plot(self.rawData[:,0], self.rawData[:,5], label='gy')
        plt.plot(self.rawData[:,0], self.rawData[:,6], label='gz')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Raw IMU Readings (a in m/s^2, g in rad/s)')
        plt.legend()
        
        plt.savefig((data_folder_name+filename).replace('.txt', '_raw.png'))
        
        plt.show()
        
    def plotSmoothData(self):
        plt.figure(figsize=(20,10))
        plt.plot(self.smoothData[:,0], self.smoothData[:,1], label='ax')
        plt.plot(self.smoothData[:,0], self.smoothData[:,2], label='ay')
        plt.plot(self.smoothData[:,0], self.smoothData[:,3], label='az')
        plt.plot(self.smoothData[:,0], self.smoothData[:,4], label='gx')
        plt.plot(self.smoothData[:,0], self.smoothData[:,5], label='gy')
        plt.plot(self.smoothData[:,0], self.smoothData[:,6], label='gz')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Smoothed IMU Readings (a in m/s^2, g in rad/s)')
        plt.legend()
        
        plt.savefig((data_folder_name+filename).replace('.txt', '_smooth.png'))
        
        plt.show()
        
    def clear(self):
        # variable initialization
        self.rawData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.smoothData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.data = np.empty((0,3)) # time, pitch, roll
        self.numSamplesSeen = 0
        
        # peak detection
        self.last_pk = -1
        self.peaks = np.empty(0,dtype=int)
        self.valleys = np.empty(0,dtype=int)
        self.segments = np.empty(0,dtype=int)
        self.reps = np.empty(0,dtype=int)

# global variables
mobitrack_status = False
states = []
sensor_data = []
m = Mobitrack()

class State:
  def __init__(self, device):
      self.device = device
      self.callback = cbindings.FnVoid_VoidP_DataP(self.data_handler)
      self.processor = None

  def data_handler(self, ctx, data):
      values = parse_value(data, n_elem=2)
      time_stamp = data.contents.epoch
      data_current = [time_stamp, values[0].x, values[0].y, values[0].z, values[1].x, values[1].y, values[1].z]
      sensor_data.append("%d,%f,%f,%f,%f,%f,%f" % (time_stamp,  values[0].x, values[0].y, values[0].z, values[1].x, values[1].y, values[1].z))
      m.processStep(np.array([time_stamp / 1000,  values[0].x, values[0].y, values[0].z, values[1].x, values[1].y, values[1].z]))

  def setup(self):
      libmetawear.mbl_mw_settings_set_connection_parameters(self.device.board, 7.5, 7.5, 0, 6000)
      time.sleep(1.5)

      e = Event()

      def processor_created(context, pointer):
          self.processor = pointer
          e.set()

      fn_wrapper = cbindings.FnVoid_VoidP_VoidP(processor_created)

      acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.device.board)
      gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.device.board)

      signals = (c_void_p * 1)()
      signals[0] = gyro
      libmetawear.mbl_mw_dataprocessor_fuser_create(acc, signals, 1, None, fn_wrapper)
      e.wait()
      libmetawear.mbl_mw_datasignal_subscribe(self.processor, None, self.callback)

  def start(self):
      libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.device.board)
      libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.device.board)

      libmetawear.mbl_mw_gyro_bmi160_start(self.device.board)
      libmetawear.mbl_mw_acc_start(self.device.board)


def mobitrack_connect(e):
  global mobitrack_status
  global states
  global sensor_data
  last_mobitrack_status = False
  logging.debug('Connecting to Mobitrack...')
  
  while(True):
    # starting session
    if(last_mobitrack_status == False and mobitrack_status == True):
      logging.debug('Starting Mobitrack Session...')

      d = MetaWear("F7:83:98:15:21:07")
      d.connect()
      print("Connected to " + d.address)
      states.append(State(d))

      for s in states:
          print("Configuring %s" % (s.device.address))
          s.setup()

      for s in states:
          s.start()

    # during session
    # while(mobitrack_status):
      # logging.debug('processStep()')
      # last_mobitrack_status = True
      # time.sleep(0.5)

    # end session
    if(last_mobitrack_status == True and mobitrack_status == False):
      logging.debug('endSession()')
      m.endSession()
      m.plotData()
      m.clear()
      print("Resetting devices")
      events = []
      for s in states:
          e = Event()
          events.append(e)

          s.device.on_disconnect = lambda s: e.set()
          libmetawear.mbl_mw_debug_reset(s.device.board)

      for e in events:
          e.wait()


      if not os.path.exists(data_folder_name):
          os.mkdir(data_folder_name)
          print("Directory " , data_folder_name ,  " created ")
      else:
          print("Directory " , data_folder_name ,  " already exists")

      #print(sensor_data)
      # Log data to file
      with open(os.path.join(data_folder_name, 'data_' + filename), 'w') as f:
          print(filename)
          f.write('timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z\n')
          f.write('\n'.join(sensor_data))

    last_mobitrack_status = mobitrack_status
    time.sleep(0.5)


def mobitrack_controller(e):
  global mobitrack_status
  logging.debug('Starting Mobitrack controller...')

  while(True):
    user_input = input()
    if(user_input == '0'):
      mobitrack_status = False
      # print("Setting Status:", user_input)
    elif(user_input == '1'):
      mobitrack_status = True
      # print("Setting Status:", user_input)

e = threading.Event()

t1 = threading.Thread(name='Mobitrack', target=mobitrack_connect, args=(e,))
t2 = threading.Thread(name='Controller', target=mobitrack_controller, args=(e,))

t1.start()
t2.start()
print("Enter Mobitrack Status (0 = off, 1 = on):")
