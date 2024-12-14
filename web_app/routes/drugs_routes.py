from flask import Blueprint, request, render_template, jsonify
from app.FDAdata import fetch_fda_data, process_pma_data, process_recall_data

drugs_bp = Blueprint("drugs", __name__)

@drugs_bp.route("/openFDA-Search/by-drug-device")
def by_drug_device():
    return render_template("by-drug-device.html")

@drugs_bp.route("/openFDA-Search/by-company")
def by_company():
    return render_template("by-company.html")

@drugs_bp.route("/search/drug", methods=["GET"])
def search_drug():
    drug_name = request.args.get("drug_name")
    if not drug_name:
        return jsonify({"error": "Drug name is required"}), 400

    pma_data, recall_data = fetch_fda_data(drug_name)

    if not pma_data or not recall_data:
        return jsonify({"error": "No data found for the drug"}), 404

    return render_template("results.html", drug_name=drug_name, pma_data=pma_data, recall_data=recall_data)

@drugs_bp.route("/search/device", methods=["GET"])
def search_device():
    company_name = request.args.get("company_name")
    keyword = request.args.get("keyword")

    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    pma_data, recall_data = fetch_fda_data(company_name)

    if not pma_data or not recall_data:
        return jsonify({"error": "No data found for the device"}), 404

    return render_template("results.html", company_name=company_name, keyword=keyword, pma_data=pma_data, recall_data=recall_data)
