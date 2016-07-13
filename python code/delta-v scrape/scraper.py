import js2py
from bs4 import BeautifulSoup
import urllib.request

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC


url = 'http://www.dcl.hpi.uni-potsdam.de/home/feinbube/web/stealth/KSPDeltaVMap/'


# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# go to the page
driver.get(url)

# find the element that's name attribute is q (the google search box)
missions = driver.find_elements_by_class_name('aobjective')

WebDriverWait(driver, 10)
driver.quit()
