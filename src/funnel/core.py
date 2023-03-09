import inspect
import logging

from flask import Flask
from flask import request
from flask_restx import Api
from flask_restx import Resource
from werkzeug.exceptions import BadRequest

api = Api()


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    return app


logger = logging.getLogger(__name__)


def register(func, cls_name, *urls, **kwargs):
    def post(self):
        if request.headers["Content-Type"] != "application/json":
            raise BadRequest("Content-Type should be application/json")
        argspec = inspect.getfullargspec(func)
        req_json = request.get_json()
        fargs = []
        for i, arg in enumerate(argspec.args):
            if arg in req_json:
                value = req_json.pop(arg)
            else:
                try:
                    value = argspec.defaults[i - len(argspec.args)]
                except (IndexError, TypeError):
                    raise BadRequest(f"{arg} is missing")
            fargs.append(value)
        if argspec.varargs is not None and argspec.varargs in req_json:
            args = req_json.pop(argspec.varargs)
            if type(args) == list:
                fargs += args
            else:
                fargs.append(args)
        fkwargs = {}
        for kwarg in argspec.kwonlyargs:
            if kwarg in req_json:
                kwval = req_json.pop(kwarg)
            elif kwarg in argspec.kwonlydefaults:
                kwval = argspec.kwonlydefaults[kwarg]
            else:
                raise BadRequest(f"{kwarg} is missing")
            fkwargs[kwarg] = kwval
        if argspec.varkw is not None and argspec.varkw in req_json:
            kwargs = req_json.pop(argspec.varkw)
            if type(kwargs) is not dict:
                raise BadRequest(f"{argspec.varkw} is not dict")
            fkwargs.update(kwargs)
        for k, v in req_json.items():
            logger.warning(f"{k}: {v} is specified but not used")
        return func(*fargs, **fkwargs)

    cls = type(cls_name, (Resource,), {"post": post})
    doc = kwargs.pop("doc", None)
    if doc is not None:
        kwargs["route_doc"] = api._build_doc(cls, doc)
    api.add_resource(cls, *urls, **kwargs)


if __name__ == "__main__":
    create_app().run(debug=True)
