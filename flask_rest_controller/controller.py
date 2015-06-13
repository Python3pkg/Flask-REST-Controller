# coding: utf-8

try:
    import simplejson as json
except:
    import json


import urllib
import jsonschema

from flask import redirect, url_for, render_template, session, request, abort, current_app
from flask.views import MethodView


__all__ = ['BaseRender', 'JsonRender', 'TemplateRender', 'BaseHandler', 'Controller']


class BaseRender(object):
    mimetype = None

    def set_mimetype(self, mimetype):
        self.mimetype = mimetype.lower()


class JsonRender(BaseRender):
    """
    for rendering a json response
    """
    schema = None

    def render_json(self, data):
        self.set_mimetype("application/json")
        if not self.is_json_response(data):
            data = [data]

        if self.should_schema_check:
            self.valid_schema(data)
        return json.dumps(data)

    @property
    def should_schema_check(self):
        """
        can verify using json schema of json response,
        """
        return True

    def valid_schema(self, response):
        if not isinstance(self.schema, dict):
            return response
        return jsonschema.validate(response, self.schema)

    def is_json_response(self, response):
        return isinstance(response, dict) or isinstance(response, list)


class TemplateRender(BaseRender):
    """
    for rendering a html template
    """
    def render_template(self, template_path, values={}):
        self.mimetype("text/html; charset=utf-8")
        return render_template(template_path, **values)


class BaseHandler(MethodView):
    """
    handling a dispatch for request
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def dispatch_request(self, *args, **kwargs):
        if not self.authenticate(*args, **kwargs):
            return self.authenticate_error()
        if not self.prepare(*args, **kwargs):
            return self.prepare_error()

        response = super(BaseHandler, self).dispatch_request(*args, **kwargs)
        self.after()

        return self.after_response(response)


class Controller(TemplateRender, JsonRender, BaseHandler):
    """
    base Class based Controller implemented,
    If you want to use this class, please use to perform extends

    When there was a request to the methods, the appropriate method is run method

    example:
        HTTP GET Request -> get
        HTTP POST Request -> post
    """
    storage = dict()
    headers = dict()

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.storage = dict()
        self.headers = dict()

    def add_header(self, key, value):
        self.headers[key] = value

    def get_headers(self):
        return self.headers

    def authenticate(self, *args, **kwargs):
        """
        run validat about your authentication
        """
        return True

    def authenticate_error(self):
        """
        run for authenticate error
        """
        return self.render_error()

    def prepare(self, *args, **kwargs):
        """
        prepare your validation and Update logic
        """
        return True

    def prepare_error(self):
        """
        run fot prepare error
        """
        return self.render_error()

    def after(self):
        pass

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def post(self, *args, **kwargs):
        raise NotImplementedError()

    def put(self, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, *args, **kwargs):
        raise NotImplementedError()

    def after_response(self, response):
        return current_app.response_class(response, headers=self.get_headers(), mimetype=self.mimetype.lower())

    def render_error(self):
        return self.error_404()

    def error_404(self):
        return abort(404)

    @property
    def request(self):
        return request

    @property
    def session(self):
        return session

    @property
    def into(self):
        return self.request.method.lower()

    def redirect(self, uri, params={}):
        try:
            return redirect(url_for(uri))
        except RuntimeError:
            pass

        query = [(k, v) for k, v in sorted(params.items())]
        params = urllib.urlencode(query)
        return redirect("{0}?{1}".format(uri, params))
