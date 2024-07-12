import datetime
import hashlib
import os


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, 'r')
        self.users = {}

        for line in self.file:
            email,hash_pass,salt,name, created = line.strip().split(';')
            self.users[email] = (hash_pass,salt, name, created)

        self.file.close()
        

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            hash_password, salt = DataBase.hash_password(password)
            self.users[email.strip()] = (hash_password.strip(),
                                         salt.strip(),
                                         name.strip(), DataBase.get_date())
            self.save()

    def validate(self, email, password):
        for user in self.users:
            passw = DataBase.verificar(password,self.users[user][0],self.users[user][1])
        if self.get_user(email) != -1 and (passw is True):
            return passw
        else:
            print("Email exists already")
            return -1

    def save(self):
        with open(self.filename, 'w') as f:
            for user in self.users:
                f.write(f"{user};{self.users[user][0]};{self.users[user][1]};{self.users[user][2]};{self.users[user][3]}\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]

    @staticmethod
    def hash_password(password,salt=None):
        if salt is None:
            salt = os.urandom(16)
        password_salt = password + str(salt)
        sha_signature = hashlib.sha256(password_salt.encode()).hexdigest()
        return sha_signature,salt

    @staticmethod
    def verificar(password,hash,salt):
        hash_pass, _ = DataBase.hash_password(password, salt)
        # Verifica se o hash gerado corresponde ao hash verdadeiro
        return hash_pass == hash
