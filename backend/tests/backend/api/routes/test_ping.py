def test_ping_should_respond_with_pong(app_test_client):
    response = app_test_client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
