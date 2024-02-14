import sqlite3
import os

path_current_directory = os.path.dirname(os.path.abspath(__file__))


class DatabaseConnection:
    def __init__(self, host):
        self.connection = None
        self.host = host

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(
                os.path.join(path_current_directory, self.host)
            )
            return self.connection
        except Exception as e:
            print(f"Error occured {e}")

    def __exit__(self, *errors):
        self.connection.rollback() if any(errors) else self.connection.commit()
        self.connection.close()
