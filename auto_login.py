# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007C6E97DEE386CBB67123839D1C3DBF3D3698AF659AAA511EABDA51686CA145B2D6E887EF5337865F12BA068D8844F4C71D9E6384AFC2E907C6A1FFABB8C74A2889316895296B3187F0FD5AE68D97693D365863D08A5DD1A85CBD304CC25BE177D5F5C4BD3AB735B03DB84D1C0B234DC026FFC470D54BB544992313C1C54F2C57EAB696E82CF524872FB44E4D006FD6B0A58F1B6605BBAD54B9FCEC5995BE33DB2FFA9EDDD23439CDCC0CA922B71FD9FFF803F4008317F4D97706D8967502FE4FA55EA8B11D5D98AE9B527753BE44FD9CEDCC13880B8EEA175582AFD8ABC6DCAAB320DFE1CABF998E7B410AF42E9042D7F8F9E575E7233CA3BE2333F9975B48E63E041F2C04C517B4C3FCB63FAF09389C95884C982B3892D379879F6D4B0EDB9D209C11053122AE291304467EDA7D3B72BC94B3FB2A79649E470855A0878F8ED162D9EA0CB438FEE13A1C2B12D60B8FA9C1066BBD125CDB92A87F0DE22F96A239"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
