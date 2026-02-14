import requests

BASE_URL = 'http://127.0.0.1:8000'

def test_create_order_success():
    url = BASE_URL + '/orders'
    headers = {'Authorization': 'Bearer testtoken'}
    params = {}
    resp = requests.post(url, json={'item_id': 'A1', 'quantity': 2}, headers=headers, params=params)
    assert resp.status_code == 201
    assert resp.json().get('item_id') == 'A1'
