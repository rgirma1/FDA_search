from flask import Blueprint, request, render_template, jsonify

stock_correlation_routes = Blueprint("stock_correlation", __name__)

@stock_correlation_routes.route("/stock-correlation")
def stock_correlation():
    return render_template("stock-correlation.html")