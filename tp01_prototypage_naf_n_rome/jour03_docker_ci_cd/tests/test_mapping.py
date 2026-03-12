import pytest


def test_list_rome(client):
    response = client.get("/api/v1/rome")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0


def test_list_naf(client):
    response = client.get("/api/v1/naf")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0


def test_get_rome_by_code(client):
    response = client.get("/api/v1/rome/M1805")
    assert response.status_code == 200
    data = response.json()
    assert data["rome"]["code_rome"] == "M1805"


def test_get_rome_not_found(client):
    response = client.get("/api/v1/rome/XXXXX")
    assert response.status_code == 404


def test_get_naf_by_code(client):
    response = client.get("/api/v1/naf/62.01Z")
    assert response.status_code == 200
    data = response.json()
    assert "naf" in data


def test_search_keyword(client):
    response = client.post("/api/v1/search", json={"query": "informatique", "limit": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert len(data["results"]) > 0


def test_search_too_short(client):
    response = client.post("/api/v1/search", json={"query": "a", "limit": 5})
    assert response.status_code == 422  # Validation error


def test_mapping_rome_to_naf(client):
    response = client.get("/api/v1/mapping/rome-to-naf/M1805")
    assert response.status_code == 200
    data = response.json()
    assert "naf_suggestions" in data
    assert len(data["naf_suggestions"]) > 0


def test_mapping_naf_to_rome(client):
    response = client.get("/api/v1/mapping/naf-to-rome/62.01Z")
    assert response.status_code == 200
    data = response.json()
    assert "rome_suggestions" in data


def test_pagination(client):
    response = client.get("/api/v1/rome?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) <= 2
