create schema if not exists "{ns}";

create table if not exists "{ns}".things (
  id serial primary key,
  idate timestamptz not null default now(),
  validity interval not null default '10 minutes',
  key text unique not null,
  value bytea not null
);


create table if not exists "{ns}".kvstore (
  id serial primary key,
  key text unique not null,
  value jsonb not null
);


create table if not exists "{ns}".vkvstore (
  id serial primary key,
  key text unique not null
);


create table if not exists "{ns}".version (
  id serial primary key,
  objid integer references "{ns}".vkvstore(id) on delete cascade,
  idate timestamptz not null default now(),
  value bytea not null,
  unique(objid, idate)
);

create index on "{ns}".version(idate);
