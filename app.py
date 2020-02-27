from flask import Flask, render_template, request
from request_apis import test_requests
from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler
import json
from time import strftime
import traceback

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
elapsed_time = timedelta()

successful_requests = 0
total_requests = 0



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/metrics')
def getMetrics():
    return render_template('metrics.html')


@app.route('/getJoke/')
def getJoke():
    global elapsed_time, total_requests, successful_requests
    response = test_requests()
    total_requests += 1
    if response != -1:
        joke, entity, url, elapsed = response
        my_dict = {'JOKE': joke, 'ENTITY': entity, 'URL': url}
        elapsed_time += elapsed
        successful_requests += 1
        return json.dumps(my_dict)
    else:
        return json.dumps({'JOKE': 'Please try again.', 'ENTITY': 'Request failed', 'URL': 'static/img/image_1.jpg'})


@app.route('/getMetrics/')
def metrics():
    global total_requests, successful_requests, elapsed_time
    try:
        return json.dumps({'LATENCY': round(elapsed_time.seconds / successful_requests, 1),
                           'SUCCESS_RATE': '{:.1%}'.format(successful_requests / total_requests),
                           'TOTAL_REQUESTS': total_requests, 'SUCCESSFUL_REQUESTS': successful_requests})
    except ZeroDivisionError:
        return json.dumps({'LATENCY': 0, 'SUCCESS_RATE': 0, 'TOTAL_REQUESTS': 0, 'SUCCESSFUL_REQUESTS': 0})


@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return e.status_code


# if __name__ == '__main__':
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
logger = logging.getLogger('tdm')
logger.setLevel(logging.ERROR)
logger.addHandler(handler)
app.run(host='127.0.0.1', debug=True)
