from dotenv import load_dotenv
load_dotenv()

import os
os.chdir(os.getenv('WORKING_DIRECTORY'))

import logging
logging.basicConfig(level=logging.INFO)

# GENERAL LIBRARIES
import random
import time

# SCRAPING LIBRARIES
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def getWebPageSeleniumHTML(url:str, waitingTime:int=random.randint(5, 10), quitDriver:bool=True) -> BeautifulSoup:
    '''
    Given the URL of a webpage, this function returns the HTML source of the webpage.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        BeautifulSoup: The HTML source of the webpage.
    '''

    chromeDriverOptions = Options()
    # chromeDriverOptions.add_argument('--headless')
    chromeDriverOptions.add_argument('--no-sandbox')
    chromeDriverOptions.add_argument('--disable-dev-shm-usage')
    chromeDriverOptions.add_argument('referer=https://www.google.com')
    
    chromeDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeDriverOptions)

    logging.info(f'Launching Chrome driver with {url}...')
    chromeDriver.get(url)

    logging.info('Getting page HTML source...')
    pageSource = chromeDriver.page_source

    if quitDriver:
        logging.info(f'Waiting before closing the driver...')
        time.sleep(waitingTime)
        logging.info(f'Closing Chrome driver...')
        chromeDriver.quit()

        return BeautifulSoup(pageSource, 'html.parser')
    else:
        return BeautifulSoup(pageSource, 'html.parser'), chromeDriver


def alwaysScrollDown(driver:webdriver) -> None:
    '''
    Continuously scrolls down a webpage until no more content is loaded.

    This function sets the web page to full display mode, then enters a loop where it scrolls to the bottom of the page. After each scroll, it waits for a random interval between 5 to 10 seconds before checking if new content has been loaded by comparing the current document height with the height from the previous scroll. If the height remains unchanged, it breaks the loop, indicating that there’s no more content to load.

    Args:
        driver (webdriver): The Selenium WebDriver instance controlling the web browser.
    
    Returns:
        None: This function does not return a value but performs the scrolling action.

    '''

    logging.info(f'Setting the page to full display...')
    driver.fullscreen_window()
    lastHeight = driver.execute_script('return document.body.scrollHeight')

    logging.info(f'Scroll page down...')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(random.randint(5, 10))
        newHeight = driver.execute_script('return document.body.scrollHeight')

        if newHeight == lastHeight:
            break

        lastHeight = newHeight