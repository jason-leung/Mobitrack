from mobitrack import Mobitrack

import os
import numpy as np

def uncalibrateData(data, m):
	uncalibrated_data = np.copy(data)
	uncalibrated_data[:,0] = uncalibrated_data[:,0]
	
	uncalibrated_data[:, 1:4] = uncalibrated_data[:, 1:4] * m.calibrationAsens / m.calibrationG
	uncalibrated_data[:, 4:7] = uncalibrated_data[:, 4:7] * m.calibrationGsens

	return uncalibrated_data


# Data collected prior to March 9 was calibrated before being saved 
is_legacy_data = False

# data_dir = '../data/2019-03-07'
# data_dir = '/home/jason/git/Mobitrack/data/2019-03-11/accuracy_test_1hz'
# data_dir = '/home/jason/git/Mobitrack/data/2019-03-12/accuracy_0.5hz'
# data_dir = '/home/jason/git/Mobitrack/data/2019-03-12/left_wrist_withandwithout_crossing'
# data_dir = '/home/jason/git/Mobitrack/data/2019-03-12/left_arm_withandwithout_crossing'
# data_dir = '/home/jason/git/Mobitrack/data/2019-03-12/upper_leg_withandwithout_crossing'
# data_dir = '/home/jason/git/Mobitrack/data/2019-03-12/lower_leg_withandwithout_crossing'
data_dir = "/home/jason/Downloads/SOP"

# data_dir = r'C:\Users\andre\OneDrive\School\FYDP\Mobitrack\data\Mobitrack\data\2019-03-07'
files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.endswith('.txt')]
# print(files,"\n")

for f in files:
	# f = 'a_specific_file'
	# f = '/home/jason/git/Mobitrack/data/2019-03-09/45_degree_device_on_side/1552174093304_left-upper-arm.txt'
	# f = r'C:\Users\andre\OneDrive\School\FYDP\Mobitrack\data\Mobitrack\data\2019-03-07\1551994890698_left-lower-leg.txt')
	# f = '/home/jason/git/Mobitrack/data/2019-03-10/1552233366_left-upper-arm.txt'
	# f = '/home/jason/git/Mobitrack/data/2019-03-10/1552234125_left-upper-arm.txt'
	# f = '/home/jason/git/Mobitrack/data/2019-03-10/1552235791_acctest_right_lower_leg.txt'
	# f = '/home/jason/git/Mobitrack/data/2019-03-10/1552269366_left-lower-arm.txt'
	# f = '/home/jason/git/Mobitrack/data/2019-03-10/1552272081_left-upper-arm.txt'
	# f = '/home/jason/git/Mobitrack/data/2019-03-12/accuracy_0.5hz/1552366961_left-upper-arm.txt' # used for poster

	f = '/home/jason/git/Mobitrack/data/2019-03-12/left_wrist_withandwithout_crossing/1552374404_left-upper-arm.txt'

	# data = pd.read_csv(f).values
	csv_data = np.genfromtxt(f, dtype=float, delimiter=',', names=True)
	data = np.empty((csv_data['timestamp'].shape[0], 7))
	data[:,0] = csv_data['timestamp']
	data[:,1] = csv_data['accel_x']
	data[:,2] = csv_data['accel_y']
	data[:,3] = csv_data['accel_z']
	data[:,4] = csv_data['gyro_x']
	data[:,5] = csv_data['gyro_y']
	data[:,6] = csv_data['gyro_z']

	# data[:,0] = data[:,0] / 1000.

	# # for poster
	# data = data[12300:,:]
	data[:,0] = data[:,0] - data[0,0]

	m = Mobitrack()
	m.patientID = 00000000



	# m.smoothWindowSize = m.frequency * 1
	# m.complementaryFilterAlpha = 1
	# m.complementaryFilterAlpha = 0
	# m.smoothWindowSize = m.frequency * 0.5
	# m.segmentMinPkDist = m.frequency * 0.4
	# m.cross_thresh = 10 # degrees
	# m.complementaryFilterAlpha = 1

	# If data was calibrated before saving, uncalibrate it. This ensures that the mobitrack.py class does not require any direct changes
	# if is_legacy_data:
		# data = uncalibrateData(data, m)

	# set wear location
	m.wearLocation = 'left-lower-arm'
	if 'left-lower-arm' in f:
		m.wearLocation = 'left-lower-arm'
	elif 'left-upper-arm' in f:
		m.wearLocation = 'left-upper-arm'
	elif 'left-lower-leg' in f:
		m.wearLocation = 'left-lower-leg'
	elif 'left-upper-leg' in f:
		m.wearLocation = 'left-upper-leg'
	elif 'right-lower-arm' in f:
		m.wearLocation = 'right-lower-arm'
	elif 'right-upper-arm' in f:
		m.wearLocation = 'right-upper-arm'
	elif 'right-lower-leg' in f:
		m.wearLocation = 'right-lower-leg'
	elif 'right-upper-leg' in f:
		m.wearLocation = 'right-upper-leg'

	print(f)
	for i in range(data.shape[0]):
		# print(data[i,:])
		m.processStep(data[i,:])

	m.endSession()

	# m.wearLocation = 'accuracy_test_05hz'

	# m.plotData()
	# m.plotDataPretty()
	# m.plotDataGyro()
	# m.plotRawDataBoth()
	# m.plotSmoothDataBoth()
	# m.plotSmoothData()
	# m.plotSmoothData_accel()
	# m.plotSmoothData_gyro()
	# m.writeData()
	m.plotDataAccel()
	m.plotDataGyro()
	m.plotRawData()
	m.plotSmoothData()

	# print(m.pkvl)
	print(m.reps.shape)

	m.clear()

	break

