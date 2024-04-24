from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Sysarch' #Secure the session, cookies, and important data

    # use .(dot) instead of /(slash)
    from .views.auth import auth
    
    app.register_blueprint(auth, url_prefix='/auth/')

    return app;