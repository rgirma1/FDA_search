from flask import Blueprint, request, render_template, jsonify
from app.FDAdata import fetch_fda_data, process_pma_data, process_recall_data

stock_correlation_routes = Blueprint("stock_correlation", __name__)

@stock_correlation_routes.route("/stock-correlation")
def stock_correlation():
    return render_template("stock-correlation.html")