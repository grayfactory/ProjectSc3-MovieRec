class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://mzbuxreehwuhgg:f36fecc4cc60b12856fbf06006a8f81855e77f231027c38f7a2aaaaa7ef243eb@ec2-3-233-43-103.compute-1.amazonaws.com:5432/d6fu8hgt6rr79c'