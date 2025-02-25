from functools import wraps
import json
import logging
import traceback as tb

from dateutil.parser import parse
import werkzeug
from werkzeug.exceptions import HTTPException
from flask import (
    Blueprint,
    make_response
)
from flask_restx import (
    Api as baseapi,
    Resource,
    reqparse
)
import requests


def utcdt(dtstr):
    return parse(dtstr)


namespace = reqparse.RequestParser()
namespace.add_argument(
    'namespace',
    type=str,
    required=True,
    help='namespace'
)

getvalue = namespace.copy()
getvalue.add_argument(
    'key',
    type=str,
    required=True,
    help='key'
)

setvalue = getvalue.copy()
setvalue.add_argument(
    'value',
    type=str,
    required=True,
    help='value'
)

vgetvalue = getvalue.copy()
vgetvalue.add_argument(
    'insertion_date',
    type=utcdt,
    help='insertion_date'
)

vsetvalue = getvalue.copy()
vsetvalue.add_argument(
    'value',
    type=werkzeug.datastructures.FileStorage,
    required=True,
    location='files',
    help='value'
)
vsetvalue.add_argument(
    'insertion_date',
    type=utcdt,
    help='insertion_date'
)


L = logging.getLogger('dbcache-server')


def onerror(func):
    @wraps(func)
    def wrapper(*a, **k):
        try:
            return func(*a, **k)
        except Exception as err:
            if isinstance(err, HTTPException):
                raise
            L.exception('oops')
            tb.print_exc()
            response = make_response(str(err))
            response.headers['Content-Type'] = 'text/plain'
            response.status_code = 418
            return response

    return wrapper


class kvstore_httpapi:
    bp = None
    api = None

    def __init__(self, uri, kvstore_apimap, vkvstore_apimap):
        if self.bp is None:
            # odd pattern to allow being mixed with
            # another class that provides:
            # .bp and .api
            self.bp = Blueprint(
                'kvstore-server',
                __name__
            )

            # api & ns
            class Api(baseapi):
                # see https://github.com/flask-restful/flask-restful/issues/67
                def _help_on_404(self, message=None):
                    return message or 'No such thing.'

            self.api = Api(
                self.bp,
                version='1.0',
                title='kvstore api'
            )
            self.api.namespaces.pop(0)  # wipe the default namespace

        nsk = self.nsk = self.api.namespace(
            'kvstore',
            description='Key-Value store'
        )
        nsv = self.nsv = self.api.namespace(
            'vkvstore',
            description='Versioned Key-Value store'
        )
        api = self.api

        @nsk.route('/all')
        class allkeyvalues(Resource):

            @api.expect(namespace)
            @onerror
            def get(self):
                args = namespace.parse_args()
                ns = args.namespace
                if ns not in kvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = kvstore_apimap[ns]
                return store.all(), 200

        @nsk.route('/keys')
        class allkeys(Resource):

            @api.expect(namespace)
            @onerror
            def get(self):
                args = namespace.parse_args()
                ns = args.namespace
                if ns not in kvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = kvstore_apimap[ns]
                return store.keys(), 200

        @nsk.route('/item')
        class item(Resource):

            @api.expect(getvalue)
            @onerror
            def get(self):
                args = getvalue.parse_args()
                ns = args.namespace
                if ns not in kvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = kvstore_apimap[ns]
                val = store.get(args.key)
                return val, 200

            @api.expect(setvalue)
            @onerror
            def put(self):
                args = setvalue.parse_args()
                ns = args.namespace
                if ns not in kvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = kvstore_apimap[ns]
                val = json.loads(args.value)

                store.set(args.key, val)
                return '', 204

            @api.expect(getvalue)
            @onerror
            def delete(self):
                args = getvalue.parse_args()
                ns = args.namespace
                if ns not in kvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = kvstore_apimap[ns]
                store.delete(args.key)
                return '', 204

        @nsv.route('/versions')
        class versions(Resource):

            @api.expect(getvalue)
            @onerror
            def get(self):
                args = getvalue.parse_args()
                ns = args.namespace
                if ns not in vkvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = vkvstore_apimap[ns]
                return [
                    v.isoformat()
                    for v in store.versions(args.key)
                ], 200

        @nsv.route('/keys')
        class allvkeys(Resource):

            @api.expect(namespace)
            @onerror
            def get(self):
                args = namespace.parse_args()
                ns = args.namespace
                if ns not in vkvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = vkvstore_apimap[ns]
                return store.keys(), 200

        @nsv.route('/item')
        class vitem(Resource):

            @api.expect(vgetvalue)
            @onerror
            def get(self):
                args = vgetvalue.parse_args()
                ns = args.namespace
                if ns not in vkvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = vkvstore_apimap[ns]
                val = store.get(args.key, args.insertion_date)
                if val is None:
                    response = make_response('null')
                else:
                    response = make_response(
                        val
                    )
                response.headers['Content-Type'] = 'application/octet-stream'
                response.status_code = 200
                return response

            @api.expect(vsetvalue)
            @onerror
            def put(self):
                args = vsetvalue.parse_args()
                ns = args.namespace
                if ns not in vkvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = vkvstore_apimap[ns]
                val = args.value.stream.read()

                store.set(args.key, val, args.insertion_date)
                return '', 204

            @api.expect(getvalue)
            @onerror
            def delete(self):
                args = getvalue.parse_args()
                ns = args.namespace
                if ns not in vkvstore_apimap:
                    api.abort(404, f'`{ns}` namespace is not supported')

                store = vkvstore_apimap[ns]
                store.delete(args.key)
                return '', 204


