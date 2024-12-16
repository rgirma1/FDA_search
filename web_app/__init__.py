from flask import Flask
from web_app.routes.home_routes import home_routes
from web_app.routes.fdadata_routes import fdadata_routes
from web_app.routes.stock_correlation_routes import stock_correlation_routes

def create_app():
    app = Flask(__name__)

    # Register routes
    
    app.register_blueprint(home_routes)
    app.register_blueprint(fdadata_routes)
    app.register_blueprint(stock_correlation_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
