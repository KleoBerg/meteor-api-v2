from flask import Flask
from .config import Config
from .flaskdgraph import DGraph
import atexit

dgraph = DGraph()
atexit.register(dgraph.close)

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)


    dgraph.init_app(app)

    from .main.routes import main_bp
    app.register_blueprint(main_bp)

    return app