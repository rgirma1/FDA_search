from app.FDAdata import fetch_drug_data, fetch_device_data, process_pma_data, process_recall_data

from pandas import DataFrame


def test_fetch_drug_data():
    drug_data_pfizer = fetch_drug_data("company", "Pfizer")
    drug_data_zemplar = fetch_drug_data("drug", "zemplar")

    assert drug_data_pfizer[0]["recalling_firm"] == "Pfizer Inc."
    assert drug_data_zemplar[0]["openfda"]["brand_name"][0] == "ZEMPLAR"

def test_fetch_device_data():
    pma_pfizer, recall_pfizer = fetch_device_data("company", "Pfizer")
    
    assert pma_pfizer[0]["applicant"] == "PFIZER, INC."
    assert recall_pfizer[0]["recalling_firm"] == "Pfizer Global"

def test_process_recall_data():
    drug_data_zemplar = fetch_drug_data("drug", "zemplar")
    df = process_recall_data(drug_data_zemplar, "60")

    assert df.columns.tolist() ==  ['timestamp','count']

def test_process_pma_data():
    pma_pfizer, recall_pfizer = fetch_device_data("company", "Pfizer")
    df = process_pma_data(pma_pfizer, "60")

    assert df.columns.tolist() ==  ['timestamp','count']