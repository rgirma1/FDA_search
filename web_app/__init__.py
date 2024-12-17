
import os
from flask import Flask
from web_app.routes.home_routes import home_routes
from web_app.routes.fdadata_routes import fdadata_routes
from web_app.routes.stock_correlation_routes import stock_correlation_routes


SECRET_KEY = os.getenv("SECRET_KEY", default="super secret") # set this to something else on production!!!

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    # Register routes
    
    app.register_blueprint(home_routes)
    app.register_blueprint(fdadata_routes)
    app.register_blueprint(stock_correlation_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
