from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC

import time


login_url = 'https://www.instagram.com/accounts/login/'
profile_url = 'https://www.instagram.com/devmart10/'


# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# go to the page
driver.get(login_url)

# find the <input> elements
username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')

# enter credentials
username.send_keys('devmart10')
password.send_keys('pokemon')
driver.find_element_by_tag_name('button').click()

# wait for next page to load
WebDriverWait(driver, 10).until(EC.title_is('Instagram'))

# click profile
driver.get(profile_url)

# keep clicking load more button while there are more
load = driver.find_element_by_partial_link_text('Load more')
load.click()

for i in range(3):
	print(i)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(5)

