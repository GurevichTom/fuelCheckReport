import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from reports import (
    get_previous_friday,
    select_options
)


@patch("reports.datetime")
def test_get_previous_friday(mock_datetime):
    """
    Tests the logic for returning the previous Friday date.
    """
    from datetime import datetime

    # Suppose 'today' is a Wednesday => day=5 => previous Friday would be day=2
    mock_datetime.today.return_value = datetime(2023, 9, 6)  # Wed 2023-09-06
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

    result = get_previous_friday()
    # Wednesday 9/6 -> the previous Friday is 9/1 if we are simplistic
    # day=6 is Wed => Fri is day=4 => difference = 2
    assert result == "1/9/2023"

@patch("reports.WebDriverWait")
def test_select_options(mock_wait):
    """
    Test that select_options tries to select or deselect checkboxes based on label.
    """
    driver = MagicMock()
    # Simulate existing checkboxes
    mock_checkbox_1 = MagicMock()
    mock_checkbox_2 = MagicMock()
    # Labels
    mock_checkbox_1.find_element.return_value.text = "מספר רכב"
    mock_checkbox_1.get_attribute.return_value = 'false'
    mock_checkbox_2.find_element.return_value.text = "SomeOtherOption"
    mock_checkbox_2.get_attribute.return_value = 'true'

    mock_wait.return_value.until.return_value = [mock_checkbox_1, mock_checkbox_2]

    select_options(driver)
    # We expect 2 calls for each checkbox (one to get label, one to click).
    assert mock_checkbox_1.find_element.call_count == 2
    mock_checkbox_1.find_element.return_value.click.assert_called_once()

    assert mock_checkbox_2.find_element.call_count == 2
    mock_checkbox_2.find_element.return_value.click.assert_called_once()


@patch("reports.os")
@patch("reports.logger")
def test_get_latest_downloaded_file(mock_logger, mock_os):
    """
    Ensure get_latest_downloaded_file returns the newest file from DOWNLOAD_DIR
    """
    mock_os.path.join.side_effect = lambda *args: "/".join(args)

    # Suppose the directory has these files
    mock_files = ["file1.xlsx", "file2.xlsx"]
    mock_os.getcwd.return_value = "/home/user"
    mock_os.listdir.return_value = mock_files

    # We'll pretend file2.xlsx is the newer one
    # side_effect => call with (path, file) => returns a different ctime
    def getctime_side_effect(path):
        if "file1.xlsx" in path:
            return 100
        elif "file2.xlsx" in path:
            return 200
        return 0

    mock_os.path.getctime.side_effect = getctime_side_effect

    from reports import get_latest_downloaded_file
    result_path, result_file, result_ctime = get_latest_downloaded_file()
    assert result_file == "file2.xlsx"
    assert result_path == "/home/user/report list/file2.xlsx"
    assert result_ctime == 200

@patch("reports.get_latest_downloaded_file")
def test_get_latest_report(mock_get_latest):
    mock_get_latest.side_effect = [
        ("path/file1.xlsx", "file1.xlsx", 100),
        ("path/file1.xlsx", "file1.xlsx", 100),
        ("path/file2.xlsx", "file2.xlsx", 200)
    ]
    from reports import get_latest_report
    path, name = get_latest_report()
    assert path == "path/file2.xlsx"
    assert name == "file2.xlsx"


@patch("reports.click_element")
@patch("reports.fill_form_field")
@patch("reports.get_latest_report")
def test_get_information_reports(mock_latest, mock_fill, mock_click):
    """
    Ensures we call the right sequence for retrieving an info report.
    """
    driver = MagicMock()
    mock_latest.return_value = ("somepath/report.xlsx", "report.xlsx")

    from reports import get_information_reports
    path = get_information_reports(driver, "SOME_LOGISTIC_GROUP")

    # check calls
    assert mock_click.call_count > 1  # multiple clicks
    assert mock_fill.call_count >= 1  # we fill in date
    assert path == "somepath/report.xlsx"
