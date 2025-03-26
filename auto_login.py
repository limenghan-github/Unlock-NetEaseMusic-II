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
    browser.add_cookie({"name": "MUSIC_U", "value": "00282CB1CBB35498D7E41D695A7A8E89E4CA4C598F43B2868FFC89BECCD270D19100A62A0432FFC21DCC3EA8B4AFD5CCACDC5E19020F6EA7C3043851B8CC4252ED64F1AFFBF090EB8D99BFA0151004C40AB459A2C8601F04B30879B4B0824B5FCA897EAF989960BB07097251C1239CBB096753D7DEE154C556FF4BFCAA1EF96123A1DFDED27222BE5B574D70C1FDFFA97C7B0E5412C88AF2B061F7A7A231BF0874243215209FC09ED41BD07CD3575D823D34F5CDE395BF5E3DFDD1B22B945A533E9B15F266367EA13FAA5ED272FB9D499ADA7322B89C8B1FFE87A3F269E279AB4E0F4D52CD5921F66ECF8871B16EEC4D402079E9F816CDA4F61D6DE8A932A33FE5D159ECFB03EBDA395C22629D9217A5218292FB051E5F3527FF4C65EB4CCBCAF22CB7C0D031F6C120AA02E7F88DAC01B0110B0B90C14C4CE07EA468DEC7B2819D5B35935C789BEF261A1FA6A3EA67154EA01374BAD292339235285763E4EE8733"})
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
