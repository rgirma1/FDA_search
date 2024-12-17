from flask import Blueprint, request, render_template, flash, jsonify, redirect
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
    #  gets data from form
    search_type = request.args.get("search_type")
    search_term = request.args.get("search_term")

    try:
        # error checking of no search term
        if not search_term: # no search term
            raise Exception(f'Please enter a {search_type} to search for!')

        # retrieving fda data using fetch_drug_data function
        recall_data = fetch_drug_data(search_type, search_term)

        # error checking of no results from OpenFDA API
        if 'error' in recall_data:
            raise Exception('OpenFDA API Error: No results found.')

        # getting first 10 results
        recall_data = recall_data[:10]

        flash("Fetched Drug Recall Data!", "success")
        
        # returns search_type, search_term, and data as jsons
        return render_template("results-drug.html", 
                                search_type=search_type, 
                                search_term=search_term, 
                                recall_data=recall_data)

    except Exception as err:
        print('OOPS', err)

        flash(str(err), "danger")
        return redirect("/openFDA-Search/drug-recalls")

@fdadata_routes.route("/search_device", methods=["GET"])
def search_result_device():
    #  gets data from form
    search_type = request.args.get("search_type")
    search_term = request.args.get("search_term")
    
    try:
        # error checking of no search term
        if not search_term: # no search term
            raise Exception(f'Please enter a {search_type} to search for!')

        # retrieving fda data using fetch_device_data function
        pma_data, recall_data = fetch_device_data(search_type, search_term)

        # error checking of no results from OpenFDA API
        if 'error' in recall_data and 'error' in pma_data:
            raise Exception('OpenFDA API Error: No results found.')
        
        # getting first 10 results
        if 'error' not in recall_data:
            recall_data = recall_data[:10]
        if 'errpr' not in pma_data:
            pma_data = pma_data[:10]

        flash("Fetched Drug Recall Data!", "success")

        # returns search_type, search_term, and data as jsons
        return render_template("results-device.html", 
                                search_type=search_type, 
                                search_term=search_term, 
                                pma_data=pma_data, 
                                recall_data=recall_data)
    
    except Exception as err:
        print('OOPS', err)

        flash(str(err), "danger")
        return redirect("/openFDA-Search/device-recalls-pma")