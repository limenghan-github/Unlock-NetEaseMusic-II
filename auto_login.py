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
    browser.add_cookie({"name": "MUSIC_U", "value": "001CE815591380D76BB5EE9FF055C56CFAC5D8238463BA3D5EDFCF9F0D5528FF6707BD8C7DE6F1BC85B725986062C1C57645253BE43481C966F2B2F01A65AB52C07BD20E677937870033303D36E935155217E68F767566CBC500E73EA8C4DA691295096E60A3A10A7F612E6EBB1AB0E5C2130428180A1C47ECF04AA5CBBAFB7DCEB2E018A204F9EE413C82FA6393B4F1B411A8D22F0044273A8461E1237CE4B9C4017ACA10BC16C0D32DE6AFAF713D9A810339723941F7C95EE5CDDE56238132F984B2530FD481B8888B0F50C8212584C015ECEBDD5D19CF431D01148D55A998CF7851010686A4B54833290FEEFB244A271473CD8D968677B006EEC948871DF46E5047FA691315BE4FCAD6790397330649E88371F9373CFC7B63C3019DB5A16159C0E4CF173E765EF011051E992948134C4C0644B82E0A10F270B7D4AAC07527D213BD46BED7EDB6E6A2BDF6996B89BF403A2499FBC96B648CA7006FC21DEDA554"})
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
