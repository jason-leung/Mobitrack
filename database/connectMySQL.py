import mysql.connector

db = mysql.connector.connect (
		host="localhost",
		user="root", # Your username
		passwd="" # Your pw
	)

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS mobitrack")
mycursor.execute("USE mobitrack")

mycursor.execute("CREATE TABLE IF NOT EXISTS wearing_session (" +
				 "SessionID VARCHAR(16), " +
				 "PatientID VARCHAR(255), " +
				 "Location VARCHAR(20), " + 
				 "TimeStamp DATE )")
mycursor.execute("CREATE TABLE IF NOT EXISTS exercise_period (" +
				 "PeriodID VARCHAR(16), " +
				 "SessionID VARCHAR(16), " +
				 "Duration VARCHAR(255), " +
				 "Repetitions VARCHAR(20), " + 
				 "TimeStamp DATE )")