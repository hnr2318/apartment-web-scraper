from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import requests


app = Flask(__name__)
app._static_folder = "templates/static"

@app.route('/')
def index():
    print("Rendered!")
    return render_template('index.html')

@app.route('/my-link/')
def my_link():
    print ('I got clicked!')

    return 'Click.'

@app.route('/scrape', methods = ['GET'])
def GetAptInfo():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.apartments.com/atlanta-ga/")

    # click "More" button to access filter options
    clickMore = driver.find_element("xpath",'//*[@id="advancedFiltersIcon"]').click()

    # click "1 Bath" option
    clickBaths = driver.find_element("xpath",'//*[@id="1_baths"]').click()

    # click ammenities options
    clickAC = driver.find_element("xpath",'//*[@id="advancedFilterUnitAmenities"]/li[1]/a').click()
    clickWD = driver.find_element("xpath",'//*[@id="advancedFilterUnitAmenities"]/li[2]/a').click()
    clickCats = driver.find_element("xpath",'//*[@id="advancedFilterUnitAmenities"]/li[13]/a').click()
    clickBalcony = driver.find_element("xpath",'//*[@id="advancedFilterUnitAmenities"]/li[22]/a').click()
    clickHardwood = driver.find_element("xpath",'//*[@id="advancedFilterUnitAmenities"]/li[21]/a').click()
    clickClosets = driver.find_element("xpath",'//*[@id="advancedFilterUnitAmenities"]/li[31]/a').click()

    # click "Cheap" option
    clickCheap = driver.find_element("xpath",'//*[@id="Specialties_128"]').click()

    # click "5 star" rating option
    clickRating = driver.find_element("xpath",'//*[@id="Rating_16"]').click()

    # click "Done" to finish filtering and load results
    clickDone = driver.find_element("xpath",'//*[@id="advancedFilters"]/section/button[2]').click()

    # make sure that the results tag includes the filter word "Cat" to ensure the results are loaded only after filtering is complete
    mapResultsWait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mapResultBox"]')))
    while "Cat" not in mapResultsWait.text:
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="mapResultBox"]'), "Cat"))

    # get lists of all of the relevant information (title, address, price, number of bedrooms, contact phone number)
    aptTitle = driver.find_elements(By.CLASS_NAME,"js-placardTitle")
    n = len(aptTitle)
    aptAddress = driver.find_elements(By.CLASS_NAME,"property-address")
    aptPrice = driver.find_elements(By.CLASS_NAME,"property-pricing")
    aptBeds = driver.find_elements(By.CLASS_NAME,"property-beds")
    aptPhoneElem = driver.find_elements(By.CLASS_NAME,"phone-link")
    time.sleep(4)
    # the phone number text is located inside the href of the class="phone-link" elements
    aptPhoneNum = [phoneElem.get_attribute('href') for phoneElem in aptPhoneElem]

    # clicks each of the image carousels to unlock the gallery of images in HTML DOM
    aptImageClick = driver.find_elements(By.CLASS_NAME,"imageCarouselArrowRightIcon")
    aptImgCarousel = driver.find_elements(By.CLASS_NAME,"carouselInner")
    for aptClick in aptImageClick:
        aptClick.click()

    time.sleep(1)
    # dictionary to keep info for all apartments
    resultsDict = {}
    # print all of the information for each listing
    for i in range(n):
        # array to keep info for each apartment
        aptInfoArr = []
        aptInfoArr.append(aptAddress[i].text)
        aptInfoArr.append(aptPrice[i].text)
        aptInfoArr.append(aptBeds[i].text)
        aptInfoArr.append(aptPhoneNum[i])
        thisAptImages = aptImgCarousel[i].find_elements("xpath", './child::*')
        numImages = len(thisAptImages)
        for j in range(numImages):
            photosArr = []
            try:
                backImage = thisAptImages[j]
                photosArr.append(backImage.value_of_css_property("background-image").split("(")[1].split(")")[0])
                r = requests.get(backImage.value_of_css_property("background-image").split("(")[1].split(")")[0])
                fileName = aptTitle[i].text + ".jpg"
                with open(fileName, 'wb') as f:
                    f.write(r.content)
            except:
                break
            aptInfoArr.append(photosArr)

        resultsDict[aptTitle[i].text] = aptInfoArr

    # send the final dictionary into a json object (format = {AptName1: [address, price, etc.], AptName2: [...], ...})
    jsonDump = json.dumps(resultsDict)
    #print(jsonDump)
    return jsonDump


if __name__ == '__main__':
    app.run(debug=True)