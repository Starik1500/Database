import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456789@localhost/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False