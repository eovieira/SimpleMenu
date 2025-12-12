from flask import Flask
from flask_session import Session
from routes.auth import auth_bp
from routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'MINHACHAVEMUITOSECRETAEPERFEITA'
    app.config["SESSION_TYPE"] = 'filesystem'
    Session(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
