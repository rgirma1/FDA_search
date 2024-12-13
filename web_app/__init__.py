from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register routes
    from web_app.routes.drugs_routes import drugs_bp
    app.register_blueprint(drugs_bp)

    return app
