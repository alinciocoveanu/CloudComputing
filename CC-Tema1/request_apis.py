from datetime import timedelta
import requests
import json


config = json.load(open('static/config.json', 'r'))

NOT_OK = -1
OK_CODE = 200
logs = ''

elapsed_time = timedelta()


def request_joke():
    url = "https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,racist"
    global elapsed_time

    querystring = {"format": "json"}

    response = requests.request("GET", url, params=querystring)
    if response.status_code == OK_CODE:
        response_joke = response.json()

        if response_joke['type'] == 'single':
            joke = response_joke['joke']
        else:
            joke = response_joke['setup'] + '\n' + response_joke['delivery']
        elapsed_time += response.elapsed
        return joke
    else:
        print('Joke request failed:', response.status_code)
        raise requests.RequestException


def request_entity_extraction(text):
    url = "https://aylien-text.p.rapidapi.com/entities"
    global elapsed_time

    querystring = {"text": text}

    response = requests.request("GET", url, headers=config['rapidapi'], params=querystring)
    if response.status_code == OK_CODE:
        response_entities = response.json()['entities']

        my_list = []
        for i in response_entities.values():
            my_list += i
        elapsed_time += response.elapsed
        return my_list
    else:
        print('Entity extraction request failed:', response.status_code)
        raise requests.RequestException


def request_image(text):
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    querystring = {"q": text, "license": "public", "imageType": "photo"}
    global elapsed_time

    response = requests.get(search_url, headers=config['bing-search'], params=querystring)

    if response.status_code == OK_CODE:
        search_results = response.json()
        thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:16]]
        elapsed_time += response.elapsed
        return thumbnail_urls
    else:
        print('Image search request failed:', response.status_code)
        raise requests.RequestException


def request_random_number(minn, maxx):
    url = 'https://api.random.org/json-rpc/2/invoke'
    global elapsed_time

    headers = {'content-type': 'application/json'}
    data = {
            "jsonrpc": "2.0",
            "method": "generateIntegers",
            "params": {
                "apiKey": config['random-org'],
                "n": 1,
                "min": minn,
                "max": maxx,
                "replacement": True
            },
            "id": 421
        }

    response = requests.request('POST', url, headers=headers, data=json.dumps(data))
    if response.status_code == OK_CODE:
        number = response.json()

        if 'error' in number:
            print('Random number generation request failed:')
            print(number['error']['code'])
            print(number['error']['message'])
            print(number['error']['data'])
            raise requests.RequestException
        elapsed_time += response.elapsed
        return number['result']['random']['data'][0]
    else:
        print('Random number generation request failed:', response.status_code)
        raise requests.RequestException


def test_requests():
    global elapsed_time
    try:
        joke = request_joke()
        entity_list = request_entity_extraction(joke)
        entity = entity_list[request_random_number(0, len(entity_list) - 1)]
        url_list = request_image(entity)
        entity = entity[0].upper() + entity[1:]
        url = url_list[request_random_number(0, len(url_list) - 1)]

        return joke, entity, url, elapsed_time
    except requests.RequestException:
        return NOT_OK
    finally:
        elapsed_time = timedelta()
