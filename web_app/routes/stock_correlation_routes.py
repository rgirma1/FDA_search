from flask import Blueprint, request, render_template, jsonify
from app.FDAdata import fetch_drug_data, fetch_device_data, process_pma_data, process_recall_data
from app.stockcorrelation import fetch_stocks_csv

stock_correlation_routes = Blueprint("stock_correlation", __name__)

@stock_correlation_routes.route("/stock-correlation")
def stock_correlation():
    return render_template("stock-correlation.html")

@stock_correlation_routes.route("/stock_correlation_dashboard", methods=["GET","POST"])
def stock_correlation_dashboard():

    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)
    
    symbol = request_data.get("symbol")
    company = request_data.get("company")

    stock = fetch_stocks_csv(symbol)
    
    drug_recall_data = fetch_drug_data("company", company)
    device_pma_data, device_recall_data = fetch_device_data("company", company)



    drugrecall = process_recall_data(drug_recall_data)
    devicerecall = process_recall_data(device_recall_data)
    pma = process_pma_data(device_pma_data)

    # insert code for timeframes

    # convert everything to dictionary
    stock = stock.to_dict("records")
    pma = pma.to_dict("records")

    return render_template("stock-correlation-dashboard.html", drug_recall_data=drugrecall, 
                            device_recall_data = devicerecall, pma_data = pma, 
                            stock_data = stock, symbol = symbol)