from hashlib import sha1
import json
from datetime import (
    datetime,
    timedelta,
    timezone
)

from sqlhelp import select
from sqlalchemy import create_engine
import pytz

from dbcache.http import (
    kvstore_http_client,
    vkvstore_http_client
)


class dbcache:
    __slots__ = ('ns', 'engine')

    def __init__(self, uri, namespace='cache'):
        self.engine = create_engine(uri)
        self.ns = namespace

    def _remove_expired(self, cn):
        cn.execute(
            f'delete from "{self.ns}".things '
            f'where idate + validity < now()'
        )

    def _txlock(self, cn, key):
        lockid = hash(key + self.ns.encode('utf-8'))
        cn.execute(
            f'select pg_advisory_xact_lock({lockid})'
        )

    def get(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        with self.engine.begin() as cn:
            self._txlock(cn, key)
            self._remove_expired(cn)
            q = select(
                'value'
            ).table(
                f'"{self.ns}".things'
            ).where(
                key=sha1(key).hexdigest()
            )
            value = q.do(cn).scalar()
            if value:
                return value.tobytes()

    def _set(self, cn, hkey, value, lifetime):
        sql = (
            f'insert into "{self.ns}".things (key, value, validity) '
            'values (%(key)s, %(value)s, %(validity)s) '
            'on conflict (key) do update set '
            ' value = %(value)s, '
            ' validity = %(validity)s, '
            ' idate = %(idate)s'
        )
        cn.execute(
            sql,
            key=hkey,
            value=value,
            validity=lifetime,
            idate=datetime.utcnow().replace(tzinfo=pytz.utc)
        )

    def set(self, key, value, lifetime=timedelta(minutes=10)):
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(lifetime, int):
            lifetime = timedelta(seconds=lifetime)
        with self.engine.begin() as cn:
            self._txlock(cn, key)
            self._remove_expired(cn)
            hkey = sha1(key).hexdigest()
            self._set(cn, hkey, value, lifetime)

    def getorset(self, key, valuemaker, lifetime=timedelta(minutes=10)):
        assert callable(valuemaker)
        if isinstance(key, str):
            key = key.encode('utf-8')
        with self.engine.begin() as cn:
            self._txlock(cn, key)
            self._remove_expired(cn)
            hkey = sha1(key).hexdigest()
            q = select(
                'value'
            ).table(
                f'"{self.ns}".things'
            ).where(
                key=hkey
            )
            value = q.do(cn).scalar()
            # we got something
            if value is not None:
                return value.tobytes()
            # we need to set a value
            value = valuemaker()
            self._set(cn, hkey, value, lifetime)
            return value

    def delete(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        with self.engine.begin() as cn:
            hkey = sha1(key).hexdigest()
            cn.execute(
                f'delete from "{self.ns}".things '
                f'where key = %(key)s',
                key=hkey
            )


def kvstore(uri, namespace='cache', auth=None):
    if uri.startswith('postgres'):
        return _kvstore(uri, namespace)
    assert uri.startswith('http')
    return kvstore_http_client(uri, namespace, auth)


class _kvstore:
    __slots__ = ('ns', 'engine')

    def __init__(self, uri, namespace='cache'):
        self.engine = create_engine(uri)
        self.ns = namespace

    def all(self):
        with self.engine.begin() as cn:
            q = select(
                'key', 'value'
            ).table(
                f'"{self.ns}".kvstore'
            )
            return {
                key: value
                for key, value in q.do(cn).fetchall()
            }

    def keys(self):
        with self.engine.begin() as cn:
            q = select('key').table(f'"{self.ns}".kvstore').order('key')
            return [
                key for key, in q.do(cn).fetchall()
            ]

    def get(self, key):
        with self.engine.begin() as cn:
            q = select(
                'value'
            ).table(
                f'"{self.ns}".kvstore'
            ).where(
                key=key
            )
            value = q.do(cn).scalar()
            return value

    def set(self, key, value):
        with self.engine.begin() as cn:
            sql = (
                f'insert into "{self.ns}".kvstore (key, value) '
                'values (%(key)s, %(value)s) '
                'on conflict (key) do update set '
                ' value = %(value)s'
            )
            cn.execute(
                sql,
                key=key,
                value=json.dumps(value)
            )

    def delete(self, key):
        with self.engine.begin() as cn:
            cn.execute(
                f'delete from "{self.ns}".kvstore '
                f'where key = %(key)s',
                key=key
            )


def vkvstore(uri, namespace='cache', auth=None):
    if uri.startswith('postgres'):
        return _vkvstore(uri, namespace)
    assert uri.startswith('http')
    return vkvstore_http_client(uri, namespace, auth)


class _vkvstore:
    __slots__ = ('ns', 'engine')

    def __init__(self, uri, namespace='cache'):
        self.engine = create_engine(uri)
        self.ns = namespace

    def keys(self) -> dict[str, object]:
        with self.engine.begin() as cn:
            q = select('key').table(f'"{self.ns}".vkvstore').order('key')
            return [
                key for key, in q.do(cn).fetchall()
            ]

    def get(self, key: str, insertion_date: datetime=None):
        with self.engine.begin() as cn:
            sql = (
                f'select version.value '
                f'from "{self.ns}".vkvstore as store,'
                f'     "{self.ns}".version as version '
                f'where store.id = version.objid and'
                f'      store.key = %(key)s '
            )
            if insertion_date:
                sql += ' and version.idate <= %(idate)s'
            sql += ' order by version.id desc limit 1'
            value = cn.execute(
                sql,
                key=key,
                idate=insertion_date
            ).scalar()
            if value is not None:
                return value.tobytes()

    def versions(self, key: str):
        with self.engine.begin() as cn:
            sql = (
                f'select version.idate '
                f'from "{self.ns}".vkvstore as store,'
                f'     "{self.ns}".version as version '
                f'where store.id = version.objid and'
                f'      store.key = %(key)s '
                f' order by version.id'
            )
            return [
                row.idate
                for row in cn.execute(
                    sql,
                    key=key
                ).fetchall()
            ]

    def set(self, key: str, value: bytes,
            insertion_date: datetime=None):
        assert isinstance(value, bytes)
        with self.engine.begin() as cn:
            # creation ?
            objid = cn.execute(
                f'select id from "{self.ns}".vkvstore '
                'where key = %(key)s',
                key=key
            ).scalar()
            if objid is None:
                objid = cn.execute(
                    f'insert into "{self.ns}".vkvstore (key) '
                    'values (%(key)s) returning id',
                    key=key
                ).scalar()

            # new version
            if insertion_date is None:
                insertion_date = datetime.utcnow().replace(
                    tzinfo=timezone.utc
                )
            # check monotonicity
            oops = cn.execute(
                f'select version.id from "{self.ns}".version '
                f'where objid = %(objid)s and '
                f'      idate > %(idate)s '
                f'limit 1',
                objid=objid,
                idate=insertion_date
            ).scalar()
            assert oops is None, 'insertion dates must be monotonic increasing'

            # gree lights
            cn.execute(
                f'insert into "{self.ns}".version (objid, idate, value) '
                f'values (%(objid)s, %(idate)s, %(value)s)',
                objid=objid,
                idate=insertion_date,
                value=value
            )
            return

    def delete(self, key):
        with self.engine.begin() as cn:
            cn.execute(
                f'delete from "{self.ns}".vkvstore '
                f'where key = %(key)s',
                key=key
            )
