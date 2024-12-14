from flask import Blueprint, request, render_template, jsonify
from app.FDAdata import fetch_fda_data, process_pma_data, process_recall_data

news_routes = Blueprint("news", __name__)

@news_routes.route("/news")
def news():
    return render_template("news.html")