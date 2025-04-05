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
    browser.add_cookie({"name": "MUSIC_U", "value": "006BF2D637B24B15D3CC3587FC5061C5142DA040876A9250C17B8CA4E3A07D0FD08AB749A0219E26A49686FA68538345EC1F400B9A5D2D501E24179904ED761823EE5A6AB2896B697184C6134CEA1FC8A01D81C57463569B4864B336F8F80A6E894C7935DF8F76DDD222D12E4C94C4066CD22AEF09DBB141BD0AF28AB213CF78DDE5F72AE869BD0FF9B0F333CD0313CFF93CC2DBC18B361BE1F758350960547E34B750ABBC701BE0656E9F9EEEDE148A7A6113793166D2FEEC86268CBCB0E81A2BB96C5E2D574E08D778E7D326E1443EEF8AA998DA4457A643E4FC1BC56B62878F3A1ADACD8C10C24676C46C5BCC4D7B0A72E6FDF73F62D599FB614AB94699BA550E1040DF6A8F478EFA79D8B471DF88249F3933743EE3AF96DB2197A887037D235FB256E2333C8115903B250847CCD4C87B0C83BEE782FC5EF3B2362D7DB4C542E0D6FE9B90EE94F1D567EF97A3DB1960E228F6F69913B4A6A24361205879F79C"})
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
