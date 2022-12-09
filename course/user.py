import db

class User():
    def init_by_email(self, email):
        self.__user = db.get_user_by_email(email)
        return self

    def init_by_dict(self, user_dict):
        self.__user = user_dict
        print(self.__user)
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_user(self):
        return self.__user

    def get_name(self):
        return self.__user['name']

    def get_id(self):
        return str(self.__user['email'])
