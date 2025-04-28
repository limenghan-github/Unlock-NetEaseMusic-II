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
    browser.add_cookie({"name": "MUSIC_U", "value": "002DA0D9A8D171885EA9167380B6E2BF3342B559E6C84FE8BB03EA6C6D70483FDA0258A39E021D9DAAA5EFAE7E3C0E62BAD86A525335164318DBF695C7F4D7DCB0B8A891385925B19612AEE5BDF01BF49D3EA2E75B4E0227CDC40407C32019A17B0DEDD8B272DB264CE8C15D1E6CD1363E34090E3DFAE1BACCB8E22F6BD3A551A0253CE9E559F452DC060F2E94E2E54461F7C07A0B99381EE10FFEF3FB7D91CEB45190465EDEFC05686AD3B73D28B7ADC87998C77336A0ECE4E610500BF3992F5984206741D3F1F7ED56C85611A699A6F3E2E42B107D17BBFCFE6FB7574A0498DB095A0D44CDDDB1471BFBF8AE41D7972FB50D553F30AADE2028494F2F8C1F09746BEA89D97D8A10781DCED3EAB76B08C05543C64B20327D04F41F4AC22054DBE71C7B4B05E6918DEB2C797C0C5D151FB4D8BFDF2DEF62A5BC5CA6848BA05CB92ADD343A57C4622B6A6D8FC9C8FD98C4094C3C9837F32DF216F96816C58E47F2CB"})
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
