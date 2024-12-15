#this is the app/OPENFDA_data file..

import requests
import pandas as pd
import plotly.express as px

pd.options.mode.copy_on_write = True

def fetch_drug_data(type, search_term):
    """
    Fetch PMA and recall data for a medical company from OpenFDA.

    Args:
        
        type (str): type of search (limited to: 'company', 'drug', 'device')
        search (str): The name of the medical company.

    Returns:
        tuple: JSON data for PMAs and recalls.
    """
    
    search_term = search_term.replace(" ", "+")

    if type == "company":
        recall_query = f'https://api.fda.gov/drug/enforcement.json?search=recalling_firm:"{search_term}"&sort=recall_initiation_date:desc&limit=10'
    elif type == "drug":
        recall_query = f'https://api.fda.gov/drug/enforcement.json?search=product_description:"{search_term}"&sort=recall_initiation_date:desc&limit=10'
        
    recall_response = requests.get(recall_query)
    recall_data = recall_response.json()

    if "error" not in recall_data:
        recall_data = recall_data["results"]

    return recall_data

def fetch_device_data(type, search_term):
    """
    Fetch PMA and recall data for a medical company from OpenFDA.

    Args:
        
        type (str): type of search (limited to: 'company', 'drug', 'device')
        search (str): The name of the medical company.

    Returns:
        tuple: JSON data for PMAs and recalls.
    """
    
    search_term = search_term.replace(" ", "+")

    if type == "company":
        pma_query = f'https://api.fda.gov/device/pma.json?search=applicant:"{search_term}"&sort=decision_date:desc&limit=10'
        recall_query = f'https://api.fda.gov/device/recall.json?search=recalling_firm:"{search_term}"&sort=event_date_posted:desc&limit=10'
    elif type == "device":
        pma_query = f'https://api.fda.gov/device/pma.json?search=trade_name:"{search_term}"&search=decision_code:"APPR"$sort=decision_date:desc&limit=10'
        recall_query = f'https://api.fda.gov/device/recall.json?search=product_description:"{search_term}"&sort=event_date_posted:desc&limit=10'

    pma_response = requests.get(pma_query)
    recall_response = requests.get(recall_query)

    pma_data =  pma_response.json()
    recall_data = recall_response.json()

    if "error" not in pma_data:
        pma_data = pma_data["results"]

    if "error" not in recall_data:
        recall_data = recall_data["results"]

    return pma_data, recall_data
    
def process_pma_data(pma_data):
    """
    Process PMA data into a pandas DataFrame.

    Args:
        pma_data (list): List of PMA records.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    df = pd.DataFrame(pma_data)
    df['decision_date'] = pd.to_datetime(df['decision_date'].astype("string"))
    return df[df['decision_code'] == "APPR"]

def process_recall_data(recall_data):
    """
    Process recall data into a pandas DataFrame.

    Args:
        recall_data (list): List of recall records.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    df = pd.DataFrame(recall_data)
    df['event_date_posted'] = pd.to_datetime(df['event_date_posted'].astype("string"))
    return df

def plot_data(df, date_column, count_column, title, x_label, y_label):
    """
    Plot data using Plotly.

    Args:
        df (pd.DataFrame): DataFrame to plot.
        date_column (str): Date column name.
        count_column (str): Count column name.
        title (str): Plot title.
        x_label (str): X-axis label.
        y_label (str): Y-axis label.
    """
    counts_by_date = df.groupby(df[date_column].dt.date).size().reset_index(name=count_column)
    fig = px.line(counts_by_date, x=date_column, y=count_column, title=title, labels={date_column: x_label, count_column: y_label})
    fig.show()