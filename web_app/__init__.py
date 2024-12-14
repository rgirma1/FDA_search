from flask import Flask
from web_app.routes.home_routes import home_routes
from web_app.routes.news_routes import news_routes
from web_app.routes.drugs_routes import drugs_bp
from web_app.routes.stock_correlation_routes import stock_correlation_routes

def create_app():
    app = Flask(__name__)

    # Register routes
    
    app.register_blueprint(home_routes)
    app.register_blueprint(news_routes)
    app.register_blueprint(drugs_bp)
    app.register_blueprint(stock_correlation_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
