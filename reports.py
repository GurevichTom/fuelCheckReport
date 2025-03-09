import logging
import os
import time
from datetime import datetime, timedelta

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from automation import click_element, fill_form_field
from config import DOWNLOAD_DIR
from constants import (
    SELECTOR_REPORTS_MENU,
    SELECTOR_REPORT_DROPDOWN,
    XPATH_OPTION_TEMPLATE,
    REPORT_TYPE_TEXT,
    SELECTOR_DATE_INPUT,
    DATE_PICKER_OVERLAY_BACKDROP,
    DATE_PICKER_OVERLAY_ID,
    SELECTOR_LOGISTIC_GROUP_SELECT,
    SELECTOR_SHOW_REPORT_BUTTON,
    SELECTOR_EXPORT_EXCEL_BUTTON,
    SELECTOR_GENERATE_REPORT_BUTTON,
    CHECKBOX_SELECTOR,
    CHECKBOX_LABEL_XPATH
)

logger = logging.getLogger(__name__)

def get_previous_friday():
    """
    Returns the date of the previous Friday in DD/MM/YYYY format.
    """
    today = datetime.today()
    days_behind = today.weekday() - 4  # Monday=0,...,Sunday=6; Friday=4
    if days_behind < 0:
        days_behind += 7
    elif days_behind == 0:
        return f"{today.day}/{today.month}/{today.year}"

    previous_friday = today - timedelta(days=days_behind)
    return f"{previous_friday.day}/{previous_friday.month}/{previous_friday.year}"

def select_options(driver):
    """
    Selects certain checkboxes on the report page.
    """
    options_to_select = ['מספר רכב', 'מוצר', 'כמות ליטר', 'סכום ברוטו ש"ח', 'תאריך']

    try:
        wait = WebDriverWait(driver, 10)
        checkboxes = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, CHECKBOX_SELECTOR))
        )

        for checkbox in checkboxes:
            label = checkbox.find_element(By.XPATH, CHECKBOX_LABEL_XPATH).text
            checked = checkbox.get_attribute('aria-checked')
            if label in options_to_select and checked == 'false':
                checkbox.find_element(By.XPATH, "./parent::div").click()
                logger.debug(f"Selected checkbox: {label}")
            elif label not in options_to_select and checked == 'true':
                checkbox.find_element(By.XPATH, "./parent::div").click()
                logger.debug(f"Deselected checkbox: {label}")
    except Exception:
        logger.exception("Error selecting checkbox options.")
        raise

def get_latest_downloaded_file():
    """
    Retrieves the most recently downloaded file from the DOWNLOAD_DIR.
    """
    directory = os.path.join(os.getcwd(), DOWNLOAD_DIR)
    os.makedirs(directory, exist_ok=True)

    files = os.listdir(directory)
    if not files:
        return None, None, None

    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(directory, x)))
    latest_file_path = os.path.join(directory, latest_file)
    latest_file_ctime = os.path.getctime(latest_file_path)

    logger.debug(f"Latest downloaded file: {latest_file_path}")
    return latest_file_path, latest_file, latest_file_ctime

def get_latest_report(start_time=time.time(), timeout=120):
    """
    Retrieves the most recent .xlsx report, with a timeout.
    """
    prev_report_path, prev_report_name, prev_file_ctime = get_latest_downloaded_file()
    if prev_file_ctime is None:
        prev_file_ctime = 0

    while True:
        latest_report_path, latest_report_name, latest_file_ctime = get_latest_downloaded_file()
        if latest_file_ctime != prev_file_ctime and latest_report_path and latest_report_path.endswith('.xlsx'):
            logger.debug(f"Found new XLSX report: {latest_report_path}")
            return latest_report_path, latest_report_name

        if time.time() - start_time > timeout:
            logger.error("Download took too long, raising exception.")
            raise TimeoutException("Download took too long.")

        time.sleep(1)

def get_information_reports(driver, logistic_group):
    """
    Retrieves information reports for the specified logistic group.
    """
    try:
        click_element(driver, SELECTOR_REPORTS_MENU)
        click_element(driver, SELECTOR_REPORT_DROPDOWN)

        xpath_selector = XPATH_OPTION_TEMPLATE.format(option_text=REPORT_TYPE_TEXT)
        click_element(driver, xpath_selector, 'xpath')

        click_element(driver, SELECTOR_DATE_INPUT)
        fill_form_field(driver, SELECTOR_DATE_INPUT, get_previous_friday())
        logger.debug(f"End date set to previous Friday: {get_previous_friday()}")

        # Remove date picker overlay if present
        while True:
            try:
                driver.execute_script(f"document.getElementById('{DATE_PICKER_OVERLAY_ID}').style.display = 'none';")
                break
            except Exception:
                logger.debug('Calendar overlay not found, retrying...')
                time.sleep(1)

        click_element(driver, DATE_PICKER_OVERLAY_BACKDROP)

        click_element(driver, SELECTOR_LOGISTIC_GROUP_SELECT)
        xpath_selector = XPATH_OPTION_TEMPLATE.format(option_text=logistic_group)
        click_element(driver, xpath_selector, 'xpath')

        click_element(driver, SELECTOR_SHOW_REPORT_BUTTON)
        click_element(driver, SELECTOR_EXPORT_EXCEL_BUTTON)

        select_options(driver)

        click_element(driver, SELECTOR_GENERATE_REPORT_BUTTON)

        report_file_path, report_file_name = get_latest_report()

        driver.back()
        driver.back()
        driver.refresh()

        logger.info(f"Generated report for '{logistic_group}', saved to: {report_file_path}")
        return report_file_path
    except Exception:
        logger.exception(f"Failed to get information report for logistic group '{logistic_group}'.")
        raise
