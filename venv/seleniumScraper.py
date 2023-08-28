from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://news.ycombinator.com/login")

USERNAME = "hnr2318"
PASSWORD = "pass2318"

# createUsr = driver.find_element("xpath","/html/body/form[2]/table/tbody/tr[1]/td[2]/input").send_keys(USERNAME)
# createPass = driver.find_element("xpath","/html/body/form[2]/table/tbody/tr[2]/td[2]/input").send_keys(PASSWORD)
# submitCreate = driver.find_element("xpath","//input[@value='create account']").click()

logUsr = driver.find_element("xpath","/html/body/form[1]/table/tbody/tr[1]/td[2]/input").send_keys(USERNAME)
logPass = driver.find_element("xpath","/html/body/form[1]/table/tbody/tr[2]/td[2]/input").send_keys(PASSWORD)
submitLogin = driver.find_element("xpath","//input[@value='login']").click()

# how to check if we are logged in? logout button
try:
    logout_button = driver.find_element("id","logout")
    print('Successfully logged in')
except NoSuchElementException:
    print('Incorrect login/password')


