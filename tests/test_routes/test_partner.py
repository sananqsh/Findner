from app.main import app 
from fastapi.testclient import TestClient
client = TestClient(app)

def test_create_partner():
    payload = {
        "id": "1",
        "tradingName": "Test Partner",
        "ownerName": "John Doe",
        "document": "123456789/abcdef.something",
        "coverageArea": {
            "type": "MultiPolygon",
            "coordinates": [
                [[[30, 20], [45, 40], [10, 40], [30, 20]]],
                [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
            ]
        },
        "address": {
            "type": "Point",
            "coordinates": [-46.57421, -21.785741]
        }
    }

    # Success scenario
    response = client.post("/partners/", json=payload)

    assert response.status_code == 201
    assert response.json()["id"] == "1"
    assert response.json()["tradingName"] == "Test Partner"
    assert response.json()["document"] == "123456789/abcdef.something"
    assert response.json()["coverageArea"]["type"] == "MultiPolygon"

    # Dupicate document scenario
    response = client.post("/partners/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Document already registered"

    # Existing id scenario
    payload["document"] += "new-document/1234.notDuplicate"
    response = client.post("/partners/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Id already exists"

    # Resolved duplication scenario
    payload["id"] = "11"
    response = client.post("/partners/", json=payload)
    assert response.status_code == 201


def test_read_partners():
    response = client.get("/partners/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_nearest_covering_partner():
    response = client.get("/partners/nearest?long=123.456&lat=12.345")

    assert response.status_code == 404
    assert response.json()["detail"] == "Partner not found"

    # Success scenario
    response = client.get("/partners/nearest?long=30&lat=30")

    assert response.status_code == 200
    assert response.json()["id"] == "1"
    assert response.json()["tradingName"] == "Test Partner"

    # Creating a new Partner with same coverageArea, but closer in longitude
    payload = {
        "id": "2",
        "tradingName": "Harry Somethinger",
        "ownerName": "Ab Boss",
        "document": "987/abc.something-new",
        "coverageArea": {
            "type": "MultiPolygon",
            "coordinates": [
                [[[30, 20], [45, 40], [10, 40], [30, 20]]],
                [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
            ]
        },
        "address": {
            "type": "Point",
            "coordinates": [-20.57421, -21.785741]
        }
    }

    response = client.post("/partners/", json=payload)

    # Returns nearer Partner
    response = client.get("/partners/nearest?long=30&lat=30")

    assert response.status_code == 200
    assert response.json()["id"] == "2"
    assert response.json()["tradingName"] == "Harry Somethinger"
