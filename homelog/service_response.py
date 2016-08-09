from flask import Response, jsonify


class ServiceResponse(Response):

    def __init__(self, response, **kwargs):
        if 'direct_passthrough' not in kwargs:
            kwargs['direct_passthrough'] = True
        super(ServiceResponse, self).__init__(response, **kwargs)

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(ServiceResponse, cls).force_type(rv, environ)