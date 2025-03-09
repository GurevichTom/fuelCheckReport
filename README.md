# Fuel Check Report Automation

This project automates weekly fuel report generation and distribution for specified logistic groups, interacting with an internal web service for data retrieval. It:

- Logs into the **Pazomat** site via Selenium  
- Generates Excel-based fuel detail reports  
- Downloads them, then automatically distributes via email  
- Offers robust error handling and logging  

## Key Features

1. **Modular Codebase**  
   - **`automation.py`**: Selenium setup, base click/fill logic, user sign-in.  
   - **`reports.py`**: Business logic for retrieving or generating fuel reports (dates, checkboxes, final download).  
   - **`mailer.py`**: Single function for sending emails with attachments.  
   - **`main.py`**: Orchestrates everything and manages the driver’s lifecycle.

2. **Configuration & Constants**  
   - **`config.py`**: Holds environment-specific settings (credentials, paths, server addresses).  
   - **`constants.py`**: Hard-coded CSS/XPath selectors and repeated strings.  

3. **Error Handling & Logging**  
   - Centralized logging messages at `DEBUG`/`INFO`/`WARNING`/`ERROR` levels.  
   - Thorough `try/except` blocks ensure partial failures won’t crash the entire script.  

4. **Test Coverage**  
   - **Mock-based** tests prevent real browser launches or SMTP connections.  
   - Found in `tests/`, referencing `pytest` + `unittest.mock`.  

## Project Structure

```
fuelCheckReport/
├── automation.py         # Selenium setup & base operations
├── reports.py            # Logic for retrieving fuel detail reports
├── mailer.py             # Email sending logic
├── main.py               # Entrypoint: sign in, generate, send
├── config.py             # Configurable paths, credentials
├── constants.py          # Central place for repeated selectors/strings
├── requirements.txt      # Minimal dependencies for production
├── dev-requirements.txt  # Development/test libraries
└── tests/
    ├── test_automation.py
    ├── test_reports.py
    └── test_mailer.py
```

## Installation & Setup

1. **Clone** the Repository:
   ```bash
   git clone https://github.com/GurevichTom/fuelCheckReport.git
   cd fuelCheckReport
   ```

2. **Install Production Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - This includes **Selenium** for the browser automation.

3. **(Optional) Install Dev/Test Dependencies**:
   ```bash
   pip install -r dev-requirements.txt
   ```
   - Installs `pytest`, `pytest-mock`, etc., for local testing.

4. **Configure**:
   - Adjust **`config.py`** for local environment (Chrome driver path, email server, etc.).
   - Confirm **`constants.py`** matches your site’s CSS or XPath.  
   - Add environment variables or safely store credentials for `USER_ID`, `PASSWORD`.

## Usage

1. **Run Script**:
   ```bash
   python main.py
   ```
   - Launches Chrome, logs into the service, fetches the weekly report for each logistic group, and emails them.

2. **Logging Output**:  
   - Prints to console by default.  
   - You can change the logging level or direct logs to a file in `main.py`.

## Running Tests

1. **Install** dev requirements if not done yet:
   ```bash
   pip install -r dev-requirements.txt
   ```
2. **Execute Tests**:
   ```bash
   pytest tests/
   ```
   - Tests use **mocks** to avoid real network or browser calls.
   - Check coverage for key logic in each module.

## Security & Privacy

- **Credentials**: Real usernames/passwords should be injected via environment variables or a `.env` file – never committed in plain text.  
- **Email**: The SMTP config in `config.py` is for demonstration.  
- The code is **Windows-specific** (Selenium with Chrome, local path usage). For cross-platform usage, verify your environment.

## Contributing

Pull requests or issues are welcome. If you’d like to add coverage for new features or a more advanced test harness, feel free to propose changes.

## License

This project is licensed under the [MIT License](LICENSE).

---

### Thank You
Thank you for checking out **Fuel Check Report Automation**! This project highlights a robust approach to automated data retrieval, PDF/Excel generation, and email distribution using Python, Selenium, and a well-tested code layout. Enjoy exploring or adapting it for your own environment!