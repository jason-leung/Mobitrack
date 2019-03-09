from mobitrack import Mobitrack

import os
import numpy as np

# data_dir = '../data/2019-03-07'
data_dir = '/home/jason/git/Mobitrack/data/test'
files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.endswith('.txt')]
print(files,"\n")

for f in files:
	# f = 'a_specific_file'
	# f = '/home/jason/git/Mobitrack/data/MetaMotion/data_20190309-test2.txt'
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

	# print(data.shape)
	data[:,0] = data[:,0] / 1000

	m = Mobitrack()
	m.patientID = 00000000
	m.complementaryFilterAlpha = 1

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
		m.processStep(data[i,:])

	m.endSession()

	m.plotData()
	m.plotRawData()
	#     m.plotSmoothData()
	m.clear()
	# break
