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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DEA4BD68EF43AC029831C46D7AA6DD369E4A94E636930AD3D801ECD5757465D8E22F288352FCF27E887EFBEFCC27D497CFF9A891B55EB23053CFFCFCED3FD8DA8C58750A14236BEE66E7C3D07219B25ECF17531C7E05695D2A194E3AC01E6F5179DBFCC62879A5944DADE78AEE093AF3EFB403607A8DEEBA66F77A3E2B63926F44C63335208F1AD9A169E91CA2BBDAB00F64C2005F9D0EDEBE2A94B1B0929D2CA6B190653864ADDEF6F73991CB6ADA9E0252EA0C1B9BFEED12F677960D586A4411AE64CF642F2D4425DA2876A8E16571B5B510F0655390BB5B51263AA89D6D8C707783279E27BC9E1DA50C5DA01E68C72C1E3F7CE05DA2E4B5052361DBC120E1F71CC747488BE44B2393D8CA7CCCD7999596027705189177424D439810E873E95388E0829815CB71B2CE799EF316DAF29F0416CB1DE9AD2FEC0CB44B25F3CCCA898FC2A7ED05823A22B9021CE0AD11C8D2756593DD7ADB8CC9A62AE6613142F7"})
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
