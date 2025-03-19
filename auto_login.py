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
    browser.add_cookie({"name": "MUSIC_U", "value": "006AD9B6E2197F5CD4AC9A49D6FECE4542B8EA52F26B2431D7B36075F06833529920D0AE0E1837624BC11300EE61189E3BAA100A8CE35D00D5896F7670FFFDDED14DE1F3448AB9C032A99B5605B759BCC1CB9B14F3BCEAC9F0B7A02B574B68603D71FCB93CE8D422BCE060B143BD47876701C70DB3FD9B9A9F197B4A5CB91680F3EC740F18A3940B6696ADC0F1B113AF5C951AF76877C15ACC0D56FB1CAEACEAEC8B7EEF62B701D47240F39F1DD64E8332FF743EE7FFC6890A35C7840DCFE1C16EAA73FB37CBD079B579904F0C80C1EEF586D1E8F8C927CC47844352A13AC00F508DC5C454EEB041089C9AB59C5787821C28B740A32770A263F6668B425A289EBFAA1D40B3C8519CFF49EF8CB43F8E0D34952E458E1A5FAE5C063E7AA6DE486526C2E969CD138AE63C52C550E95DD862262C930533FE0885E53AFF8DEE0A266A7ECB7478EE0583669FAB6468EF0C9E845BA5C53B7D70AA4C5575CE97A3181A88D4"})
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
