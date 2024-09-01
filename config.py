import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '302cd2dde38138bed7925ea88becdb73'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# "qFfZVVQnPnKh8GZ5Th2RRsq2Cqnc6wAf9wbrFyBLwC9uG74Sruk4RFxbeyfg79ue"