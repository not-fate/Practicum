import threading
import utilities


class Authentication:
    def __init__(self):
        self.logins = utilities.read_dic("server_logins.csv")
        self.admin_login = "admin"
        self.admin_pass = "admin"
        self.lock = threading.Lock()

    def add_user(self, login: str, password: str) -> bool:
        with self.lock:
            if login in self.logins:
                return False
            self.logins[login] = password
            utilities.write_dic("server_logins.csv", self.logins)
            return True

    def check_login(self, login: str, password: str):
        with self.lock:
            if login is None or password is None:
                return 0
            if login == self.admin_login and password == self.admin_pass:
                return 2
            if login in self.logins and self.logins[login] == password:
                return 1
            return 0

