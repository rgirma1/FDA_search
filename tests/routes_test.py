import pytest
from web_app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

def test_search_drug(client):
    response = client.get("/search/drug?drug_name=aspirin")
    assert response.status_code == 200

def test_search_device(client):
    response = client.get("/search/device?company_name=medtronic&keyword=pacemaker")
    assert response.status_code == 200
