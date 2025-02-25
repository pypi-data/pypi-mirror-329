# from flask import Flask, Response, request


# class EndpointAction(object):
#     def __init__(self, action):
#         self.action = action
#         self.response = Response(status=200, headers={})

#     def __call__(self, *args):
#         result = self.action()
#         headers = {}
#         if type(result) == list and len(result) == 2:
#             result, headers = result

#         if result != None:
#             response = Response(response=result, status=200, headers=headers)
#             return response
#         else:
#             return self.response


# class FlaskAppWrapper(object):
#     app = None

#     def __init__(self, name):
#         self.app = Flask(name)

#     def run(self, host="0.0.0.0", port="80"):
#         self.app.run(host=host, port=port)

#     def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
#         self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)
