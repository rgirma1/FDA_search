from flask import Blueprint, request, render_template, jsonify

news_routes = Blueprint("news", __name__)

@news_routes.route("/news")
def news():
    return render_template("news.html")