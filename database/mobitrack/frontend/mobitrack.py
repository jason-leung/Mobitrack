# mobitrack
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import math

import mysql.connector
import uuid
import random

class Mobitrack:
    # constructor
    def __init__(self):
        
        # variable initialization
        self.rawData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.calibratedData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.smoothData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.data_accel = np.empty((0,3)) # time, pitch, roll
        self.data_gyro = np.empty((0,3)) # time, pitch, roll
        self.data_compl = np.empty((0,3)) # time, pitch, roll

        self.numSamplesSeen = 0
        self.data_folder = ""
        
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
        self.complementaryFilterAlpha = 0.9 # 1 is accel
        self.max_allowed_acceleration = 0.2
        
        # peak detection
        self.last_pk = -1
        self.peaks = np.empty(0,dtype=int)
        self.valleys = np.empty(0,dtype=int)
        self.pkvl = np.empty(0,dtype=int)
        self.segments = np.empty(0,dtype=int)
        self.reps = np.empty(0,dtype=int)
        
        # segmentation
        self.segmentWindow = self.frequency * 1 # seconds
        self.segmentMinPkDist = self.frequency * 0.5
        self.segmentPkThr = 0.5
        self.segmentMaxPk2PkDist = self.frequency * 200 # seconds
        self.wearLocation = 'right-lower-arm'
        
        # rep detection
        self.last_pkvl_is_rep = False
        self.minROM = 40
        self.cross_thresh = 15 # degrees
        
        # exercise detection
        self.minRepsPerMin = 5
        self.minExerciseDuration = 5 # seconds
        self.minExerciseRepSeparationTime = 5 # seconds
        self.currentExercisePeriodNumReps = 0
        self.currentExercisePeriodStartIdx = -1

        # database
        self.db = {
            "host": "localhost",
            "user": "root", #yourusername
            "passwd": "password" #yourpw
        }
        self.patientID = ""
        self.sessionID = uuid.uuid4().hex[:16]

        
    def processStep(self, data):
        status = {
            "valid": False,
            "isPeak": 0,
            "isRep": -1
        }

        # validate data
        if(len(data) != 7):
            print("Invalid data!")
            return status
        status["valid"] = True

        # get raw data
        if self.numSamplesSeen >= self.rawDataStorageWindowSize:
            self.rawData = np.copy(self.rawData[1:])
        self.rawData = np.vstack((self.rawData, data))
        
        # calibrate data
        if self.numSamplesSeen >= self.rawDataStorageWindowSize:
            self.calibratedData = np.copy(self.calibratedData[1:])
        self.calibratedData = np.vstack((self.calibratedData, self.calibrateData(data)))

        # smooth data
        if self.numSamplesSeen >= self.rawDataStorageWindowSize:
            self.smoothData = np.copy(self.smoothData[1:])
        self.smoothData = np.vstack((self.smoothData, self.preprocessData()))
        
        # compute angles
        if self.numSamplesSeen >= self.dataStorageWindowSize:
            self.data_accel = np.copy(self.data_accel[1:])
            self.data_gyro = np.copy(self.data_gyro[1:])
        rotAngles = self.computeRotationAngles()
        self.data_accel = np.vstack((self.data_accel, rotAngles['accel']))
        self.data_gyro = np.vstack((self.data_gyro, rotAngles['gyro']))
        self.data_compl = np.vstack((self.data_compl, rotAngles['compl']))
        
        # peak detection
        isPeak = self.detectPeaks()
        status["isPeak"] = isPeak
        
        if isPeak == 1:
            if len(self.peaks) == self.eventStorageWindowSize:
                self.peaks = np.copy(self.peaks[1:])
            if len(self.pkvl) == self.eventStorageWindowSize:
                self.pkvl = np.copy(self.pkvl[1:])
            self.peaks = np.append(self.peaks, self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int))
            self.pkvl = np.append(self.pkvl, self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int))
            self.last_pk = self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int)
        elif isPeak == -1:
            if len(self.valleys) == self.eventStorageWindowSize:
                self.valleys = np.copy(self.valleys[1:])
            if len(self.pkvl) == self.eventStorageWindowSize:
                self.pkvl = np.copy(self.pkvl[1:])
            self.valleys = np.append(self.valleys, self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int))
            self.pkvl = np.append(self.pkvl, self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int))
            self.last_pk = self.numSamplesSeen - np.round(self.segmentWindow/2).astype(int)
        
        # detect repetitions
        isRep = -1
        if isPeak == 1 or isPeak == -1: isRep = self.detectRepetition()
        status["isRep"] = isRep
        if isRep != -1:
            if len(self.reps) == self.eventStorageWindowSize:
                self.reps = np.copy(self.reps[1:])
            self.reps = np.append(self.reps, isRep)
            print("Repetition Detected!")
            
        # detect exercise periods
        if isRep != -1:
            if self.currentExercisePeriodNumReps == 0:
                self.currentExercisePeriodStartIdx = self.reps[-1]
            self.currentExercisePeriodNumReps += 1
        
        if self.currentExercisePeriodNumReps > 0 and len(self.reps) > 0:
            if (isRep == -1 and self.numSamplesSeen >= self.reps[-1] + self.minExerciseRepSeparationTime * self.frequency + np.round(self.segmentWindow/2).astype(int)):
                self.endPeriod()
        
        # increment numSamplesSeen
        self.numSamplesSeen += 1

        return status
    
    def endPeriod(self):
        exercisePeriodStats = {"timestamp": datetime.utcfromtimestamp(self.data_accel[self.currentExercisePeriodStartIdx, 0]).strftime('%Y-%m-%d %H:%M:%S')}
        if self.currentExercisePeriodNumReps > 0 and len(self.reps) > 0:
            duration = (self.reps[-1] - self.currentExercisePeriodStartIdx) / self.frequency
            repsPerMin = 0
            if duration > 0: repsPerMin = self.currentExercisePeriodNumReps / (duration / 60.0)
            if duration >= self.minExerciseDuration and self.currentExercisePeriodNumReps >= self.minRepsPerMin and repsPerMin > self.minRepsPerMin:
                exercisePeriodStats = {
                    "timestamp": datetime.utcfromtimestamp(self.data_accel[self.currentExercisePeriodStartIdx, 0]).strftime('%Y-%m-%d %H:%M:%S'),
                    "numReps": self.currentExercisePeriodNumReps,
                    "duration": int(duration)
                }

                # write exercise period to database
                print("Exericse Period Detected:", exercisePeriodStats)
                
                try:
                    print("Writing exercise period to database")
                    db = mysql.connector.connect (
                        host=self.db['host'],
                        user=self.db['user'], #yourusername
                        passwd=self.db['passwd'] #yourpw
                    )
                    mycursor = db.cursor()
                    mycursor.execute("USE mobitrack")
                    sql = "INSERT INTO database_exerciseperiod (PeriodID, PatientID, SessionID_id, Duration, Repetitions, Timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
                    periodID = uuid.uuid4().hex[:8]
                    val = (periodID, self.patientID, self.sessionID, int(exercisePeriodStats['duration']), exercisePeriodStats['numReps'], exercisePeriodStats['timestamp'])
                    mycursor.execute(sql, val)
                    db.commit()
                    mycursor.close()
                    db.close()
                    print("Exercise period successfully written to database")
                except (Exception, ArithmeticError) as e:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(e).__name__, e.args)
                    print(message)
                    print("Exception occured: Error when writing exercise period to database")
            self.currentExercisePeriodNumReps = 0
        return exercisePeriodStats

    def endSession(self):
        exercisePeriodStats = self.endPeriod()

        # write wearing session to database
        try:
            print("Writing wearing session to database")
            db = mysql.connector.connect (
                host=self.db['host'],
                user=self.db['user'], #yourusername
                passwd=self.db['passwd'] #yourpw
            )
            mycursor = db.cursor()
            mycursor.execute("USE mobitrack")
            sql = "INSERT INTO database_wearingsession (SessionID, PatientID, Location, TimeStamp) VALUES (%s, %s, %s, %s)"
            val = (self.sessionID, self.patientID, self.wearLocation, exercisePeriodStats['timestamp'])
            mycursor.execute(sql, val)
            db.commit()
            mycursor.close()
            db.close()
            print("Wearing session successfully written to database")
        except (Exception, ArithmeticError) as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)
            print("Exception occured: Error when writing wearing session to database")

        # generate new session ID
        self.sessionID = uuid.uuid4().hex[:16]

        return
    
    def calibrateData(self, data):
        # calibrate data by dividing by sensitivity
        data[1:4] = data[1:4] / self.calibrationAsens * self.calibrationG
        data[4:7] = data[4:7] / self.calibrationGsens
        return data
    
    def preprocessData(self):
        # smooth data with a moving average for specified window size
        smoothData = np.copy(self.calibratedData[-1,:])
            
        startSumIdx = 0
        if self.numSamplesSeen >= self.smoothWindowSize:
            startSumIdx = -self.smoothWindowSize
        
        for i in range(1,7):
            smoothData[i] = np.mean(self.calibratedData[int(startSumIdx):,i])
        return smoothData
    
    def computeRotationAngles(self):
        # compute pitch and roll using complementary filter

        angle_est = {}
        
        # initialize variables
        data = self.smoothData[-1,:]
        angle_est['accel'] = np.zeros(3)
        angle_est['gyro'] = np.zeros(3)
        angle_est['compl'] = np.zeros(3)
        angle_est['accel'][0] = data[0]
        angle_est['gyro'][0] = data[0]
        angle_est['compl'][0] = data[0]

        sum_accel = abs(data[1]) + abs(data[2]) + abs(data[3]) - self.calibrationG
        sum_accel = abs(math.sqrt((data[1])**2 + abs(data[2])**2 + abs(data[3])**2) - self.calibrationG)
        
        # estimate pitch and roll based on acceleration
        pitch_est_acc = np.rad2deg(np.arctan2(data[1], np.sqrt(data[2]**2 + data[3]**2))) # range [-90, 90]
        roll_est_acc = np.rad2deg(np.arctan2(data[2], np.sqrt(data[1]**2 + data[3]**2))) # range [-90, 90]

        angle_est['accel'][1] = pitch_est_acc
        angle_est['accel'][2] = roll_est_acc
        
        # estimate pitch and roll data based on gyroscope
        # use acceleration data only for first sample
        if(self.numSamplesSeen == 0):
            angle_est['gyro'][1] = pitch_est_acc
            angle_est['gyro'][2] = roll_est_acc
        else:
            dt = self.smoothData[-1,0] - self.smoothData[-2,0]
            pitch_est_gyr = self.data_gyro[-1,1] + dt * data[5]
            roll_est_gyr = self.data_gyro[-1,2] + dt * data[4]

            angle_est['gyro'][1] = pitch_est_gyr
            angle_est['gyro'][2] = roll_est_gyr

            pitch_for_compl_gyro_est = self.data_compl[-1,1] + dt * data[5]
            roll_for_compl_gyro_est = self.data_compl[-1,2] + dt * data[4]

            # If the acceleration can't be trusted because of extreme motion, use the gyro
            if(sum_accel > self.max_allowed_acceleration*self.calibrationG):
                angle_est['compl'][1] = pitch_for_compl_gyro_est
                angle_est['compl'][2] = roll_for_compl_gyro_est
            else:
                # acceleration is acceptable so use the complementary filter
                angle_est['compl'][1] = (1-self.complementaryFilterAlpha) * pitch_for_compl_gyro_est + self.complementaryFilterAlpha * pitch_est_acc
                angle_est['compl'][2] = (1-self.complementaryFilterAlpha) * roll_for_compl_gyro_est + self.complementaryFilterAlpha * roll_est_acc
            
    
        return angle_est
    
    def detectPeaks(self):
        # peak detection, returns 1 if peak, -1 if valley, and 0 otherwise
        
        # check if enough samples
        if self.numSamplesSeen < self.segmentWindow: return 0
        
        # find center point
        pitch = self.data_gyro[-self.segmentWindow:,1]
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

    def getOpening(self, data):
        # takes first half of data
        # returns 1 if open down, -1 if open up
        
        data_min = min(data)
        data_max = max(data)

        if data[0] >= data[-1]:
            if abs(data_min - data[-1]) >= self.cross_thresh:
                print("pattern 5")
                return -1
            else:
                if abs(data_max - data[0]) <= self.cross_thresh:
                    print("pattern 4")
                    return -1
                else:
                    print("pattern 3")
                    return 1
        else:
            if abs(data_max - data[-1]) >= self.cross_thresh:
                print("pattern 2")
                return 1
            else:
                if abs(data_min - data[0]) <= self.cross_thresh:
                    print("pattern 1")
                    return 1
                else:
                    print("pattern 6")
                    return -1

        return 0

    def detectRepetition(self):
        # repetition detection, returns index if rep found, -1 otherwise
        if "arm" in self.wearLocation or "leg" in self.wearLocation:
            if len(self.pkvl) >= 3:

                if not self.last_pkvl_is_rep:
                    last_pkvls = self.pkvl[-3:]
                    last_pkvls_pitch = self.data_compl[last_pkvls, 1]

                    # calculate ROM
                    ROM, ROM_f, ROM_b = 0, 0, 0
                    segment_mean = np.mean(self.data_compl[last_pkvls[0]:last_pkvls[2], 1])
                    crossover_angle = 90. if segment_mean >= 0 else -90.
                    print("crossover_angle:", crossover_angle)
                    # open up
                    if( self.getOpening(self.data_compl[last_pkvls[0]:last_pkvls[1], 1]) == -1):
                        crossover_pt1 = min(self.data_compl[last_pkvls[0]:last_pkvls[1], 1])
                        crossover_pt2 = min(self.data_compl[last_pkvls[1]:last_pkvls[2], 1])
                        crossover_amt1 = abs(crossover_pt1 - last_pkvls_pitch[1])
                        crossover_amt2 = abs(crossover_pt2 - last_pkvls_pitch[1])
                        if crossover_amt1 >= self.cross_thresh:
                            ROM_f = abs(last_pkvls_pitch[0] - crossover_angle) + abs(last_pkvls_pitch[1] - crossover_angle)
                        else:
                            ROM_f = abs(last_pkvls_pitch[0] - last_pkvls_pitch[1])
                        if crossover_amt2 >= self.cross_thresh:
                            ROM_b = abs(last_pkvls_pitch[2] - crossover_angle) + abs(last_pkvls_pitch[1] - crossover_angle)
                        else:
                            ROM_b = abs(last_pkvls_pitch[2] - last_pkvls_pitch[1])
                    # open down
                    elif( self.getOpening(self.data_compl[last_pkvls[0]:last_pkvls[1], 1]) == 1 ):
                        crossover_pt1 = max(self.data_compl[last_pkvls[0]:last_pkvls[1], 1])
                        crossover_pt2 = max(self.data_compl[last_pkvls[1]:last_pkvls[2], 1])
                        crossover_amt1 = abs(crossover_pt1  - last_pkvls_pitch[1])
                        crossover_amt2 = abs(crossover_pt2 - last_pkvls_pitch[1])
                        if crossover_amt1 >= self.cross_thresh:
                            ROM_f = abs(last_pkvls_pitch[0] - crossover_angle) + abs(last_pkvls_pitch[1] - crossover_angle)
                        else:

                            ROM_f = abs(last_pkvls_pitch[0] - last_pkvls_pitch[1])
                        if crossover_amt2 >= self.cross_thresh:

                            ROM_b = abs(last_pkvls_pitch[2] - crossover_angle) + abs(last_pkvls_pitch[1] - crossover_angle)
                        else:

                            ROM_b = abs(last_pkvls_pitch[2] - last_pkvls_pitch[1])
                        
                    ROM = min(ROM_f, ROM_b)
                    ROM_max = max(ROM_f, ROM_b)


                    if ROM >= self.minROM:
                        self.last_pkvl_is_rep = True
                        print("ROM_rep:", round(ROM, 2))
                        return self.pkvl[-1]
                self.last_pkvl_is_rep = False
        return -1
    
    def plotData(self):
        plt.figure(figsize=(20,10))
        
        plt.plot(self.data_accel[:,0], self.data_accel[:,1] , label='Pitch')
        plt.plot(self.data_accel[:,0], self.data_accel[:,2], label='Roll')
        
        plt.plot(self.data_accel[self.peaks,0], self.data_accel[self.peaks,1], 'yx', label='Peaks')
        plt.plot(self.data_accel[self.valleys,0], self.data_accel[self.valleys,1], 'mx', label='Valleys')
        plt.plot(self.data_accel[self.reps,0], self.data_accel[self.reps,1], 'g.', label='Reps')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Angle')
        plt.legend()
        
        data_dir = os.path.join(self.data_folder, datetime.today().strftime('%Y-%m-%d'))
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("Directory " , data_dir ,  " created ")
        else:
            print("Directory " , data_dir ,  " already exists")
        plt.savefig(os.path.join(data_dir, str(int(self.data_accel[0,0])) + "_" + self.wearLocation + ".png"))
        
        plt.show()

    def plotDataGyro(self):
        plt.figure(figsize=(20,10))
        
        plt.plot(self.data_gyro[:,0], self.data_gyro[:,1] , label='Pitch')
        plt.plot(self.data_gyro[:,0], self.data_gyro[:,2], label='Roll')
        
        plt.plot(self.data_gyro[self.peaks,0], self.data_gyro[self.peaks,1], 'yx', label='Peaks')
        plt.plot(self.data_gyro[self.valleys,0], self.data_gyro[self.valleys,1], 'mx', label='Valleys')
        plt.plot(self.data_gyro[self.reps,0], self.data_gyro[self.reps,1], 'g.', label='Reps')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Angle')
        plt.legend()
        
        data_dir = os.path.join(self.data_folder, datetime.today().strftime('%Y-%m-%d'))
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("Directory " , data_dir ,  " created ")
        else:
            print("Directory " , data_dir ,  " already exists")
        plt.savefig(os.path.join(data_dir, str(int(self.data_gyro[0,0])) + "_" + self.wearLocation + "_gyro.png"))
        
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
        plt.ylabel('Raw IMU Readings (a in g, g in deg/s)')
        plt.legend()
        
        data_dir = os.path.join(self.data_folder, datetime.today().strftime('%Y-%m-%d'))
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("Directory " , data_dir ,  " created ")
        else:
            print("Directory " , data_dir ,  " already exists")
        plt.savefig(os.path.join(data_dir, str(int(self.data_accel[0,0])) + "_" + self.wearLocation + "_raw.png"))
        
        # plt.show()
        
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
        
        data_dir = os.path.join(self.data_folder, datetime.today().strftime('%Y-%m-%d'))
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("Directory " , data_dir ,  " created ")
        else:
            print("Directory " , data_dir ,  " already exists")
        plt.savefig(os.path.join(data_dir, str(int(self.data_accel[0,0])) + "_" + self.wearLocation + "_smooth.png"))
        
        # plt.show()

    def writeData(self):
        data_dir = os.path.join(self.data_folder, datetime.today().strftime('%Y-%m-%d'))
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("Directory " , data_dir ,  " created ")
        else:
            print("Directory " , data_dir ,  " already exists")

        # Log data to file
        np.savetxt(os.path.join(data_dir, str(int(self.data_accel[0,0])) + "_" + self.wearLocation + ".txt"), self.rawData, delimiter=',', header='timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z')

    def clear(self):
        # variable initialization
        self.rawData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.smoothData = np.empty((0,7)) # time, ax, ay, az, gx, gy, gz
        self.data_accel = np.empty((0,3)) # time, pitch, roll
        self.data_gyro = np.empty((0,3)) # time, pitch, roll
        self.numSamplesSeen = 0
        
        # peak detection
        self.last_pk = -1
        self.peaks = np.empty(0,dtype=int)
        self.valleys = np.empty(0,dtype=int)
        self.pkvl = np.empty(0,dtype=int)
        self.segments = np.empty(0,dtype=int)
        self.reps = np.empty(0,dtype=int)
        self.last_pkvl_is_rep = False

        # database
        self.sessionID = uuid.uuid4().hex[:16]