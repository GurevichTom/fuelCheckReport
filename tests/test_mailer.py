import os
import sys
from unittest.mock import MagicMock, patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mailer import send_email

@patch("mailer.os.path.basename")
@patch("mailer.open")
@patch("mailer.smtplib.SMTP")
def test_send_email_success(mock_smtp, mock_file, mock_basename):
    """
    Tests that send_email tries to attach the file and send the email.
    """
    mock_basename.return_value = "report.xlsx"
    mock_file.return_value = mock_open(read_data=b"fakebinarydata").return_value

    smtp_instance = MagicMock()
    mock_smtp.return_value = smtp_instance

    send_email("Test Subject", "Hello Body", "/path/to/report.xlsx", "one@domain.com;two@domain.com")

    mock_file.assert_called_once_with("/path/to/report.xlsx", "rb")
    smtp_instance.sendmail.assert_called_once()
    smtp_instance.quit.assert_called_once()

@patch("mailer.open", side_effect=FileNotFoundError("No file found"))
def test_send_email_file_not_found(mock_open_fn):
    """
    If file isn't found, the function logs an exception but doesn't raise.
    """
    from mailer import logger
    with patch.object(logger, "exception") as mock_logger_ex:
        send_email("test", "body", "/invalid/path.xlsx", "someone@domain.com")
        mock_logger_ex.assert_called_once_with("Failed to attach file: /invalid/path.xlsx")

@patch("mailer.smtplib.SMTP", side_effect=Exception("SMTP failure"))
def test_send_email_smtp_fail(mock_smtp):
    """
    If SMTP server fails, we log an exception.
    """
    from mailer import logger
    with patch.object(logger, "exception") as mock_logger_ex:
        send_email("test", "body", "/path/report.xlsx", "someone@domain.com")
        mock_logger_ex.assert_called_once()
