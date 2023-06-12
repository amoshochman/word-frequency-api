from app import app, TOP, MINIMUM, MEDIAN


def test_stats_endpoint():
    client = app.test_client()
    client.post('/words', data='ball,eggs,pool,dart,ball,ball')
    client.post('/words', data='table,eggs,pool,mouse,ball,eggs')
    client.post('/words', data='table,mouse')
    response = client.get('/stats')
    assert response.status_code == 200
    data = response.get_json()
    top_5 = data[TOP]
    assert type(top_5) == list and len(top_5) == 5
    assert top_5[0] == 'ball 4' and top_5[1] == 'eggs 3' and set(top_5[2:]) == {'mouse 2', 'pool 2', 'table 2'}
    assert data[MINIMUM] == 1
    assert data[MEDIAN] == 2
