from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Generator
from urllib.parse import unquote, urlparse

from zut import Header
from zut.db import Db

if TYPE_CHECKING:
    from MySQLdb import Connection
    from MySQLdb.cursors import Cursor

try:
    from MySQLdb import connect
    _missing_dependency = None
except ImportError:
    _missing_dependency = "mysqlclient"


class MariaDb(Db[Connection, Cursor] if TYPE_CHECKING else Db):
    """
    Database adapter for MariaDB and Mysql.
    """
    scheme = 'mariadb'
    default_port = 3306
    default_schema = None
    identifier_quotechar_begin = '`'
    identifier_quotechar_end = '`'
    identity_definition_sql = 'AUTO_INCREMENT'
    float_sql_type = 'double'
    datetime_sql_type = 'datetime'
    datetime_sql_precision = 6
    accept_aware_datetime = False        
    can_cascade_truncate = False
    temporary_prefix = 'temp.'
    missing_dependency = _missing_dependency
    
    def create_connection(self, *, autocommit: bool, **kwargs):        
        r = urlparse(self._connection_url)
        
        if r.hostname and not 'host' in kwargs:
            kwargs['host'] = unquote(r.hostname)
        if r.port and not 'port' in kwargs:
            kwargs['port'] = r.port
        
        path = r.path.lstrip('/')
        if path and not 'database' in kwargs:
            kwargs['database'] = unquote(path)

        if r.username and not 'user' in kwargs:
            kwargs['user'] = unquote(r.username)
        if r.password and not 'password' in kwargs:
            kwargs['password'] = unquote(r.password)
        
        return connect(**kwargs, sql_mode='STRICT_ALL_TABLES', autocommit=autocommit)

    @property
    def autocommit(self):
        if not self._connection:
            return self._autocommit
        else:
            return self._connection.get_autocommit()


    @contextmanager
    def transaction(self):
        with self.connection.cursor() as cursor:
            cursor.execute("START TRANSACTION")
        try:
            yield None
            with self.connection.cursor() as cursor:
                cursor.execute("COMMIT")
        except:
            with self.connection.cursor() as cursor:
                cursor.execute("ROLLBACK")
            raise


    def table_exists(self, table: str|tuple = None, *, cursor = None) -> bool:        
        _, table = self.split_name(table)

        query = "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)"
        params = [table]

        return self.get_scalar(query, params, cursor=cursor) == 1


    def _get_table_columns(self, table, *, cursor, typeonly: bool) -> Generator[dict,Any,Any]|list[Header|dict]|tuple[list[dict],list[dict]]:
        schema, table = self.split_name(table)

        sql = "SHOW COLUMNS FROM "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += self.escape_identifier(table)

        columns: list[Header] = []
        any_multi = False
        for data in self.get_dicts(sql, cursor=cursor):
            if not typeonly:
                name = data['Field']
                if data['Key'] == 'UNI':
                    unique = True
                elif data['Key'] == 'MUL':
                    any_multi = True
                    unique = [(name, '?')]
                else:
                    unique = False
                    ()               
                columns.append(Header(name, sql_type=data['Type'].lower(), null=data['Null'] == 'YES', primary_key=data['Key'] == 'PRI', unique=unique, identity='auto' in data['Extra']))
            else: # typeonly
                columns.append(Header(data['Field'], sql_type=data['Type'].lower(), null=data['Null'] == 'YES'))

        if not any_multi:
            return columns

        # Find multi-column unique keys
        sql = "SHOW INDEX FROM "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += self.escape_identifier(table)
        sql += " WHERE Non_unique = 0"

        columns_by_name: dict[str,Header] = {}
        for column in columns:
            columns_by_name[column.name] = column
            #Reset unique
            column.unique = False

        columns_by_index: dict[str,list[str]] = {}
        for data in self.get_dicts(sql, cursor=cursor):
            if data['Key_name'] in columns_by_index:
                names = columns_by_index[data['Key_name']]
            else:
                names = []
                columns_by_index[data['Key_name']] = names                
            names.append(data['Column_name'])

        for names in columns_by_index.values():
            for name in names:
                column = columns_by_name[name]
                if len(names) == 1:
                    column.unique = True
                elif not column.unique:
                    column.unique = [names]
                else:
                    column.unique.append(tuple(names))

        return columns
