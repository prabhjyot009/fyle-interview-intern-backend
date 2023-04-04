def Server_check(client):
    response = client.get(
        '/'
    )

    assert response.status_code == 200

    res = response.json
    assert res['status'] == 'on'