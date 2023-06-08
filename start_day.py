

import sys
import os
import time
import json
import argparse
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.service import Service as ChromeService


def set_chrome_options(chrome_options):

    # Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) 96.0.4664.113 Safari/537.36

    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Fedora; Linux x86_64)"
                                + "AppleWebKit/537.36 (KHTML, like Gecko)"
                                + "96.0.4664.113 Safari/537.36")

    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    if settings['incognito']:
        chrome_options.add_argument("--incognito")

    if settings['mute_audio']:
        chrome_options.add_argument("--mute-audio")

    if settings['maximize_window']:
        chrome_options.add_argument("start-maximized")

    if settings['headless']:
        chrome_options.add_argument("--headless")


def exit(message=""):
    if message == "":
        message = "Oops! Something went wrong."

    print(message)
    driver.quit()
    sys.exit()


def get_settings():
    settings = {}

    try:
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'settings.json')) as json_f:
            settings = json.load(json_f)
    except:
        print("Failed to import settings from settings.json.")
        sys.exit()

    return settings


def get_credentials():

    try:
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'credentials.json')) as json_file:
            creds = json.load(json_file)

        login = creds['login']
        password = creds['password']
    except:
        return "", ""

    return login, password


def parse_arguments():
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    return args


def login_to_sso(login, password):
    print("Starting the login")
    if settings['auto_login'] and login != "" and password != "":
        user_name = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.ID, 'userNameInput'))
        )

        user_name.send_keys(login)

        password_field = driver.find_element(By.ID, 'passwordInput')
        password_field.send_keys(password)

        signin_button = driver.find_element(By.ID, 'submitButton')
        signin_button.click()

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.ID, 'punchSubmitBtnId')))

        print('Logged in to SSO')

    except WebDriverException:
        exit("Timed out. Please login to Duolingo in time.")


def punch_in_for_the_day():
    punch_in_button = driver.find_element(By.ID, 'punchSubmitBtnId')
    punch_in_button.click()


def main():

    print("🏁 Starting out")

    global settings
    settings = get_settings()

    login, password = get_credentials()

    args = parse_arguments()

    chrome_options = Options()
    set_chrome_options(chrome_options)

    global driver

    service = ChromeService(executable_path=settings['chromedriver_path'])

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://methodisthospitals-sso.prd.mykronos.com/wfd/home")

    try:
        have_account = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'brandingWrapper'))
        )
        login_to_sso(login, password)
    except WebDriverException as e:
        exit(e)

    print("Clocking in for the day")

    punch_in_for_the_day()

    print("You are punched in")

    input("Press Enter to continue...")


if __name__ == "__main__":
    main()
