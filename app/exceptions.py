class FieldError(Exception):
    def __init__(self, data):
        self.message = { 'error': 'wrong fields' }

class UserAlreadyExistsError(Exception):
    def __init__(self):
        self.message = {'error': 'User already exists.'}