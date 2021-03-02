# In[82]:

class Error(Exception):
    pass


class NoSuchFolder(Error):
    def __init__(self):
        self.code = 400
        self.message = 'Folder does not exist.'
    
class NoSuchFile(Error):
    def __init__(self):
        self.code = 400
        self.message = 'Cannot find file at path.'
    
class ElementAlreadyExists(Error):
    def __init__(self):
        self.code = 400
        self.message = 'Element already exists. Please delete existing element, or pick a new path.'

class DatabaseError(Error):
    def __init__(self):
        self.code = 500
        self.message = 'Database Error.'

class UnknownServerError(Error):
    def __init__(self):
        self.code = 500
        self.message = 'Please report to DevOps.'


class NoFileSent(Error):
    def __init__(self):
        self.code = 400
        self.message = 'No file sent.'