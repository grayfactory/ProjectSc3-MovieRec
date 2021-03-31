class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://oxyjeoubcrvgnd:cda41dbcc9da52941de12e3dc61ade0c2fcb77e34aff7619ed0ee04e9568aa57@ec2-54-211-176-156.compute-1.amazonaws.com:5432/d441brlclr7kf'