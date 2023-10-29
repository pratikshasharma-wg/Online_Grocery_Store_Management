import sqlite3


class DatabaseConnection:
    def __init__(self, host):
        try:
            self.connection = None
            self.host = host
        except Exception as e:
            print(f'Error occurred {e}')
            
    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.host)
            return self.connection
        except Exception as e:
                print(f"Error occured {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()