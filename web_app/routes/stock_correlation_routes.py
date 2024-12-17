from flask import Blueprint, request, render_template, jsonify, flash, redirect
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
    
    '''
    symbol = request_data.get("symbol")
    company = request_data.get("company")
    timeoffset = request_data.get("btndaterange")

    stock = fetch_stocks_csv(symbol)
    
    drug_recall_data = fetch_drug_data("company", company)
    device_pma_data, device_recall_data = fetch_device_data("company", company)



    drugrecall = process_recall_data(drug_recall_data)
    devicerecall = process_recall_data(device_recall_data)
    pma = process_pma_data(device_pma_data)

    print(pma.loc[pma['count'] == 14])

    # insert code for timeframes

    stock = date_range_filter(timeoffset, stock)
    pma = date_range_filter(timeoffset, pma)

    print(pma)
    print("---------------------")
    print(stock)

    # convert everything to dictionary
    stock = stock.to_dict("records")
    pma = pma.to_dict("records")

    return render_template("stock-correlation-dashboard.html", drug_recall_data=drugrecall, 
                            device_recall_data = devicerecall, pma_data = pma, 
                            stock_data = stock, symbol = symbol)'''

    try:
        # get data from form
        symbol = request_data.get("symbol")
        company = request_data.get("company")
        timeoffset = request_data.get("btndaterange")

        # error checking if data is filled
        if not symbol and not company and not timeoffset: # no search term
            raise Exception(f'Please enter all search criteria below!')

        # get stock data
        stock = fetch_stocks_csv(symbol, timeoffset)
        
        # get fda data
        drug_recall_data = fetch_drug_data("company", company)
        device_pma_data, device_recall_data = fetch_device_data("company", company)

        # error checking of no results from OpenFDA API
        if 'error' in drug_recall_data or 'error' in device_recall_data and 'error' in device_pma_data:
            raise Exception('OpenFDA API Error: No results found.')

        #
        # todo, convert timeoffset and process into one
        #
        # processing data in dataframes
        #drugrecall = process_recall_data(drug_recall_data)
        #devicerecall = process_recall_data(device_recall_data)
        pma = process_pma_data(device_pma_data, timeoffset)

        print(pma.loc[pma['count'] == 14])

        # insert code for timeframes


        print(pma)
        print("---------------------")
        print(stock)

        # convert everything to dictionary
        stock = stock.to_dict("records")
        pma = pma.to_dict("records")
        
        flash("Fetched openFDA and AlphaVantage API data!", "success")
        
        # returns data as dataframes
        return render_template("stock-correlation-dashboard.html", 
                                drug_recall_data=drugrecall, 
                                device_recall_data = devicerecall, 
                                pma_data = pma, 
                                stock_data = stock, 
                                symbol = symbol)

    except Exception as err:
        print('OOPS', err)

        flash(str(err), "danger")
        return redirect("/openFDA-Search/drug-recalls")