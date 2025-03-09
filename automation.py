import os
import time
import logging
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import CHROME_DRIVER_PATH, DOWNLOAD_DIR, BUSINESS_PARTNER_NUMBER, USER_ID, PASSWORD
from constants import (
    LOADING_SCREEN_SELECTOR,
    SELECTOR_BUSINESS_PARTNER_INPUT,
    SELECTOR_ID_INPUT,
    SELECTOR_PASSWORD_INPUT,
    SELECTOR_LOGIN_BUTTON
)

logger = logging.getLogger(__name__)


def wait_for_loading_to_disappear(driver):
    """
    Waits until the loading screen disappears from the page.
    """
    try:
        while True:
            loading_elements = driver.find_elements(By.CSS_SELECTOR, LOADING_SCREEN_SELECTOR)
            if loading_elements:
                loading_screen = loading_elements[0]
                style_attr = loading_screen.get_attribute('style')
                if style_attr == 'display: flex;':
                    logger.debug("Loading screen detected, waiting...")
                    time.sleep(0.5)
                else:
                    logger.debug("Loading screen disappeared.")
                    break
            else:
                logger.debug("Loading screen not detected.")
                break
    except WebDriverException:
        logger.exception("Exception while checking loading screen.")
        raise


def click_element(driver, selector, selector_type='css'):
    """
    Waits until the specified element is clickable, and then clicks on it.
    """
    max_attempts = 5
    attempts = 0

    if selector_type == 'css':
        by = By.CSS_SELECTOR
    elif selector_type == 'xpath':
        by = By.XPATH
    else:
        raise ValueError(f"Invalid selector_type: {selector_type}")

    while attempts < max_attempts:
        try:
            element = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((by, selector)))
            element.click()
            logger.debug(f"Clicked element: {selector}")
            return
        except (TimeoutException, WebDriverException) as e:
            attempts += 1
            logger.warning(f"Unable to click element '{selector}', "
                           f"attempt {attempts}/{max_attempts}: {e}")
            time.sleep(3)

    logger.error(f"Failed to click element after {max_attempts} attempts: {selector}")
    raise TimeoutException(f"Cannot click element: {selector}")


def fill_form_field(driver, css_selector, text):
    """
    Fills in a form field with the specified text.
    """
    try:
        wait_for_loading_to_disappear(driver)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        form_field = driver.find_element(By.CSS_SELECTOR, css_selector)
        form_field.send_keys(text)
        logger.debug(f"Filled form field '{css_selector}' with text='{text}'.")
    except (TimeoutException, WebDriverException):
        logger.exception(f"Failed to fill form field '{css_selector}' with text='{text}'.")
        raise


def initialize_webdriver_and_navigate(url):
    """
    Initializes the webdriver and navigates to the specified URL.
    """
    try:
        driver_path = CHROME_DRIVER_PATH
        chrome_options = Options()

        download_dir = os.path.join(os.getcwd(), DOWNLOAD_DIR)
        os.makedirs(download_dir, exist_ok=True)

        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })

        driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=chrome_options)
        driver.get(url)
        logger.info(f"Navigated to {url}")
        return driver

    except WebDriverException as e:
        logger.exception(f"Error initializing WebDriver or navigating to {url}")
        raise


def sign_in(driver):
    """
    Signs in to the website using credentials from config.
    """
    try:
        fill_form_field(driver, SELECTOR_BUSINESS_PARTNER_INPUT, BUSINESS_PARTNER_NUMBER)
        fill_form_field(driver, SELECTOR_ID_INPUT, USER_ID)
        fill_form_field(driver, SELECTOR_PASSWORD_INPUT, PASSWORD)
        click_element(driver, SELECTOR_LOGIN_BUTTON)
        logger.info("Sign-in process completed.")
    except Exception:
        logger.exception("Failed to sign in.")
        raise