def unwraperror(func):

    def wrapper(*a, **k):
        res = func(*a, **k)
        if isinstance(res, requests.models.Response):
            if res.status_code == 418:
                raise Exception(res.text)
            if res.status_code == 404:
                raise Exception('404 - please check your base uri')
            if res.status_code == 400:
                raise Exception(f'Bad Query: {res.text}')
            if res.status_code in (401, 403):
                raise Exception('401 - Unauthorized.')
            if res.status_code == 413:
                raise Exception('413 - Payload to big for the web server.')
            if res.status_code >= 500:
                raise Exception('The server could not process your query.')
        return res

    return wrapper


class kvstore_http_client:

    def __init__(self, uri, namespace='cache', auth=None):
        self.uri = uri
        self.session = requests.Session()
        self.ns = namespace
        if auth and 'login' in auth:
            self.session.auth = auth['login'], auth['password']

    @unwraperror
    def all(self):
        resp = self.session.get(f'{self.uri}/kvstore/all', params={
            'namespace': self.ns
        })
        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 404:
            return {}

        return resp

    @unwraperror
    def keys(self):
        resp = self.session.get(f'{self.uri}/kvstore/keys', params={
            'namespace': self.ns
        })
        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 404:
            return []

        return resp

    @unwraperror
    def get(self, key):
        resp = self.session.get(f'{self.uri}/kvstore/item', params={
            'namespace': self.ns,
            'key': key
        })
        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 404:
            return None

        return resp

    @unwraperror
    def set(self, key, value):
        resp = self.session.put(f'{self.uri}/kvstore/item', data={
            'namespace': self.ns,
            'key': key,
            'value': json.dumps(value)
        })
        if resp.status_code in (204, 404):
            return

        return resp

    @unwraperror
    def delete(self, key):
        resp = self.session.delete(f'{self.uri}/kvstore/item', data={
            'namespace': self.ns,
            'key': key
        })
        if resp.status_code in (204, 404):
            return

        return resp


class vkvstore_http_client:

    def __init__(self, uri, namespace='cache', auth=None):
        self.uri = uri
        self.session = requests.Session()
        self.ns = namespace
        if auth and 'login' in auth:
            self.session.auth = auth['login'], auth['password']

    @unwraperror
    def versions(self, key):
        resp = self.session.get(f'{self.uri}/vkvstore/versions', params={
            'namespace': self.ns,
            'key': key
        })
        if resp.status_code == 200:
            return [
                utcdt(v)
                for v in resp.json()
            ]

        if resp.status_code == 404:
            return {}

        return resp

    @unwraperror
    def keys(self):
        resp = self.session.get(f'{self.uri}/vkvstore/keys', params={
            'namespace': self.ns
        })
        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 404:
            return []

        return resp

    @unwraperror
    def get(self, key, insertion_date=None):
        resp = self.session.get(f'{self.uri}/vkvstore/item', params={
            'namespace': self.ns,
            'key': key,
            'insertion_date': insertion_date.isoformat() if insertion_date else None
        })
        if resp.status_code == 200:
            if resp.content.startswith(b'null'):
                return None
            return resp.content

        if resp.status_code == 404:
            return None

        return resp

    @unwraperror
    def set(self, key, value, insertion_date=None):
        resp = self.session.put(
            f'{self.uri}/vkvstore/item',
            data={
                'namespace': self.ns,
                'key': key,
                'insertion_date': insertion_date.isoformat() if insertion_date else None
            },
            files={
                'value': value
            }
        )
        if resp.status_code in (204, 404):
            return

        return resp

    @unwraperror
    def delete(self, key):
        resp = self.session.delete(f'{self.uri}/vkvstore/item', data={
            'namespace': self.ns,
            'key': key
        })
        if resp.status_code in (204, 404):
            return

        return resp
