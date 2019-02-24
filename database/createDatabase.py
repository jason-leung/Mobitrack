# This script create database and tables for mobitrack.

import mysql.connector

db = mysql.connector.connect (
		host="localhost",
		user="root", #yourusername
		passwd="password" #yourpw
	)


mycursor = db.cursor()

try:
	sql_Delete_query = """DROP DATABASE mobitrack"""
	mycursor.execute(sql_Delete_query)
	print ("mobitrack databse Deleted successfully ")
except:
	print ("mobitrack database did not originally exist ")

# Create database if it doesn't exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS mobitrack")
mycursor.execute("USE mobitrack")

# Create the wearing session table if it doesn't exist
mycursor.execute("CREATE TABLE IF NOT EXISTS database_wearingsession (" +
				 "SessionID VARCHAR(16) PRIMARY KEY NOT NULL, " +
				 "PatientID VARCHAR(8), " +
				 "Location VARCHAR(20), " + 
				 "TimeStamp TIMESTAMP ) " )
				 
# Create the exercise period table if it doesn't exist
mycursor.execute("CREATE TABLE IF NOT EXISTS database_exerciseperiod (" +
				 "PeriodID VARCHAR(8) PRIMARY KEY NOT NULL, " +
				 "SessionID VARCHAR(16), " +
				 "Duration VARCHAR(255), " +
				 "Repetitions VARCHAR(20), " + 
				 "TimeStamp TIMESTAMP )" )