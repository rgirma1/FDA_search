from flask import Blueprint, request, render_template, flash, jsonify
from app.FDAdata import fetch_drug_data, fetch_device_data, process_pma_data, process_recall_data
import pandas as pd

fdadata_routes = Blueprint("fdadata_routes", __name__)

@fdadata_routes.route("/openFDA-Search/drug")
@fdadata_routes.route("/openFDA-Search/drug-recalls")
def drug_recalls():
    return render_template("drug-recalls.html")

@fdadata_routes.route("/openFDA-Search/device")
@fdadata_routes.route("/openFDA-Search/device-recalls-pma")
def device_recalls_pma():
    return render_template("device-recalls-pma.html")


# result forms

@fdadata_routes.route("/search_drug", methods=["GET"])
def search_result_drug():
    search_type = request.args.get("search_type")
    search_term = request.args.get("search_term")
    if not search_term:
        raise Exception(f'Please enter a {search_type}')
    recall_data = fetch_drug_data(search_type, search_term)

    if 'error' in recall_data:
        raise Exception('No results found.')

    return render_template("results-drug.html", search_type=search_type, search_term=search_term, recall_data=recall_data)

@fdadata_routes.route("/search_device", methods=["GET"])
def search_result_device():
    search_type = request.args.get("search_type")
    search_term = request.args.get("search_term")
    if not search_term:
        return jsonify({"error": "Search term is required"}), 400

    pma_data, recall_data = fetch_device_data(search_type, search_term)

    if not recall_data:
        return jsonify({"error": "No data found for the drug"}), 404

    return render_template("results-device.html", search_type=search_type, search_term=search_term, pma_data=pma_data, recall_data=recall_data)