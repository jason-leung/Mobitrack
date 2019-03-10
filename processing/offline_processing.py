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
is_legacy_data = True

# data_dir = '../data/2019-03-07'
# data_dir = '/home/jason/git/Mobitrack/data/2019-03-09/45_degree_device_on_back'
data_dir = r'C:\Users\andre\OneDrive\School\FYDP\Mobitrack\data\Mobitrack\data\2019-03-07'
files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.endswith('.txt')]
print(files,"\n")

for f in files:
	# f = 'a_specific_file'
	# f = '/home/jason/git/Mobitrack/data/2019-03-09/45_degree_device_on_side/1552174093304_left-upper-arm.txt'
	f = r'C:\Users\andre\OneDrive\School\FYDP\Mobitrack\data\Mobitrack\data\2019-03-07\1551994890698_left-lower-leg.txt'
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

	m = Mobitrack()
	m.patientID = 00000000
	# m.smoothWindowSize = m.frequency * 1
	# m.complementaryFilterAlpha = 1

	# If data was calibrated before saving, uncalibrate it. This ensures that the mobitrack.py class does not require any direct changes
	if is_legacy_data:
		data = uncalibrateData(data, m)

	# set wear location
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

	m.plotData()
	m.plotRawData()
	m.plotSmoothData()
	m.writeData()

	m.clear()
	break
