import requests

cookies = {
    '__cf_bm': 'YkMbbTCO0X3QoR62nKzJi70V6SfgSUGKz5WZaTYYMd4-1738247827-1.0.1.1-HlJG9k3o1QEgRBTjxdFUDE4RTiW3IlnlghrNzBl2xbEKEEW7UhLW66FN_cZg5q6RAN2eH5o68h9i0GCsGxS4wA',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'app_version': '9.2.15',
    'appid': '30004',
    'appsiteid': '0',
    'authorization': 'Bearer eyJicyI6MCwiYWlkIjoxMDAwOSwicGlkIjoiMzAiLCJzaWQiOiJhM2JmYWE4MzFiOWUxYzc5MGJjYjBkYmNjMjM3YTFmMiIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiIxMzc5MzM1NzcyNDUxNDk1OTQxIiwiZXhwIjoxNzM4Njc5ODM5LCJqdGkiOiIxZGZmYjNhOC02ZjU1LTQ0OTYtOWZhNi02NDQ5ODdjNjQ0MDMifQ.t51lrJYfjCd-N9iLjB7It47ku6imK-cchk42QPIWf5IrUjsuI1PsX6OWLvvFkoIw5uucuSlNQrlcbuFRPz5ngA',
    'channel': 'official',
    'content-type': 'application/json',
    # 'cookie': '__cf_bm=YkMbbTCO0X3QoR62nKzJi70V6SfgSUGKz5WZaTYYMd4-1738247827-1.0.1.1-HlJG9k3o1QEgRBTjxdFUDE4RTiW3IlnlghrNzBl2xbEKEEW7UhLW66FN_cZg5q6RAN2eH5o68h9i0GCsGxS4wA',
    'device_brand': 'Linux_Chrome_132.0.0.0',
    'device_id': '6f76e02b64ba4a078a331eb5c323913b',
    'lang': 'ru-RU',
    'mainappid': '10009',
    'origin': 'https://bingx.paycat.com',
    'platformid': '30',
    'priority': 'u=1, i',
    'referer': 'https://bingx.paycat.com/',
    'reg_channel': 'official',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sign': '3CEFB4B1B8B7FF82080D092FB1D68F3B7DC5E91FAFB3CD885636FAB9889FD3A3',
    'timestamp': '1738247933539',
    'timezone': '3',
    'traceid': 'e2f42528383e4bc095151a9f501f57fd',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

json_data = {
    'advertNo': '1383430032238764040',
    'asset': 'USDT',
    'fiat': 'RUB',
    'type': 1,
    'userPrice': 103,
    'areaType': 2,
    'amount': '500',
    'paymentMethodId': 110,
}

response = requests.post('https://api-app.qq-os.com/api/c2c/v1/order/create', cookies=cookies, headers=headers, json=json_data)
print(response.text)
