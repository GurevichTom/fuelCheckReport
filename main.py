import logging
from selenium.common import WebDriverException

# Local modules
from automation import initialize_webdriver_and_navigate, sign_in
from reports import get_information_reports
from mailer import send_email

from config import LOGISTIC_GROUPS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """
    The main entry point. Initializes the webdriver, signs in, retrieves reports for each logistic group,
    and sends an email for each report.
    """
    driver = None
    try:
        logger.info("Script started.")
        driver = initialize_webdriver_and_navigate('https://service.pazomat.co.il/Login')
        sign_in(driver)

        for logistic_group, email in LOGISTIC_GROUPS.items():
            report_file_path = get_information_reports(driver, logistic_group)
            send_email(
                subject="Weekly Pazomat Report",
                body=f"Attached is the weekly fuel detail report for logistic group: {logistic_group}",
                attachment_path=report_file_path,
                recipient_emails=email
            )

    except WebDriverException:
        logger.exception("A Selenium WebDriver error occurred.")
    except Exception:
        logger.exception("Unexpected error occurred in main.")
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("WebDriver closed.")
            except Exception:
                logger.warning("Failed to close WebDriver gracefully.")

if __name__ == "__main__":
    main()
