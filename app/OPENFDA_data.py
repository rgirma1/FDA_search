#this is the app/OPENFDA_data file..

import requests
import pandas as pd
import plotly.express as px

pd.options.mode.copy_on_write = True

def fetch_fda_data(company):
    """
    Fetch PMA and recall data for a medical company from OpenFDA.

    Args:
        company (str): The name of the medical company.

    Returns:
        tuple: JSON data for PMAs and recalls.
    """
    company = company.replace(" ", "+")
    pma_query = f'https://api.fda.gov/device/pma.json?search=applicant:"{company}"&sort=decision_date:desc&limit=1000'
    recall_query = f'https://api.fda.gov/device/recall.json?search=recalling_firm:"{company}"&sort=event_date_posted:desc&limit=1000'

    pma_response = requests.get(pma_query)
    recall_response = requests.get(recall_query)

    if pma_response.status_code == 200 and recall_response.status_code == 200:
        return pma_response.json(), recall_response.json()
    return None, None

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