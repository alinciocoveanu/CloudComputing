from concurrent.futures import ThreadPoolExecutor
import requests


def make_request(id):
    # print('Thread id:', id)
    try:
        url = 'http://127.0.0.1:5000/getJoke/'
        response = requests.request('GET', url)
        response.raise_for_status()
    except Exception as e:
        print(str(e))


for i in range(5):
    with ThreadPoolExecutor(max_workers=2) as executor:
        for _ in executor.map(make_request, range(5)):
            pass
