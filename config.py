import os
from dotenv import load_dotenv

"""
Configuration file for the 'pazomat automation' script.
"""

# Load environment variables (if using a .env file)
load_dotenv()

# 1. Chrome WebDriver Settings
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", r"C:\Path\To\ChromeDriver\chromedriver.exe")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "report list")

# 2. Credentials for pazomat.co.il
BUSINESS_PARTNER_NUMBER = os.getenv("BUSINESS_PARTNER_NUMBER", "YOUR_BUSINESS_PARTNER_NO")
USER_ID = os.getenv("ID", "YOUR_ID")

PASSWORD = os.getenv("PASSWORD", "YOUR_PASSWORD")
# 3. SMTP/Email Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "192.168.20.30")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "pycharm@budget.co.il")

LOGISTIC_GROUPS = {
    'אילת': 'eilat@budget.co.il;anabely@budget.co.il',
    'ירושלים': 'jerusalem@budget.co.il',
    'נתניה': 'natanya@budget.co.il',
    'באר שבע': 'BeerSheva@budget.co.il',
    'אייל': 'Ashdod@budget.co.il'
}

