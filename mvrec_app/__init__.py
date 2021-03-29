from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

db = SQLAlchemy() # factory pattern 에서는 app을 넣지 않고 생성
migrate = Migrate() # 일단 migrate는 하지 말고

def create_app(config=None):

    app = Flask(__name__)

    # app.config["ENV"]='development'

    if app.config["ENV"] == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')
    if config is not None:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db
    # , render_as_batch=True
    )

    # 라우트 blueprint 등록
    from mvrec_app.routes import (main_route, rating_route, delete_route, keep_route)
    app.register_blueprint(main_route.bp)
    app.register_blueprint(rating_route.bp, url_prefix='/api')
    app.register_blueprint(delete_route.bp, url_prefix='/api')
    app.register_blueprint(keep_route.bp, url_prefix='/api')

    # print(app.root_path)
    # db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)