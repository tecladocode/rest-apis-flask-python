# This defines the user object class

class User(object):
    def __init__(self,_id, username, password):
        self.id = _id
        self.username = username
        self.password = password
