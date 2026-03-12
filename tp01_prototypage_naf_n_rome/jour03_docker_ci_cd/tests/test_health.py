def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert data["records_loaded"] > 0


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "docs" in response.json()


def test_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "naf_rome_records_total" in data
    assert data["api_status"] == 1
