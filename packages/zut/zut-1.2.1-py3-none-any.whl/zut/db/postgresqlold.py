from __future__ import annotations

from contextlib import contextmanager, nullcontext
from io import IOBase
import logging
import re
from typing import TYPE_CHECKING
from urllib.parse import unquote, urlparse

from zut import build_url, get_logger
from zut.db.postgresql import PostgreSql, postgresql_parse_notice

if TYPE_CHECKING:
    from psycopg2.extensions import connection, cursor

try:
    from psycopg2 import connect
    _missing_dependency = None
except ImportError:
    _missing_dependency = "psycopg2"


class PostgreSqlOld(PostgreSql[connection, cursor] if TYPE_CHECKING else PostgreSql):
    """
    Database adapter for PostgreSQL (using `psycopg2` driver).
    """
    missing_dependency = _missing_dependency

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_transaction = None

    def create_connection(self, *, autocommit: bool, **kwargs):
        r = urlparse(self._connection_url)

        if r.hostname and not 'host' in kwargs:
            kwargs['host'] = unquote(r.hostname)
        if r.port and not 'port' in kwargs:
            kwargs['port'] = r.port

        path = r.path.lstrip('/')
        if path and not 'dbname' in kwargs:
            kwargs['dbname'] = unquote(path)

        if r.username and not 'user' in kwargs:
            kwargs['user'] = unquote(r.username)
        if r.password and not 'password' in kwargs:
            kwargs['password'] = unquote(r.password)

        conn = connect(**kwargs)
        conn.autocommit = autocommit
        return conn

    def transaction(self):
        if self._in_transaction:
            return nullcontext()
        
        class CM:
            def __init__(self, db: PostgreSqlOld):
                self.db = db

            def __enter__(self):
                self.db._in_transaction = self.db.connection.__enter__()
                return self
            
            def __exit__(self, *args):
                self.db._in_transaction.__exit__(*args)
                self.db._in_transaction = None
                
        return CM(self)

    def _get_url_from_connection(self):    
        params = self.connection.get_dsn_parameters()
        return build_url(
            scheme=self.scheme,
            path='/' + params.get('dbname', None),
            hostname=params.get('host', None),
            port=params.get('port', None),
            username=params.get('user', None),
            password=params.get('password', None),
        )
            
    def _register_notice_handler(self, cursor, query_id = None):
        if query_id is not None:
            logger = get_logger(self._logger.name + f':{query_id}')
        else:
            logger = self._logger

        return PostgreSqlOldNoticeHandler(cursor.connection, logger)

    def _actual_copy_from_csv(self, cursor: cursor, sql: str, fp: IOBase, buffer_size: int):
        cursor.copy_expert(sql, fp, buffer_size)


class PostgreSqlOldNoticeHandler:
    """
    This class is the actual handler required by psycopg 2 `connection.notices`.
    
    It can also be used as a context manager that remove the handler on exit.
    """
    _notice_re = re.compile(r"^(?P<severity>[A-Z]+)\:\s(?P<message>.*)$", re.DOTALL)

    def __init__(self, connection, logger: logging):
        self.connection = connection
        self.logger = logger
        self.connection.notices = self

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        self.connection.notices = []

    def append(self, fullmsg: str):
        fullmsg = fullmsg.strip()
        m = self._notice_re.match(fullmsg)
        if not m:
            self.logger.error(fullmsg)
            return

        severity = m.group("severity")
        message = m.group("message").lstrip()
        level, message = postgresql_parse_notice(severity, message)

        self.logger.log(level, message)
