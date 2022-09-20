import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='c5d5d5f3623e012d9abc911d2eefcc64147c8b9e6cdca08397d9f70eacbb5f08',
        DATABASE=os.path.join(app.instance_path, 'mysite.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import station
    app.register_blueprint(station.bp)

    return app
