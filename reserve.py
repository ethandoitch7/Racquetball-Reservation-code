from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import time

# ===== CONFIGURE THESE =====
USERNAME = '****'
PASSWORD = '****'
ZIP = '91326'
CHROMEDRIVER_PATH = 'C:/Users/ethan/OneDrive/Desktop/chromedriver.exe' 
TARGET_LOCATION = 'NORTHRIDGE'
DURATION = '120'
if datetime.today().weekday() == 6:
	COURT_TIME = '10:30 AM' 
else:
	COURT_TIME = '06:30 PM'
COURT = '2322'
DAYS_AHEAD = 14 #2 weeks in advance
# ===========================
print("Heratch")
print(datetime.today())
# Date of the court you want to book
start_date = datetime.today()
target_date = start_date  + timedelta(days=DAYS_AHEAD)
target_date_str = target_date.strftime('%#m/%#d/%Y') 
print(target_date_str)

# Start browser
service = Service(CHROMEDRIVER_PATH)

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
options.add_argument('--log-level=3')  # Suppress most logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress DevTools messages

driver = webdriver.Chrome(service=service, options=options)
# Go to LA Fitness login page
driver.get('https://www.lafitness.com/Pages/RacquetballReservation.aspx')

wait = WebDriverWait(driver, 5)

# Log in
wait.until(EC.presence_of_element_located((By.ID, 'txtUser'))).send_keys(USERNAME)
wait.until(EC.presence_of_element_located((By.ID, 'txtPassword'))).send_keys(PASSWORD)
wait.until(EC.presence_of_element_located((By.ID, 'ctl00_MainContent_Login1_btnLogin'))).click()
print("Login Complete")
print(datetime.today())

while datetime.now().hour != 0 or datetime.now().minute != 0:
    time.sleep(0.1)

NUMBER_OF_RUNS = 1
while NUMBER_OF_RUNS < 6:
	try:
		print(NUMBER_OF_RUNS)
		print("Refresh Page")
		driver.refresh()

		print("Step 1 - change club")
		wait.until(EC.presence_of_element_located((By.ID, 'btnChangeClub'))).click()
		time.sleep(0.1)

		print("Step 2 - ZIP")
		wait.until(EC.presence_of_element_located((By.ID, 'txtZipCode'))).send_keys(ZIP)
		driver.find_element(By.ID, 'btnFindclub').click()
		driver.find_element(By.ID, 'btnFindclub').click()
		wait.until(EC.presence_of_element_located((By.ID, 'arySelClub'))).click()
		time.sleep(0.1)

		print("Step 3 - Date")
		Select(wait.until(EC.presence_of_element_located((By.ID, 'ddlDates')))).select_by_value(target_date_str)  
		time.sleep(0.1)

		print("Step 4 - Duration")
		Select(wait.until(EC.presence_of_element_located((By.ID, 'ddlDuration')))).select_by_value(DURATION)
		time.sleep(0.1)

		print("Step 5 - Time")
		if NUMBER_OF_RUNS == 4 and datetime.today().weekday() != 6:
			COURT_TIME = '07:00 PM'
		if NUMBER_OF_RUNS == 5 and datetime.today().weekday() != 6:
			COURT_TIME = '07:30 PM'
		Select(wait.until(EC.presence_of_element_located((By.ID, 'cboSearByTimeList')))).select_by_value(COURT_TIME)
		time.sleep(0.1)

		print("Step 6 - Court")
		Select(wait.until(EC.presence_of_element_located((By.ID, 'cboCourtByTime')))).select_by_value(COURT)
		time.sleep(0.1)

		print("Step 7")
		driver.find_element(By.ID, 'btnSaveReservation').click()
		print("Complete Save")
		print(datetime.today())
		try:
			error_element = wait.until(EC.presence_of_element_located((By.ID, "lblErrorMessage")))
			error_text = error_element.text.strip()
			if error_text:
				print("Error message:", error_text)
			else:
				print("No error message displayed.")

		except:
			print("Success")
		
		NUMBER_OF_RUNS = 6

	except Exception as e:
		NUMBER_OF_RUNS = NUMBER_OF_RUNS + 1
		print(str(e))
		print(datetime.today())


input("Press Enter to close the browser...")

#driver.quit()


