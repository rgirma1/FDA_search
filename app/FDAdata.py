#this is the app/OPENFDA_data file..

import requests
import pandas as pd
import datetime
import plotly.express as px
from dateutil.relativedelta import relativedelta

pd.options.mode.copy_on_write = True

def fetch_drug_data(type, search_term):
    '''
    Fetch drug recall data from OpenFDA API

    Args:
        type (str): type of search term used ("company" or "drug")
        search_term (str): input by the user

    Returns:
        recall_data (json)

    '''
    
    # request data from openFDA API
    search_term = search_term.replace(" ", "+")

    if type == "company":
        recall_query = f'https://api.fda.gov/drug/enforcement.json?search=recalling_firm:"{search_term}"&sort=recall_initiation_date:desc&limit=10'
    elif type == "drug":
        recall_query = f'https://api.fda.gov/drug/enforcement.json?search=product_description:"{search_term}"&sort=recall_initiation_date:desc&limit=10'
        
    recall_response = requests.get(recall_query)
    recall_data = recall_response.json()

    # gets the results portion of recall data json, otherwise returns json with error
    if "error" not in recall_data:
        recall_data = recall_data["results"]

    return recall_data

def fetch_device_data(type, search_term):
    '''
    Fetch device recall and pma data from OpenFDA API

    Args:
        type (str): type of search term used ("company" or "device")
        search_term (str): input by the user

    Returns:
        recall_data (json)
        pma_data (json)

    '''
    # request data from openFDA API
    search_term = search_term.replace(" ", "+")

    if type == "company":
        pma_query = f'https://api.fda.gov/device/pma.json?search=applicant:"{search_term}"&sort=decision_date:desc&limit=1000'
        recall_query = f'https://api.fda.gov/device/recall.json?search=recalling_firm:"{search_term}"&sort=event_date_posted:desc&limit=1000'
    elif type == "device":
        pma_query = f'https://api.fda.gov/device/pma.json?search=trade_name:"{search_term}"&sort=decision_date:desc&limit=1000'
        recall_query = f'https://api.fda.gov/device/recall.json?search=product_description:"{search_term}"&sort=event_date_posted:desc&limit=1000'

    pma_response = requests.get(pma_query)
    recall_response = requests.get(recall_query)

    pma_data =  pma_response.json()
    recall_data = recall_response.json()

    # gets the results portion of data json, otherwise returns json with error
    if "error" not in pma_data:
        pma_data = pma_data["results"]

    if "error" not in recall_data:
        recall_data = recall_data["results"]

    return pma_data, recall_data
    
def process_pma_data(pma_data, time):
    """
    Process PMA data into a pandas DataFrame.

    Args:
        pma_data (list): List of PMA records.
        cutoff: how many months of a data

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    # turn pma data json into a dataframe
    df = pd.DataFrame(pma_data)

    # convert decision_date column into datetime
    df['decision_date'] = pd.to_datetime(df['decision_date'].astype("string"))

    # Get today's date
    today = pd.Timestamp(datetime.now().date())

    # converting time from radio button into number of months (m)
    m = int(time)
    '''if time == "1M": m = 1
    if time == "6M": m = 6
    if time == "1Y": m = 12
    if time == "5Y": m = 60    '''

    # Calculate the offset
    m_months_ago = today - pd.DateOffset(months=m)
    
    # ------------------------
    # FILTERING USING DATETIME
    # ------------------------
     # filtering the data till m months ago
    df = df[(df['decision_date'] >= m_months_ago) & (df['decision_date'] <= today)]
    # filter data for pma approvals
    df = df[(df['decision_code'] == "APPR") | (df['decision_code'] == "OK30") | (df['decision_code'] == "LE30")]

    # ------------------------
    # Grouping
    # ------------------------
    # group PMAs by date
    approvals_by_date = df.groupby(df['decision_date'].dt.date).size().reset_index(name='count')
    approvals_by_date = approvals_by_date.sort_values(by=['decision_date'])
    
    # convert decision_date column into datetime
    approvals_by_date['timestamp'] = pd.to_datetime(df['decision_date'].astype("string"))

    # only get timestamp and count
    df = df[['timestamp','count']]

    return approvals_by_date

def process_recall_data(recall_data):
    """
    Process recall data into a pandas DataFrame.

    Args:
        recall_data (list): List of recall records.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    df = pd.DataFrame(recall_data)

    if "event_date_initiated" in df.columns:
        df.rename(columns={"event_date_initiated": "recall_initiation_date"}, inplace=True)
    
    df['recall_initiation_date'] = pd.to_datetime(df['recall_initiation_date'].astype("string"))
    recalls_by_date = df.groupby(df['recall_initiation_date'].dt.date).size().reset_index(name='count')

    return recalls_by_date