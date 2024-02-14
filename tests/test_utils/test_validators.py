import pytest
import re

from utils import validators


def test_valid_email_negative(mocker):
    mocker.patch("builtins.input", return_value="email")
    return_value = validators.valid_email()
    assert return_value is False


def test_valid_email_positive(mocker):
    mocker.patch("builtins.input", return_value="email@gmail.com")
    return_value = validators.valid_email()
    assert return_value is True


def test_validate_pwd_positive(mocker):
    return_val = validators.validate_pwd("123")
    assert return_val is False


def test_validate_pwd_negative():
    return_val = validators.validate_pwd("Pratiksha15@")
    assert return_val is True
