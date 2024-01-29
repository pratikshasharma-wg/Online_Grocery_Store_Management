import pytest
import unittest
from unittest import TestCase

import controllers.auth as auth
from config.config import Config
from config.logs_stmts import Logs
from database.database_queries import db_query_config
from unittest.mock import patch, Mock, MagicMock


class TestAuth(TestCase):
        
    def test_login(self):
        with patch('auth.login_details', return_value = [True,'role','username']) as p:
            self.assertEqual(auth.login(), [True,'role','username'])


    def test_login_details_valid_user(self):
        with patch('auth.validators.valid_email', return_value = "email"):
            with patch('maskpass.askpass', return_value = "password"):
                mock_db_connection = MagicMock()
                mock_cursor = MagicMock()
                mock_db_connection.return_value = mock_db_connection
                mock_db_connection.__enter__ = mock_db_connection
                mock_db_connection.cursor = mock_cursor
                mock_cursor.fetchone.return_value = ["","pwd","role"]
                with patch('auth.DatabaseConnection', mock_db_connection) as mock_db_connection:
                    with patch('auth.validate_user', return_value = True):
                        self.assertEqual(auth.login_details(),[True,"role","email"])

    def test_login_details_invalid_user(self):
        with patch('auth.validators.valid_email', return_value = "email"):
            with patch('maskpass.askpass', return_value = "password"):
                mock_db_connection = MagicMock()
                mock_cursor = MagicMock()
                mock_db_connection.return_value = mock_db_connection
                mock_db_connection.__enter__ = mock_db_connection
                mock_db_connection.cursor = mock_cursor
                mock_cursor.fetchone.return_value = [("","pwd","role")]
                with patch('auth.DatabaseConnection', mock_db_connection) as mock_db_connection:
                    with patch('auth.validate_user', return_value = False):
                        self.assertEqual(auth.login_details(),[False,"",""])

    def test_login_details_invalid_credentials(self):
        with patch('auth.validators.valid_email', return_value = "email"):
            with patch('maskpass.askpass', return_value = "password"):
                mock_db_connection = MagicMock()
                mock_cursor = MagicMock()
                
                mock_db_connection.return_value = mock_db_connection
                mock_db_connection.__enter__ = mock_db_connection
                mock_db_connection.cursor = mock_cursor
                mock_cursor.fetchone.return_value = None
                with patch('auth.DatabaseConnection', mock_db_connection) as mock_db_connection:
                    self.assertEqual(auth.login_details(),[False,"",""])

    def test_signUp(self,mocker):
        with patch('builtins.input', return_value = "name"):
            with patch('auth.validators.valid_email', return_value = "email"):
                mocker.patch('auth.password_parser', return_value = "pwd")

if __name__ == '__main__':
    unittest.main()

