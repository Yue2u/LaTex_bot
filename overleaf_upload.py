from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils import path_join, get_abs_path
from create_bot import USER_DATA
import time


def upload(email, password, uid, pr_name):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.overleaf.com/login")
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, "btn-primary").click()
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "new-project-button").click()
        driver.find_element(By.LINK_TEXT, "Upload Project").click()
        driver.find_element(By.NAME, "files[]").send_keys(
            path_join(get_abs_path(), USER_DATA, uid, pr_name, pr_name + ".zip")
        )
        time.sleep(5)
    except Exception as ex:
        driver.close()
        driver.quit()
        raise Exception(str(ex))

    driver.close()
    driver.quit()
