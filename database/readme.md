# This folder is for managing codes relevent to database of Mobitrack

The following documentation contains information regards to design choices made related to database & required packages.

1. Choice of Database: 

For Mobitrack, MySQL is used due to multiple reasons
- Offers default schema reinforcement: We want the data to have all the fields completed when we insert the data into the database
- Open source & widely supported (big community): Offers good community support, easily adaptable to different developing environment
- high availability (every request receives a response about whether it succeeded or not) & high consistency (all database has latest successful transaction updated) due to the quality of rdbms (relational database management system)
	
2. System Requirements:
- Check requirements.txt

3. Procedure (WIP)
- Follow the below order to achieve a functional database that you can interact through web application or terminal
	0 Install root pip packages
		- install mysql connector and virtualenv pip packages
		- pip install -r requirements_1.txt
	1 Run 'createDatabase.py' to create the database and the tables. If the database already exists, it will be dropped first
		- python createDatabase.py
	2 Create virtualenv under './mobitrack' folder & activate
		- virtualenv env
		- (To activate) source env/bin/activate (on windows .\env\Scripts\activate.ps1)
		- (To deactivate) deactivate
	3 Install all the required packages in virtualenv (i.e. pip)
		- pip install -r requirements.txt (This should only be run once the virtualenv is activated)
	3.5 Install npm
		- sudo apt install npm
		- npm install
	4 (Whenever applicable) Launch the development server
		- npm run build
		- python manage.py runserver
	5 Run 'insertMockData.py' to generate data for both tables; each run adds 1 row to wearing session table and 1-5 exercise period table
		- python insertMockData.py
	6 If there is any change made in schema for the table (MySQL), follow the below procedure:
		- Log in to mysql & drop the affected table(s)
		- Update the django about the changes
			- python manage.py makemigrations database
			- python manage.py migrate
		- Ensure that the changes aren't affecting the application side of things
	7 You can see the table contents through logging into admin
	8 You can see the table-formatted contents based on the sessionID by using following address
		- http://127.0.0.1:8000/database/sessionID/
		- ex: http://127.0.0.1:8000/database/e8495e1e36ba48b7/
	9 Entering http://127.0.0.1:8000/ will hit the homepage
	10 Entering http://127.0.0.1:8000/wearingsession will hit the wearing session page
	11 Search function is implemented under "All wearing session page"
		- The behaviour is that whenever there is a change made inside a search bar, the query will be made to populate the corresponding database. If the query text is null, all exercise periods will be populated instead.	
	12 (TODO) Export into csv format
			

4. Lauching Celery Service
	- Install rabbitMQ and start service
	- Start celery worker service
		- cd Mobitrack/database/mobitrack
		- celery -A mobitrack worker -l info
