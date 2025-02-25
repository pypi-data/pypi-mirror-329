import click

from sqlalchemy import create_engine
from dbcache import schema


@click.group('dbcache')
def dbcache():
    pass


@dbcache.command('migrate-to-kvstores')
@click.argument('dburi')
@click.option('--namespace', default='cache')
def migrate_to_kvstores(dburi, namespace):
    engine = create_engine(dburi)
    ns = namespace
    with engine.begin() as cn:
        cn.execute(f"""
create table "{ns}".kvstore (
  id serial primary key,
  key text unique not null,
  value jsonb not null
);


create table "{ns}".vkvstore (
  id serial primary key,
  key text unique not null
);


create table "{ns}".version (
  id serial primary key,
  objid integer references "{ns}".vkvstore(id) on delete cascade,
  idate timestamptz not null default now(),
  value bytea not null,
  unique(objid, idate)
);

create index on "{ns}".version(idate);
""")


@dbcache.command('init-db')
@click.argument('dburi')
@click.option('--namespace', default='cache')
@click.option('--reset', is_flag=True, default=False)
def init_db(dburi, namespace, reset=False):
    engine = create_engine(dburi)
    schema.init(engine, ns=namespace, drop=reset)
