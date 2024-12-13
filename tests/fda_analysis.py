
from app.main import fetch_fda_data, process_pma_data, process_recall_data

# Mock PMA and Recall API responses
mock_pma_response = {
    "meta": {"results": {"total": 2}},
    "results": [
        {"decision_date": "2023-01-01", "decision_code": "APPR"},
        {"decision_date": "2023-02-01", "decision_code": "APPR"}
    ]
}

mock_recall_response = {
    "meta": {"results": {"total": 2}},
    "results": [
        {"event_date_posted": "2023-01-01"},
        {"event_date_posted": "2023-02-01"}
    ]
}

class MockResponse:
    """
    Mock object to simulate API responses.
    """
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

@patch('app.main.requests.get')
def test_fetch_fda_data(mock_get):
    """
    Test fetching FDA data using mocked API responses.
    """
    # Simulate API responses
    def mock_side_effect(url):
        if "pma" in url:
            return MockResponse(mock_pma_response)
        elif "recall" in url:
            return MockResponse(mock_recall_response)
        return MockResponse({}, status_code=404)

    mock_get.side_effect = mock_side_effect

    # Test the fetch function
    pma_data, recall_data = fetch_fda_data("Abbott Laboratories")

    assert pma_data["meta"]["results"]["total"] == 2
    assert recall_data["meta"]["results"]["total"] == 2

def test_process_pma_data():
    """
    Test processing PMA data into a DataFrame.
    """
    df = process_pma_data(mock_pma_response["results"])

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "decision_date" in df.columns
    assert "decision_code" in df.columns

def test_process_recall_data():
    """
    Test processing recall data into a DataFrame.
    """
    df = process_recall_data(mock_recall_response["results"])

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "event_date_posted" in df.columns