from flask import Flask, render_template
from request_apis import test_requests
from datetime import timedelta
import json

app = Flask(__name__)
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
