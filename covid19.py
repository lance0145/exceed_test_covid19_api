#imports
import time
import datetime
from datetime import datetime, date, timedelta
import csv
import requests
import json
import sqlite3

def print_header(header):
	print('\n')
	print(*header, sep='|')
	print('----------------------------------------------------------------------------------------------------------------------------------')

def get_data():
	response = requests.get("https://coronavirus-19-api.herokuapp.com/countries")
	obj = json.loads(response.text)
	for o in obj:
		date_of_robot_run = date.today().strftime("%Y.%m.%d")
		country = o["country"]
		cases = o["cases"]
		todayCases = o["todayCases"]
		deaths = o["deaths"]
		todayDeaths = o["todayDeaths"]
		recovered = o["recovered"]
		active = o["active"]
		critical = o["critical"]
		casesPerOneMillion = o["casesPerOneMillion"]
		deathsPerOneMillion = o["deathsPerOneMillion"]
		totalTests = o["totalTests"]
		testsPerOneMillion = o["testsPerOneMillion"]      
		time_now = datetime.now().time()
		print(date_of_robot_run, time_now.strftime("%H:%M:%S"), country, cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion, deathsPerOneMillion, totalTests, testsPerOneMillion, sep='|')
		write_csv(date_of_robot_run, time_now.strftime("%H:%M:%S"), country, cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion, deathsPerOneMillion, totalTests, testsPerOneMillion)
		write_db(date_of_robot_run, time_now.strftime("%H:%M:%S"), country, cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion, deathsPerOneMillion, totalTests, testsPerOneMillion)

def write_csv(date_of_robot_run, time_of_scrape, country, cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion, deathsPerOneMillion, totalTests, testsPerOneMillion):
	with open('covid19_{}.csv'.format(date.today().strftime("%Y.%m.%d")), 'a+', encoding='utf-8') as f:
		csv_writer = csv.DictWriter(f, delimiter='|', fieldnames=header)
		csv_writer.writerow({'date_of_robot_run': date_of_robot_run, 'time_of_scrape': time_of_scrape, 'country': country, 'cases': cases,
			'todayCases': todayCases, 'deaths': deaths, 'todayDeaths': todayDeaths, 'recovered': recovered, 'active': active, 'critical': critical,
			'casesPerOneMillion': casesPerOneMillion, 'deathsPerOneMillion': deathsPerOneMillion, 'totalTests': totalTests, 'testsPerOneMillion': testsPerOneMillion})

def write_db(date_of_robot_run, time_of_scrape, country, cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion, deathsPerOneMillion, totalTests, testsPerOneMillion):
	cur.execute("INSERT INTO covid(date, time, country, cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion, deathsPerOneMillion, totalTests, testsPerOneMillion) \
	VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
	(date_of_robot_run, time_of_scrape, country, cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion, deathsPerOneMillion, totalTests, testsPerOneMillion))
	con.commit()

def create_csv():
	with open('covid19_{}.csv'.format(date.today().strftime("%Y.%m.%d")), 'w', encoding='utf-8') as f:
		csv_writer = csv.DictWriter(f, delimiter='|', fieldnames=header)
		csv_writer.writeheader()

# Robot parse started
def robot_start_header(website, front_or_back, page):
	robot_name = website + ' ' + front_or_back + ' ' + page
	print('\n')
	print('===========================================================')
	print('Robot: ' + robot_name)
	print('Robot Start: ' + str(datetime.now().replace(microsecond=0)))
	print('===========================================================')
	print('\n')
	time.sleep(3)

# Robot parse ended
def robot_end_header(website, front_or_back, page):
	robot_end_time = datetime.now().strftime("%H:%M:%S")
	robot_name = website + ' ' + front_or_back + ' ' + page
	execution_time = round(((time.time()-robot_start_time_float)/60),2)  # robot total runtime
	print('\n')
	print('Scraping ' + robot_name + ' complete!')  
	print('\n')
	print('===========================================================')
	print("Robot Start Time: " + robot_start_time)
	print("Robot End Time: " + robot_end_time) 
	print('Robot Run Time: ' + str(execution_time) + ' minutes')
	print('===========================================================')
	print('\n')

# start the script
if __name__ == '__main__':
	website = 'Covid19'
	front_or_back = ''
	page = ''
	header = ['date_of_robot_run', 'time_of_scrape', 'country', 'country', 'cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered', 'active', 'critical', 'casesPerOneMillion', 'deathsPerOneMillion', 'totalTests', 'testsPerOneMillion']
	robot_start_time_float = time.time()
	robot_start_time = datetime.now().strftime("%H:%M:%S")
	robot_start_header(website, front_or_back, page)
	con = sqlite3.connect("/content/covid19.db")
	cur = con.cursor()
	create_csv()
	print_header(header)
	get_data()
	robot_end_header(website, front_or_back, page)
