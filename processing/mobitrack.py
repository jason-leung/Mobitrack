import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Mobitrack:
    # contructor for initialize fields
    def __init__(self):
        
        # variable initialization
        self.rawData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.smoothData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.data = np.empty((0,3)) # time, pitch, roll
        self.numSamplesSeen = 0
        
        # storage variables
        self.rawDataStorageWindowSize = 60 * 60 * 100 # store 60 minutes of data @ 100 Hz
        self.dataStorageWindowSize = 60 * 60 * 100 # store 60 minutes of data @ 100 Hz
        self.eventStorageWindowSize = 60 * 60 * 100
        
        # calibration
        self.calibrationG = 9.81
        self.calibrationAsens = 1
        self.calibrationGsens = 1
        
        # preprocessing
        self.smoothWindowSize = 50 # window size for moving average filter
        self.complementaryFilterAlpha = 0.1
        
        # peak detection
        self.last_pk = -1
        self.peaks = np.empty(0,dtype=int)
        self.valleys = np.empty(0,dtype=int)
        self.segments = np.empty(0,dtype=int)
        self.reps = np.empty(0,dtype=int)
        
        # segmentation
        self.segmentWindow = 100
        self.segmentMinPkDist = 15
        self.segmentPkThr = 0.5
        self.segmentMaxPk2PkDist = 20000
        
        # rep detection
        self.minROM = 40
        
    def processStep(self, data):
        # validate data
        if(len(data) != 7):
            print("Invalid data!")
            return
        
        # calibrate data
        if self.numSamplesSeen >= self.rawDataStorageWindowSize:
            self.rawData = self.rawData[1:]
        self.rawData = np.vstack((self.rawData, self.calibrateData(data)))
        
        # smooth data
        if self.numSamplesSeen >= self.rawDataStorageWindowSize:
            self.smoothData = self.smoothData[1:]
        self.smoothData = np.vstack((self.smoothData, self.preprocessData()))
        
        # compute angles
        if self.numSamplesSeen >= self.dataStorageWindowSize:
            self.data = self.data[1:]
        self.data = np.vstack((self.data, self.computeRotationAngles()))
        
        # peak detection
        isPeak = self.detectPeaks()
        if isPeak == 1:
            if len(self.peaks) == self.eventStorageWindowSize:
                self.peaks = self.peaks[1:]
            self.peaks = np.append(self.peaks, self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int))
            self.last_pk = self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int)
        elif isPeak == -1:
            if len(self.valleys) == self.eventStorageWindowSize:
                self.valleys = self.valleys[1:]
            self.valleys = np.append(self.valleys, self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int))
            self.last_pk = self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int)
        
        # detect segments
        isSegment = self.detectSegment()
        if isSegment != -1:
            if len(self.segments) == self.eventStorageWindowSize:
                self.segments = self.segments[1:]
            self.segments = np.append(self.segments, isSegment)
        
        # detect segments
        isRep = self.detectRepetition()
        if isRep != -1:
            if len(self.reps) == self.eventStorageWindowSize:
                self.reps = self.reps[1:]
            self.reps = np.append(self.reps, isRep)
            print("Index: ", i, "Repetition Detected!")
        
        # increment numSamplesSeen
        self.numSamplesSeen += 1
    
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
            smoothData[i] = np.mean(self.rawData[startSumIdx:,i])
        return smoothData
    
    def computeRotationAngles(self):
        # compute pitch and roll using complementary filter
        
        # initialize variables
        data = self.smoothData[-1,:]
        angle_est = np.zeros(3)
        angle_est[0] = data[0]
        
        # estimate pitch and roll based on acceleration
        pitch_est_acc = np.rad2deg(np.arctan2(data[2], np.sqrt(data[1]**2 + data[3]**2))) # range [-90, 90]
        roll_est_acc = np.rad2deg(np.arctan2(data[1], np.sqrt(data[2]**2 + data[3]**2))) # range [-90, 90]
        
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
        center_idx = len(pitch) - np.round(self.segmentWindow/2).astype(int)
        center = pitch[center_idx]
        
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
        if len(self.peaks) >= 2 and len(self.valleys) >= 1:
            if self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int) == self.peaks[-1]:
                if self.peaks[-2] > self.valleys[-1] > self.peaks[-2]:
                    if (self.peaks[-1] - self.peaks[-2]) <= self.segmentMaxPk2PkDist:
                        return self.peaks[-1]
        return -1
    
    def detectRepetition(self):
        # repetition detection, returns index if rep found, -1 otherwise
        if len(self.peaks) >= 2 and len(self.valleys) >= 1:
            if self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int) == self.peaks[-1]:
                ROM_f = self.data[self.peaks[-1]] - self.data[self.valleys[-1]]
                ROM_b = self.data[self.peaks[-2]] - self.data[self.valleys[-1]]
                if np.min(ROM_f, ROM_b) >= self.minROM:
                    return self.peaks[-1]
        return -1
    
    def plotData(self):
        plt.plot(self.data[:,0], self.data[:,1] , label='Pitch')
        plt.plot(self.data[:,0], self.data[:,2], label='Roll')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Angle')
        plt.legend()
        plt.show()

    def plotRawData(self):
        plt.plot(self.rawData[:,0], self.rawData[:,1], label='ax')
        plt.plot(self.rawData[:,0], self.rawData[:,2], label='ay')
        plt.plot(self.rawData[:,0], self.rawData[:,3], label='az')
        plt.plot(self.rawData[:,0], self.rawData[:,4], label='gx')
        plt.plot(self.rawData[:,0], self.rawData[:,5], label='gy')
        plt.plot(self.rawData[:,0], self.rawData[:,6], label='gz')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Raw IMU Readings (a in m/s^2, g in rad/s)')
        plt.legend()
        plt.show()
        
    def plotSmoothData(self):
        plt.plot(self.smoothData[:,0], self.smoothData[:,1], label='ax')
        plt.plot(self.smoothData[:,0], self.smoothData[:,2], label='ay')
        plt.plot(self.smoothData[:,0], self.smoothData[:,3], label='az')
        plt.plot(self.smoothData[:,0], self.smoothData[:,4], label='gx')
        plt.plot(self.smoothData[:,0], self.smoothData[:,5], label='gy')
        plt.plot(self.smoothData[:,0], self.smoothData[:,6], label='gz')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Smoothed IMU Readings (a in m/s^2, g in rad/s)')
        plt.legend()
        plt.show()


m = Mobitrack()

filename = '/home/jason/Downloads/Jan25_AndreaSOP_Left/data_wrist_full.txt'
data = pd.read_csv(filename).values
data[:,0] = (data[:,0] - data[0,0]) / 1000

for i in range(data.shape[0]):
    m.processStep(data[i,:])

m.plotData()
m.plotRawData()
m.plotSmoothData()
