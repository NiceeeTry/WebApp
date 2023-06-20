import mysql.connector

class UseDataBase:
    def __init__(self, db :dict)->None:
        self.dbconfig = db
        
    def __enter__(self):
        pass
    def __exit(self):
        pass