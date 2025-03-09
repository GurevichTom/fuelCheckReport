import os
import sys

import pytest
from unittest.mock import MagicMock, patch
from selenium.common import TimeoutException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from automation import initialize_webdriver_and_navigate, sign_in, click_element, fill_form_field
from config import BUSINESS_PARTNER_NUMBER, USER_ID, PASSWORD

@pytest.mark.parametrize("url", [
    "https://service.pazomat.co.il/Login",
    "https://example.com"
])
@patch("automation.webdriver.Chrome")  # Mock the Chrome driver
def test_initialize_webdriver_and_navigate(mock_chrome, url):
    """
    Ensures initialize_webdriver_and_navigate sets up the driver and navigates to the given URL.
    """
    driver_instance = MagicMock()
    mock_chrome.return_value = driver_instance

    driver = initialize_webdriver_and_navigate(url)
    mock_chrome.assert_called_once()  # ensure Chrome was instantiated
    driver_instance.get.assert_called_once_with(url)  # ensure driver.get(url) was called
    assert driver is driver_instance  # returned the same mock

@patch("automation.click_element")
@patch("automation.fill_form_field")
def test_sign_in(mock_fill_form, mock_click):
    """
    Checks that sign_in calls fill_form_field for each credential and calls click_element to submit.
    """
    driver = MagicMock()

    sign_in(driver)

    # fill_form_field calls
    # We expect 3 calls total
    assert mock_fill_form.call_count == 3

    # Check each call's positional args
    calls = mock_fill_form.call_args_list
    
    from config import BUSINESS_PARTNER_NUMBER, USER_ID, PASSWORD
    expected_texts = [BUSINESS_PARTNER_NUMBER, USER_ID, PASSWORD]

    for i in range(3):
        args, kwargs = calls[i]
        # args[0] should be driver, args[1] is the css_selector, args[2] is the text
        assert len(args) == 3
        # Just verify text matches the expected one
        assert args[2] == expected_texts[i], f"Unexpected text for fill_form_field call {i}"

    # click_element call
    mock_click.assert_called_once()


@patch("automation.WebDriverWait")
def test_click_element_success(mock_wait):
    """
    Test that click_element eventually clicks if the element becomes clickable.
    """
    driver = MagicMock()
    clickable_element = MagicMock()
    mock_wait.return_value.until.return_value = clickable_element

    click_element(driver, "some_selector", "css")
    clickable_element.click.assert_called_once()

@patch("automation.WebDriverWait")
def test_click_element_fail(mock_wait):
    """
    Test that click_element raises TimeoutException if element is never clickable.
    """
    driver = MagicMock()
    mock_wait.return_value.until.side_effect = TimeoutException("Element not clickable")

    with pytest.raises(TimeoutException):
        click_element(driver, "failing_selector", "css")

@patch("automation.wait_for_loading_to_disappear")
@patch("automation.WebDriverWait")
def test_fill_form_field(mock_wait, mock_wait_loading):
    from automation import fill_form_field
    driver = MagicMock()
    form_elem = MagicMock()

    # The element from WebDriverWait
    mock_wait.return_value.until.return_value = form_elem
    # The element from driver.find_element
    driver.find_element.return_value = form_elem

    fill_form_field(driver, "input[name='some_field']", "HELLO")
    form_elem.send_keys.assert_called_once_with("HELLO")
