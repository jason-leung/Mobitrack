# This script inserts dummie data for mobitrack database.
# It already assumes that you have run createDatabase.py to create the database

import mysql.connector
import time
import uuid
import random

db = mysql.connector.connect (
		host="localhost",
		user="root", #yourusername
		passwd="password" #yourpw
	)

mycursor = db.cursor()

# Select the database to use
mycursor.execute("USE mobitrack")

# Create a random data and insert it into wearing_session db
sessionID = uuid.uuid4().hex[:16]
patientID = uuid.uuid4().hex[:8]
targetROM = random.randint(30, 45)
locationList = ["left-upper-arm","left-lower-arm","right-upper-arm","right-lower-arm","left-upper-leg","left-lower-leg","right-upper-leg","right-lower-leg"]
locationIndx = random.randint(0,len(locationList)-1)
location = locationList[locationIndx] 
timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
targetROM = random.randint(35,45)
sql = "INSERT INTO database_wearingsession (SessionID, PatientID, TargetROM, Location, TimeStamp) VALUES (%s, %s, %s, %s, %s)"
val = (sessionID, patientID, targetROM, location, timestamp)
mycursor.execute(sql, val)
db.commit()

# Create a dummie data and insert it into exercise_period db
# To mimic a realistic situation of having multiple exercise_period for each session, a random number will be generated from 1-5, which represents how many exercise_periods the specific session will have
numPeriods = random.randint(1,6)
for i in range(numPeriods):
	periodID = uuid.uuid4().hex[:8]
	duration = random.randint(50, 300) # Come back to this once the data type is decided
	repetitions = random.randint(10,21)
	periodTS = time.strftime('%Y-%m-%d %H:%M:%S')
	sql = "INSERT INTO database_exerciseperiod (PeriodID, PatientID, TargetROM, SessionID_id, Duration, Repetitions, Timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	val = (periodID, patientID, targetROM, sessionID, duration, repetitions, periodTS)
	mycursor.execute(sql, val)
	db.commit()
