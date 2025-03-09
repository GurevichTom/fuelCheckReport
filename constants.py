# Sign In
SELECTOR_BUSINESS_PARTNER_INPUT = 'input[aria-label="מספר שותף עסקי"]'
SELECTOR_ID_INPUT = 'input[aria-label="תעודת זהות"]'
SELECTOR_PASSWORD_INPUT = 'input[aria-label="סיסמה"]'
SELECTOR_LOGIN_BUTTON = 'button[aria-label="כניסה"]'

# Reports
SELECTOR_REPORTS_MENU = 'div[aria-label="דוחות מידע"]'
SELECTOR_REPORT_DROPDOWN = 'mat-select[aria-label="בחר את הדוח המבוקש"]'
REPORT_TYPE_TEXT = 'דוח תדלוקים מפורט'  # used for matching text in the Xpath
SELECTOR_DATE_INPUT = 'input[aria-label="תקופה עד"]'
SELECTOR_LOGISTIC_GROUP_SELECT = 'mat-select[aria-label="קבוצה לוגיסטית"]'
SELECTOR_SHOW_REPORT_BUTTON = 'div[aria-label="הצג דוח"]'
SELECTOR_EXPORT_EXCEL_BUTTON = 'button[aria-label="ייצוא לאקסל"]'
SELECTOR_GENERATE_REPORT_BUTTON = 'button[aria-label="הפקת דוח"]'

# Other Buttons/Elements
SELECTOR_BACK_BUTTON = 'button[class="btn-back mat-button mat-button-base"]'

# Xpath
XPATH_OPTION_TEMPLATE = "//mat-option/span[contains(text(), '{option_text}')]"

# Example for label checkboxes (used in `select_options`):
CHECKBOX_SELECTOR = "input[type='checkbox']"
CHECKBOX_LABEL_XPATH = "./ancestor::label/span"

# Misc
LOADING_SCREEN_SELECTOR = 'div.example-loading-shade'
DATE_PICKER_OVERLAY_ID = 'cdk-overlay-1'
DATE_PICKER_OVERLAY_BACKDROP = 'div[class="cdk-overlay-backdrop mat-overlay-transparent-backdrop cdk-overlay-backdrop-showing"]'
