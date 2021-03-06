import socket
from time import sleep
import logging as log
import threading
import random
from flask import Flask, render_template, Response, request
from prometheus_client import start_http_server, Histogram, MetricsHandler, Counter, generate_latest
from prometheus_client.exposition import _ThreadingSimpleServer, start_http_server
_ThreadingSimpleServer.daemon_threads = True


app = Flask(__name__)
PROMETHEUS_PORT = 9000
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

# Create a metric to track time spent and requests made.
REQUEST_TIME = Histogram('dummy_flask_request_time', 'DESC: Time spent processing request', ('method', 'endpoint'))
ROOT_REQUEST_TIME = REQUEST_TIME.labels('GET', '/')
# HOST_REQUEST_TIME = REQUEST_TIME.labels('GET', '/host')

# Create a metric to cound the number of runs on process_request()
c = Counter('requests_for_host', 'Number of runs of the process_request method', ['method', 'endpoint'])

@app.route('/')
@ROOT_REQUEST_TIME.time()
def hello_world():
    path = str(request.path)
    verb = request.method
    label_dict = {"method": verb,
                 "endpoint": path}
    c.labels(**label_dict).inc()
    return 'Flask Dockerized'

# Decorate function with metric.
def process_request():
    """A dummy function that takes some time."""
    weithed_sleep_times =   [0.004] * 1 + \
                            [0.009] * 3 + \
                            [0.0249] * 5 + \
                            [0.04] * 7 + \
                            [0.074] * 5 + \
                            [0.09] * 4 + \
                            [0.24] * 2 + \
                            [0.4] + [0.74] + [0.9] + [2.49]
    cosen_sleep_time = random.choice(weithed_sleep_times)
    sleep(cosen_sleep_time)
    
    return f"Did complicated things for {cosen_sleep_time} seconds."

@app.route('/work')
# @HOST_REQUEST_TIME.time()
def host():
    path = str(request.path)
    verb = request.method
    label_dict = {"method": verb,
                  "endpoint": path}
    c.labels(**label_dict).inc()
    with REQUEST_TIME.labels(verb, path).time():
        ret = str(process_request())
        return ret

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)



# # keep the server running
# def start_prometheus_server():
#     try:
#         httpd = HTTPServer(("0.0.0.0", PROMETHEUS_PORT), MetricsHandler)
#     except (OSError, socket.error):
#         return

#     thread = PrometheusEndpointServer(httpd)
#     thread.daemon = True
#     thread.start()
#     log.info("Exporting Prometheus /metrics/ on port %s", PROMETHEUS_PORT)

start_http_server(PROMETHEUS_PORT)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',threaded=True)
