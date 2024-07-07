from flask import Flask, Response
from gevent.pywsgi import WSGIServer


class EndpointAction(object):
    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class WebhookApp(object):
    app = None

    def __init__(self, config):
        self.app = Flask("WebhookApp")
        self.config = config

    def run(self):
        http_server = WSGIServer((self.config.bind_address, self.config.port), self.app)
        http_server.serve_forever()

    def add_endpoint(
        self, endpoint=None, endpoint_name=None, handler=None, methods=["GET"]
    ):
        self.app.add_url_rule(
            endpoint, endpoint_name, EndpointAction(handler), methods=methods
        )
