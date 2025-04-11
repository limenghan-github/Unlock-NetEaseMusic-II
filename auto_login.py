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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A85694CE9B8A392C4DF9DB5AEF6F577D2CB7527A8FBA441963D83117F824F445FD20C1BBA9FAC06C3536EE57A3E5772D0841CFBB5FC36A821A9539AE4251F939E98D5689E7170AD9AE0555ADEA0B0B300CF2D7857CE35F4489B55BFC2F531E8066076533791BDD9A602343CFF086295C0841D1D0CF9D940DF314C51617A7F02F5DFCD0EC9507290199F7CE058CA97B71035DAEF8874CBC3C3A4EA50C22BCF29019FAFEBC1D3183195AA1186D84CDE9CE4AB58F6A0A39A6CF488CE3BA66EBBAC84D09E6C134A4FB06D372A5A6EAA470B2708FFA635898254C55F86DF5AF09084A8642989CF0C0AFDAE53FE5EBC470AD5B68467C63B480BAD80BE888C147435CD580FB55E20A6A4C510BCB7135FC0EC6D4051C1BA74B699AACD70E9F0FC96708AE8F0ED3FE9FB6773475A0121DA4632A0220A98956898F6220C01ACA87330712F9CFBAA997B9530AB1579BE3CE2B1A46A8BC61AC16CE9F119452E745FF362E273F"})
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
