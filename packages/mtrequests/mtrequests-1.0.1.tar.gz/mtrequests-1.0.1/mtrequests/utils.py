from . import Session


def get(url, params=None, **kwargs):
    return Session.make_request("GET", url, params, **kwargs)


def options(url, params=None, **kwargs):
    return Session.make_request("OPTIONS", url, params, **kwargs)


def head(url, params=None, **kwargs):
    return Session.make_request("HEAD", url, params, **kwargs)


def post(url, params=None, **kwargs):
    return Session.make_request("POST", url, params, **kwargs)


def put(url, params=None, **kwargs):
    return Session.make_request("PUT", url, params, **kwargs)


def patch(url, params=None, **kwargs):
    return Session.make_request("PATCH", url, params, **kwargs)


def delete(url, params=None, **kwargs):
    return Session.make_request("DELETE", url, params, **kwargs)
