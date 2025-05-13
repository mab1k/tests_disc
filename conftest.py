import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


PATH_CHROME = '/home/user/selenium/chrome-linux64/chrome'
PATH_CHROME_DRIVER = '/usr/local/bin/chromedriver'

@pytest.fixture(scope="module")
def driver():
    service = Service(PATH_CHROME_DRIVER)

    chrome_options = Options()
    chrome_options.binary_location = PATH_CHROME
    #chrome_options.add_argument(PROXY) 
    chrome_options.add_argument('--no-sandbox') 
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    
    yield driver
   
    driver.quit()
