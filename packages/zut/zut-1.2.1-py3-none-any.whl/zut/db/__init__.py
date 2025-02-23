"""
Common operations on databases.
"""
from __future__ import annotations

import logging
import re
import socket
from contextlib import nullcontext
from datetime import date, datetime, time, tzinfo
from decimal import Decimal
from enum import Enum, Flag
from io import IOBase, StringIO
from pathlib import Path
from secrets import token_hex
from threading import current_thread
from time import time_ns
from typing import Any, Generator, Generic, Iterable, Sequence, Tuple, TypeVar
from urllib.parse import ParseResult, parse_qs, quote, unquote, urlparse

from zut import (ColumnsProvider, CsvDumper, Header, Literal, NotFoundError,
                 Row, SeveralFoundError, TabDumper, TabularDumper, build_url,
                 convert, examine_csv_file, files, get_default_csv_delimiter,
                 get_default_decimal_separator, get_logger, get_tzkey,
                 hide_url_password, is_aware, make_aware, make_naive,
                 now_naive_utc, parse_tz, slugify, tabular_dumper)

T_Connection = TypeVar('T_Connection')
T_Cursor = TypeVar('T_Cursor')


class Db(Generic[T_Connection, T_Cursor]):
    """
    Base class for database adapters.
    """

    # DB engine specifics
    scheme: str
    default_port: int
    default_schema: str|None = 'public'
    only_positional_params = False
    split_multi_statement_files = False
    table_in_path = True
    identifier_quotechar_begin = '"'
    identifier_quotechar_end = '"'
    sql_placeholder = '%s'
    sql_named_placeholder = '%%(%s)s'
    bool_sql_type = 'boolean'
    int_sql_type = 'bigint'
    float_sql_type = 'double precision'
    decimal_sql_type = 'decimal'
    datetime_sql_type = 'timestamptz'
    datetime_sql_precision: int|None = None # when necessary for default columns with milliseconds
    date_sql_type = 'date'
    str_sql_type = 'text'
    str_precised_sql_type = 'varchar'
    accept_aware_datetime = True
    truncate_with_delete = False
    can_cascade_truncate = True
    identity_definition_sql = 'GENERATED ALWAYS AS IDENTITY'
    procedure_caller = 'CALL'
    procedure_params_parenthesis = True
    function_requires_schema = False
    can_add_several_columns = False
    temporary_prefix = 'pg_temp.'
    missing_dependency: str = None
    
    # Global configurable
    default_autocommit = True
    use_http404 = False
    """ Use Django's HTTP 404 exception instead of NotFoundError (if Django is available). """

    def __init__(self, origin: T_Connection|str|dict|ParseResult, *, password_required: bool = False, autocommit: bool = None, tz: tzinfo|str|None = None, table: str|None = None, schema: str|None = None):
        """
        Create a new Db instance.
        - `origin`: an existing connection object (or Django wrapper), or the URL for the new connection to be created by the Db instance.
        - `autocommit`: commit transactions automatically (applies only for connections created by the Db instance).
        - `tz`: naive datetimes in results are made aware in the given timezone.
        """
        if self.missing_dependency:
            raise ValueError(f"Cannot use {type(self).__name__} (missing {self.missing_dependency} dependency)")
        
        self._logger = get_logger(f"{__name__}.{self.__class__.__qualname__}")
        
        self.table: str = table
        """ A specific table associated to this instance. Used for example as default table for `dumper`. """

        self.schema: str = schema
        """ A specific schema associated to this instance. Used for example as default table for `dumper`. """
        
        if isinstance(origin, (str,ParseResult)): # URL
            self._close_connection = True
            self._connection: T_Connection = None
            self._connection_wrapper = None
            r = origin if isinstance(origin, ParseResult) else urlparse(origin)

            if r.fragment:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected fragment: {r.fragment}")
            if r.params:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected params: {r.params}")
            
            query = parse_qs(r.query)
            query_schema = query.pop('schema', [None])[-1]
            if query_schema and self.schema is None:
                self.schema = query_schema
            query_table = query.pop('table', [None])[-1]                
            if query_table and self.table is None:
                self.table = query_table
            if query:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected query data: {query}")
            
            scheme = r.scheme
            r = self._verify_scheme(r)
            if not r:
                raise ValueError(f"Invalid {self.__class__.__name__}: invalid scheme: {scheme}")

            if not self.table and self.table_in_path:
                table_match = re.match(r'^/?(?P<name>[^/@\:]+)/((?P<schema>[^/@\:\.]+)\.)?(?P<table>[^/@\:\.]+)$', r.path)
            else:
                table_match = None

            if table_match:
                if self.table is None:
                    self.table = table_match['table']
                if self.schema is None:
                    self.schema = table_match['schema'] if table_match['schema'] else None
            
                r = r._replace(path=table_match['name'])
                self._connection_url = r.geturl()
            
            else:
                self._connection_url = r.geturl()
        
        elif isinstance(origin, dict): # connect dictionnary
            self._close_connection = True
            self._connection: T_Connection = None
            self._connection_wrapper = None

            if 'NAME' in origin:
                # uppercase (as used by django)
                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = origin.get('HOST', None),
                    port = origin.get('PORT', None),
                    username = origin.get('USER', None),
                    password = origin.get('PASSWORD', None),
                    path = origin.get('NAME', None),
                )
                if not self.table:
                    self.table = origin.get('TABLE', None)
                if not self.schema:
                    self.schema = origin.get('SCHEMA', None)

            else:
                # lowercase (as used by some drivers' connection kwargs)
                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = origin.get('host', None),
                    port = origin.get('port', None),
                    username = origin.get('user', None),
                    password = origin.get('password', None),
                    path = origin.get('name', origin.get('dbname', None)),
                )
                if not self.table:
                    self.table = origin.get('table', None)
                if not self.schema:
                    self.schema = origin.get('schema', None)

        else:
            connection = _get_connection_from_wrapper(origin)
            if connection is not None:
                self._connection_wrapper = None
                self._connection = connection
            else:
                self._connection_wrapper = origin
                self._connection = None
            self._connection_url: str = None
            self._close_connection = False
        
        self.password_required = password_required
        if isinstance(tz, str):
            tz = tz if tz == 'localtime' else parse_tz(tz)
        self.tz = tz
        
        self._autocommit = autocommit if autocommit is not None else self.__class__.default_autocommit
        self._last_autoclose_cursor = None
        self._is_port_opened = None
    

    @classmethod
    def get_sqlutils_path(cls):
        path = Path(__file__).resolve().parent.joinpath('sqlutils', f"{cls.scheme}.sql")
        if not path.exists():
            return None
        return path
    
    
    def _verify_scheme(self, r: ParseResult) -> ParseResult|None:
        if r.scheme == self.scheme:
            return r
        else:
            return None


    def get_url(self, *, hide_password = False):
        if self._connection_url:
            url = self._connection_url
        else:
            url = self._get_url_from_connection()

        if hide_password:
            url = hide_url_password(url)

        if self.table:
            if self.table_in_path:
                url += f"/"
                if self.schema:
                    url += quote(self.schema)
                    url += '.'
                url += quote(self.table)
            else:
                url += f"?table={quote(self.table)}"
                if self.schema:
                    url += f"&schema={quote(self.schema)}"

        return url


    def _get_url_from_connection(self):
        raise NotImplementedError()
    

    def get_db_name(self):
        url = self.get_url()
        r = urlparse(url)
        return unquote(r.path).lstrip('/')


    @property
    def is_port_opened(self):
        if self._is_port_opened is None:
            r = urlparse(self.get_url())
            host = r.hostname or '127.0.0.1'
            port = r.port if r.port is not None else self.default_port
        
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug("Check host %s, port %s (from thread %s)", host, port, current_thread().name)

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((host, port))
                if result == 0:
                    self._logger.debug("Host %s, port %s: connected", host, port)
                    self._is_port_opened = True
                else:
                    self._logger.debug("Host %s, port %s: NOT connected", host, port)
                    self._is_port_opened = False
                sock.close()
            except Exception as err:
                raise ValueError(f"Cannot check host {host}, port {port}: {err}")
        
        return self._is_port_opened
    

    #region Connection

    def __enter__(self):
        return self


    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        self.close()


    def close(self):
        if self._last_autoclose_cursor:
            # NOTE: for SqlServer/PyODBC, this should be enough to avoid committing when autocommit is False because we don't call __exit__()
            # See: https://github.com/mkleehammer/pyodbc/wiki/Cursor#context-manager
            self._last_autoclose_cursor.close()
            self._last_autoclose_cursor = None

        if self._connection and self._close_connection:
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Close %s (%s) connection to %s", type(self).__name__, type(self._connection).__module__ + '.' + type(self._connection).__qualname__, hide_url_password(self._connection_url))
            self._connection.close()
            self._connection = None


    @property
    def connection(self) -> T_Connection:
        if not self._connection:
            if self._connection_wrapper:
                self._connection = self._connection_wrapper.cursor().connection
            else:
                if self.password_required:
                    password = urlparse(self._connection_url).password
                    if not password:
                        raise ValueError("Cannot create %s connection to %s: password not provided" % (type(self).__name__, hide_url_password(self._connection_url)))
                if self._logger.isEnabledFor(logging.DEBUG):
                    self._logger.debug(f"Create %s connection to %s", type(self).__name__, hide_url_password(self._connection_url))
                self._connection = self.create_connection(autocommit=self._autocommit)
        return self._connection
    

    @property
    def autocommit(self):
        if not self._connection:
            return self._autocommit
        else:
            return self._connection.autocommit


    def create_connection(self, *, autocommit: bool, **kwargs) -> T_Connection:
        raise NotImplementedError()


    def cursor(self, *, autoclose=True, **kwargs) -> T_Cursor:
        """
        A new cursor object that support the context manager protocol
        """
        if autoclose:
            if self._last_autoclose_cursor:
                self._last_autoclose_cursor.close()
                self._last_autoclose_cursor = None
            self._last_autoclose_cursor = self.connection.cursor(**kwargs)
            return self._last_autoclose_cursor
        else:
            return self.connection.cursor(**kwargs)
        
    def transaction(self):
        """
        A context manager for a transaction.
        """
        raise NotImplementedError()

    #endregion
    

    #region Queries

    def to_positional_params(self, query: str, params: dict) -> tuple[str, Sequence[Any]]:
        from sqlparams import \
            SQLParams  # not at the top because the enduser might not need this feature

        if not hasattr(self.__class__, '_params_formatter'):
            self.__class__._params_formatter = SQLParams('named', 'qmark')
        query, params = self.__class__._params_formatter.format(query, params)

        return query, params
    

    def get_paginated_select_queries(self, query: str, *, limit: int|None, offset: int|None) -> tuple[str,str]:        
        if limit is not None:
            if isinstance(limit, str) and re.match(r"^[0-9]+$", limit):
                limit = int(limit)
            elif not isinstance(limit, int):
                raise TypeError(f"Invalid type for limit: {type(limit).__name__} (expected int)")
            
        if offset is not None:
            if isinstance(offset, str) and re.match(r"^[0-9]+$", offset):
                offset = int(offset)
            elif not isinstance(offset, int):
                raise TypeError(f"Invalid type for offset: {type(limit).__name__} (expected int)")
        
        beforepart, selectpart, orderpart = self._parse_select_query(query)

        paginated_query = beforepart
        total_query = beforepart
        
        paginated_query += self._paginate_parsed_query(selectpart, orderpart, limit=limit, offset=offset)
        total_query += f"SELECT COUNT(*) FROM ({selectpart}) s"

        return paginated_query, total_query
    

    def _parse_select_query(self, query: str):
        import sqlparse  # not at the top because the enduser might not need this feature

        # Parse SQL to remove token before the SELECT keyword
        # example: WITH (CTE) tokens
        statements = sqlparse.parse(query)
        if len(statements) != 1:
            raise sqlparse.exceptions.SQLParseError(f"Query contains {len(statements)} statements")

        # Get first DML keyword
        dml_keyword = None
        dml_keyword_index = None
        order_by_index = None
        for i, token in enumerate(statements[0].tokens):
            if token.ttype == sqlparse.tokens.DML:
                if dml_keyword is None:
                    dml_keyword = str(token).upper()
                    dml_keyword_index = i
            elif token.ttype == sqlparse.tokens.Keyword:
                if order_by_index is None:
                    keyword = str(token).upper()
                    if keyword == "ORDER BY":
                        order_by_index = i

        # Check if the DML keyword is SELECT
        if not dml_keyword:
            raise sqlparse.exceptions.SQLParseError(f"Not a SELECT query (no DML keyword found)")
        if dml_keyword != 'SELECT':
            raise sqlparse.exceptions.SQLParseError(f"Not a SELECT query (first DML keyword is {dml_keyword})")

        # Get part before SELECT (example: WITH)
        if dml_keyword_index > 0:
            tokens = statements[0].tokens[:dml_keyword_index]
            beforepart = ''.join(str(token) for token in tokens)
        else:
            beforepart = ''
    
        # Determine actual SELECT query
        if order_by_index is not None:
            tokens = statements[0].tokens[dml_keyword_index:order_by_index]
            selectpart = ''.join(str(token) for token in tokens)
            tokens = statements[0].tokens[order_by_index:]
            orderpart = ''.join(str(token) for token in tokens)
        else:
            tokens = statements[0].tokens[dml_keyword_index:]
            selectpart = ''.join(str(token) for token in tokens)
            orderpart = ''

        return beforepart, selectpart, orderpart
    

    def _paginate_parsed_query(self, selectpart: str, orderpart: str, *, limit: int|None, offset: int|None) -> str:
        result = f"{selectpart} {orderpart}"
        if limit is not None:
            result += f" LIMIT {limit}"
        if offset is not None:
            result += f" OFFSET {offset}"
        return result
    

    def _get_select_table_query(self, table: str|tuple = None, *, schema_only = False) -> str:
        """
        Build a query on the given table.

        If `schema_only` is given, no row will be returned (this is used to get information on the table).
        Otherwise, all rows will be returned.

        The return type of this function depends on the database engine.
        It is passed directly to the cursor's execute function for this engine.
        """
        schema, table = self.split_name(table)
        
        query = f'SELECT * FROM'
        if schema:
            query += f' {self.escape_identifier(schema)}.'
        query += f'{self.escape_identifier(table)}'
        if schema_only:
            query += ' WHERE 1 = 0'

        return query
    

    @classmethod
    def escape_identifier(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"Invalid identifier: {value} ({type(value)})")
        return f"{cls.identifier_quotechar_begin}{value.replace(cls.identifier_quotechar_end, cls.identifier_quotechar_end+cls.identifier_quotechar_end)}{cls.identifier_quotechar_end}"
    

    @classmethod
    def escape_literal(cls, value) -> str:
        if value is None:
            return "null"
        else:
            return f"'" + str(value).replace("'", "''") + "'"
    
    
    #endregion
    

    #region Execution

    def execute_query(self, query: str, params: list|tuple|dict = None, *, cursor: T_Cursor = None, traverse: bool|Literal['warn'] = False, tz: tzinfo = None, limit: int = None, offset: int = None, query_id = None) -> DbResult[T_Connection, T_Cursor]:
        if limit is not None or offset is not None:
            query, _ = self.get_paginated_select_queries(query, limit=limit, offset=offset)
        
        # Example of positional param: cursor.execute("INSERT INTO foo VALUES (%s)", ["bar"])
        # Example of named param: cursor.execute("INSERT INTO foo VALUES (%(foo)s)", {"foo": "bar"})
        if params is None:
            params = []
        elif isinstance(params, dict) and self.only_positional_params:
            query, params = self.to_positional_params(query, params)

        if not cursor:
            cursor = self.cursor().__enter__() # will be closed in Db's next cursor() method, or in the final close() method

        with self._register_notice_handler(cursor, query_id=query_id):
            # Execute query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self._log_cursor_notices(cursor)

            if traverse:
                rows, columns = self._traverse_cursor(cursor, warn=traverse == 'warn', query_id=query_id)
            elif cursor.description:
                # None indicates to QueryResults to use the cursor
                rows, columns = None, [info[0] for info in cursor.description]
            else:
                rows, columns = [], []

            # Handle results
            return DbResult(self, cursor, rows=rows, columns=columns, query_id=query_id, tz=tz)

    
    def _register_notice_handler(self, cursor: T_Cursor, query_id = None):
        """
        Register a handle for messages produced during execution of a query or procedure.
        """
        return nullcontext()
    

    def _log_cursor_notices(self, cursor: T_Cursor):
        """
        Log messages produced during execution of a query or procedure, if this cannot be done through `_register_notice_handler`.
        """
        pass
    

    def _traverse_cursor(self, cursor: T_Cursor, *, warn: bool, query_id) -> tuple[list[tuple]|None, list[str]]:
        """
        Move to last result set of the cursor, returning (last_rows, last_columns).
        Useful mostfly for pyodbc on stored procedures.
        """
        if not cursor.description:
            # [] indicates to QueryResults that there are no rows
            return [], []
        
        columns = [info[0] for info in cursor.description]

        if warn:
            self._warn_if_rows(cursor, columns=columns, query_id=query_id)
            # [] indicates to QueryResults to not report rows that we just warned about
            return [], columns
        
        else:
            # None indicates to QueryResults to use the cursor
            return None, columns
        

    def _warn_if_rows(self, cursor: T_Cursor, *, columns: list[str], query_id):
        top_rows = []
        there_are_more = False
        iterator = iter(cursor)
        try:
            for i in range(11):
                row = next(iterator)
                if i < 10:
                    top_rows.append(row)
                else:
                    there_are_more = True
        except StopIteration:
            pass
        
        if not top_rows:
            return
        
        fp = StringIO()
        with (TabDumper if not TabDumper.missing_dependency else CsvDumper)(fp, headers=columns) as dumper:
            for row in top_rows:
                dumper.append(row)
        text_rows = fp.getvalue()

        if there_are_more:
            text_rows += "\n…"

        self._logger.warning("Result set for query%s contain rows:\n%s", f" {query_id}" if query_id is not None else "", text_rows)


    def execute_file(self, path: str|Path, params: list|tuple|dict = None, *, cursor: T_Cursor = None, traverse: bool|Literal['warn'] = True, tz: tzinfo = None, limit: int = None, offset: int = None, query_id = None, encoding = 'utf-8', **file_kwargs) -> DbResult[T_Connection, T_Cursor]:
        file_content = files.read_text(path, encoding=encoding)

        if file_kwargs:
            file_content = file_content.format(**{key: '' if value is None else value for key, value in file_kwargs.items()})

        if self.split_multi_statement_files and ';' in file_content:
            # Split queries
            import sqlparse  # not at the top because the enduser might not need this feature
            queries = sqlparse.split(file_content, encoding)
            
            # Execute all queries
            query_count = len(queries)
    
            if not cursor:
                cursor = self.cursor().__enter__() # will be closed in Db's next cursor() method, or in the final close() method
        
            for index, query in enumerate(queries):
                query_num = index + 1
                if self._logger.isEnabledFor(logging.DEBUG):
                    title = re.sub(r"\s+", " ", query).strip()[0:100] + "…"
                    self._logger.debug("Execute query %d/%d: %s ...", query_num, query_count, title)

                # Execute query
                if query_id is not None and query_count > 1:
                    sub_id = f'{query_id}:{query_num}/{query_count}'
                elif query_id is not None or query_count > 1 :
                    sub_id = query_id
                elif query_count > 1:
                    sub_id = f'{query_num}/{query_count}'
                else:
                    sub_id = None
                
                results = self.execute_query(query, params, cursor=cursor, traverse='warn' if query_num < query_count else traverse, tz=tz, query_id=sub_id, limit=limit, offset=offset)

            return results
        else:
            return self.execute_query(file_content, params, cursor=cursor, traverse=traverse, tz=tz, limit=limit, offset=offset, query_id=query_id)
        
    
    def execute_function(self, name: str|tuple, params: list|tuple|dict = None, *, cursor: T_Cursor = None, traverse: bool|Literal['warn'] = True, tz: tzinfo = None, limit: int = None, offset: int = None, query_id = None, caller='SELECT', params_parenthesis=True) -> DbResult[T_Connection, T_Cursor]:
        schema, name = self.split_name(name)
        
        sql = f"{caller} "
        if not schema and self.function_requires_schema:
            schema = self.default_schema
        if schema:    
            sql += f"{self.escape_identifier(schema)}."
        sql += f"{self.escape_identifier(name)} "

        if params_parenthesis:
            sql += "("
                
        if isinstance(params, dict):
            list_params = []
            first = True
            for key, value in enumerate(params):
                if not key:
                    raise ValueError(f"Parameter cannot be empty")
                elif not re.match(r'^[\w\d0-9_]+$', key): # for safety
                    raise ValueError(f"Parameter contains invalid characters: {key}")
                
                if first:
                    first = False
                else:
                    sql += ','

                sql += f'{key}={self.sql_placeholder}'
                list_params.append(value)
                params = list_params
        elif params:
            sql += ','.join([self.sql_placeholder] * len(params))
    
        if params_parenthesis:
            sql += ")"

        if not query_id:
            query_id = f"{schema + '.' if schema and schema != self.default_schema else ''}{name}"

        return self.execute_query(sql, params, cursor=cursor, traverse=traverse, tz=tz, limit=limit, offset=offset, query_id=query_id)
    

    def execute_procedure(self, name: str|tuple, params: list|tuple|dict = None, *, cursor: T_Cursor = None, traverse: bool|Literal['warn'] = True, tz: tzinfo = None, limit: int = None, offset: int = None, query_id = None) -> DbResult[T_Connection, T_Cursor]:
        return self.execute_function(name, params, cursor=cursor, traverse=traverse, tz=tz, limit=limit, offset=offset, query_id=query_id, caller=self.procedure_caller, params_parenthesis=self.procedure_params_parenthesis)


    #endregion


    #region Results

    def get_scalar(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, cursor=cursor, limit=limit, offset=offset)
            row = results.single()
            return row[0]


    def get_tuple(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, cursor=cursor, limit=limit, offset=offset)
            row = results.single()
            return row.as_tuple()


    def get_dict(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, limit=limit, offset=offset, cursor=cursor)
            row = results.single()
            return row.as_dict()
    

    def get_scalars(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        scalars = []

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, cursor=cursor, limit=limit, offset=offset)
            for row in results:
                scalars.append(row[0])

        return scalars


    def iter_dicts(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, limit=limit, offset=offset, cursor=cursor)
            for row in results:
                yield row.as_dict()
                
    
    def get_dicts(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, limit=limit, offset=offset, cursor=cursor)
            return results.as_dicts()
    

    def get_paginated_dicts(self, query: str, params: list|dict = None, *, limit: int, offset: int = 0, cursor: T_Cursor = None):
        paginated_query, total_query = self.get_paginated_select_queries(query, limit=limit, offset=offset)

        rows = self.get_dicts(paginated_query, params, cursor=cursor)
        total = self.get_scalar(total_query, params, cursor=cursor)
        return {"rows": rows, "total": total}

    #endregion


    #region Schemas, tables and columns

    def split_name(self, name: str|tuple|type = None) -> tuple[str|None,str]:
        if name is None:
            if not self.table:
                raise ValueError("No table given")
            return self.schema, self.table        
        elif isinstance(name, tuple):
            return name
        elif isinstance(name, str):
            pass
        else:
            meta = getattr(name, '_meta', None) # Django model
            if meta:
                name: str = meta.db_table
            else:
                raise TypeError(f'name: {type(name).__name__}')
        
        try:
            pos = name.index('.')
            schema = name[0:pos]
            name = name[pos+1:]
        except ValueError:
            schema = None
            name = name

        return (schema, name)
    

    def table_exists(self, table: str|tuple = None, *, cursor: T_Cursor = None) -> bool:
        raise NotImplementedError()

   
    def schema_exists(self, schema: str = None, *, cursor: T_Cursor = None) -> bool:        
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")
        raise NotImplementedError()
        

    def get_columns(self, table_or_cursor: str|tuple|T_Cursor = None, *, cursor: T_Cursor = None) -> list[str]:
        if table_or_cursor is None or isinstance(table_or_cursor, (str,tuple)):
            # table_or_cursor is assumed to be a table name (use self.table if None) 
            query = self._get_select_table_query(table_or_cursor, schema_only=True)
            with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
                cursor.execute(query)
                return self.get_columns(cursor)
        else:
            # table_or_cursor is assumed to be a cursor
            if not table_or_cursor.description:
                raise ValueError("No results in last executed query (no cursor description available)")
            return [info[0] for info in table_or_cursor.description]
        

    def get_headers(self, object: str|tuple|T_Cursor = None, *, cursor: T_Cursor = None, typeonly = False) -> list[Header]:
        """
        Get the headers for the given table, cursor, or Django model.

        The following Header attributes are set (when possible):
        - `name`: set to the name of the table or cursor columns, or of the Django model columns.
        - `null`: indicate whether the column in nullable.
        
        If `typeonly`, do not retrieve primary key, unique key and identity information.
        """
        if object is None or isinstance(object, (str,tuple)): # `object` is assumed to be a table name (use `self.table` if `object` is `None`)
            schema, table = self.split_name(object)

            with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
                result = self._get_table_columns((schema, table), cursor=cursor, typeonly=typeonly)
                
                if isinstance(result, tuple):
                    columns, indexes = result
                else:
                    columns = result
                    indexes = None

                headers = [self._get_header_from_table_column(column) for column in columns]

                if indexes:
                    headers_by_name = {header.name: header for header in headers}
                    for header in headers:
                        headers_by_name[header.name] = header
                        # Set defaults
                        if header.unique is None:
                            header.unique = False
                        if header.primary_key is None:
                            header.primary_key = False
                        if header.identity is None:
                            header.identity = False

                    for index in indexes:
                        columns = index['columns']
                        if isinstance(columns, str):
                            columns = columns.split(',')
                        
                        for name in columns:
                            header = headers_by_name[name]
                            if index['unique']:
                                if len(columns) == 1:
                                    header.unique = True
                                elif not header.unique:
                                    header.unique = [columns]
                                else:
                                    header.unique.append(tuple(columns))
                            if index['primary_key']:
                                header.primary_key = True
                            if index.get('identity'):
                                header.identity = True
                
                return headers

        elif isinstance(object, type): # `object` is assumed to be a Django model
            return self._get_model_headers(object, typeonly=typeonly)

        else: # `object` is assumed to be a cursor
            if not object.description:
                raise ValueError("No results in last executed query (no cursor description available)")
            return self._get_cursor_headers(object)
    
    
    def _get_header_from_table_column(self, column: Header|dict):
        if isinstance(column, dict):
            header = Header(**column)
        elif isinstance(column, Header):
            header = column
        else:
            raise TypeError(f"column: {column}")
        
        # Set type from sql type
        if not header.type and header.sql_type:
            if header.sql_type.endswith('[]'):
                header.type = list
            elif 'char' in header.sql_type or 'text' in header.sql_type:
                header.type = str
            elif header.sql_type.startswith('int') or header.sql_type in {'bigint', 'smallint', 'tinyint'}:
                header.type = int
            elif header.sql_type.startswith('bool') or (self.scheme == 'sqlserver' and header.sql_type == 'bit'):
                header.type = bool
            elif header.sql_type.startswith(('float','double','real')):
                header.type = float
            elif header.sql_type in {'numeric', 'decimal'}:
                header.type = Decimal
            elif header.sql_type.startswith(('timestamp','datetime')):
                header.type = datetime
            elif header.sql_type == 'date':
                header.type = date

        # Update type of default
        if isinstance(header.default, str) and header.default != header.DEFAULT_NOW and header.type is not None and not isinstance(header.type, str):
            header.default = convert(header.default, header.type)

        return header
            

    def _get_table_columns(self, table, *, cursor, typeonly: bool) -> Generator[dict,Any,Any]|list[Header|dict]|tuple[list[dict],list[dict]]:
        """
        Return either list of columns (as Header or dict) or a tuple (columns, indexes).
        """
        raise NotImplementedError()
    

    def _get_model_headers(self, model, *, typeonly = False) -> Iterable[Header]:
        from django.db import models

        from zut.django import get_field_python_type, get_model_unique_keys

        field: models.Field
       
        headers: dict[str,Header] = {}

        for field in model._meta.fields:
            header = Header(field.attname)

            _type = get_field_python_type(field)
            if _type:
                header.type = _type
                if isinstance(field, models.DecimalField):
                    header.sql_precision = field.max_digits
                    header.sql_scale = field.decimal_places
                elif isinstance(field, models.CharField):
                    header.sql_precision = field.max_length

            header.null = field.null

            if field.primary_key:
                header.primary_key = True
            if field.unique:
                header.unique = True

            headers[header.name] = header

        if not typeonly:
            unique_keys = get_model_unique_keys(model)
            for key in unique_keys:
                if len(key) == 1:
                    header = headers[key[0]]
                    header.unique = True
                else:
                    for field in key:
                        header = headers[field]
                        if not headers[field].unique:
                            header.unique = [key]
                        elif not headers[field].unique is True:
                            header.unique.append(key)

        return headers.values()


    def _get_cursor_headers(self, cursor: T_Cursor) -> list[Header]:
        # ROADMAP: retrieve more Header settings
        return [Header(info[0]) for info in cursor.description]
    

    def get_sql_fulltype(self, _type: type|Header, precision: int|None = None, scale: int|None = None, *, key = False):
        if isinstance(_type, Header):
            header = _type
            sql_type = header.sql_type
            _type = header.type
            if precision is None:
                precision = header.sql_precision
            if scale is None:
                scale = header.sql_scale
            if key is None:
                key = header.unique
            if _type is None:
                if header.default is not None:
                    if header.default == header.DEFAULT_NOW:
                        _type = datetime
                    else:
                        _type = type(header.default)
                else:
                    _type = str
        else:
            if not isinstance(_type, type):
                raise TypeError(f"_type: {type(_type)}")
            header = None
            sql_type = None
        
        if not sql_type:
            if issubclass(_type, bool):
                sql_type = self.bool_sql_type
            elif issubclass(_type, int):
                sql_type = self.int_sql_type
            elif issubclass(_type, float):
                sql_type = self.float_sql_type
            elif issubclass(_type, Decimal):
                if self.decimal_sql_type == 'text':
                    sql_type = self.decimal_sql_type
                else:
                    if precision is None:
                        raise ValueError("Precision must be set for decimal values")
                    if scale is None:
                        raise ValueError("Scale must be set for decimal values")
                    sql_type = self.decimal_sql_type
            elif issubclass(_type, datetime):
                sql_type = self.datetime_sql_type
            elif issubclass(_type, date):
                sql_type = self.date_sql_type
            else: # use str
                if precision is not None:
                    sql_type = self.str_precised_sql_type
                elif key:
                    sql_type = self.str_precised_sql_type
                    precision = 255 # type for key limited to 255 characters (max length for a 1-bit length VARCHAR on MariaDB)
                else:
                    sql_type = self.str_sql_type

        if header:
            header.sql_type = sql_type
            if precision is not None:
                header.sql_precision = precision
            if scale is not None:
                header.sql_scale = scale

        result = sql_type
        if precision is not None or scale is not None:
            result += '('
            if precision is not None:
                result += str(precision)                
            if scale is not None:
                if precision is not None:
                    result += ','
                result += str(scale)
            result += ')'

        return result


    def get_sql_column_definition(self, columns: Iterable[Header|str]|Header|str, *, separator = ',', skip_notnull = False, skip_primary_key: bool|Literal['raise'] = False):
        if isinstance(columns, Header):
            columns = [columns]
        
        sql = ""
        for column in columns:
            if not isinstance(column, Header):
                column = Header(column)
            
            if sql:
                sql += separator

            sql += f"{self.escape_identifier(column.name)} {self.get_sql_fulltype(column)} {'NOT NULL' if not skip_notnull and (column.null is False or column.primary_key) else 'NULL'}"

            if column.primary_key:
                if skip_primary_key:
                    if skip_primary_key == 'raise':
                        raise ValueError(f"Cannot add primary key colunm: {column}")
                else:
                    sql += " PRIMARY KEY"
            elif column.unique is True:
                sql += " UNIQUE"
            
            if column.identity:
                sql += f" {self.identity_definition_sql}"

            if column.default is not None:
                if column.default == Header.DEFAULT_NOW:
                    escaped_default = 'CURRENT_TIMESTAMP'
                elif isinstance(column.default, str) and column.default.startswith('sql:'):
                    escaped_default = column.default[len('sql:'):]
                else:
                    escaped_default = self.escape_literal(column.default)

                sql += f" DEFAULT {escaped_default}"

        return sql
    

    def drop_table(self, table: str|tuple = None, *, if_exists = False, cursor: T_Cursor = None):
        schema, table = self.split_name(table)
        
        query = "DROP TABLE "
        if if_exists:
            query += "IF EXISTS "
        if schema:    
            query += f"{self.escape_identifier(schema)}."
        query += f"{self.escape_identifier(table)}"

        with self.cursor(autoclose=False) as cursor:
            self.execute_query(query, cursor=cursor)
    

    def truncate_table(self, table: str|tuple = None, *, if_exists = False, cascade = False, cursor: T_Cursor = None):
        if cascade:
            if not self.can_cascade_truncate or self.truncate_with_delete:
                raise ValueError(f"Cannot use cascade truncate with {self.__class__.__name__}")

        if self.truncate_with_delete:
            self.erase_table(table, if_exists=if_exists)
            return
        
        schema, table = self.split_name(table)
        
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            if if_exists:
                if not self.table_exists((schema, table), cursor=cursor):
                    return
            
            query = "TRUNCATE TABLE "    
            if schema:    
                query += f"{self.escape_identifier(schema)}."
            query += f"{self.escape_identifier(table)}"

            if cascade:
                query += " CASCADE"

            self.execute_query(query, cursor=cursor)


    def erase_table(self, table: str|tuple = None, *, if_exists = False, cursor: T_Cursor = None):
        schema, table = self.split_name(table)

        if if_exists:
            if not self.table_exists((schema, table), cursor=cursor):
                return
        
        query = "DELETE FROM "          
        if schema:    
            query += f"{self.escape_identifier(schema)}."
        query += f"{self.escape_identifier(table)}"

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            self.execute_query(query, cursor=cursor)


    def create_table(self, table: str|tuple, columns: Iterable[str|Header], *, if_not_exists = False, cursor: T_Cursor = None):
        """
        Create a table from a list of columns.

        NOTE: This method does not intend to manage all cases, but only those usefull for zut library internals.
        """
        schema, table = self.split_name(table)
        
        columns = [Header(column) if not isinstance(column, Header) else column for column in columns]

        sql = "CREATE "
        if schema in {'pg_temp', 'temp'}:
            sql += "TEMPORARY "
        sql += "TABLE "
        if if_not_exists:
            sql += "IF NOT EXISTS "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += f"{self.escape_identifier(table)}("

        all_columns: list[Header] = []
        primary_key_columns: list[Header] = []
        unique_keys: list[tuple] = []
        for column in columns:
            if not isinstance(column, Header):
                column = Header(column)
            
            all_columns.append(column)
            if column.primary_key:
                primary_key_columns.append(column)

            if isinstance(column.unique, list):
                for key in column.unique:
                    if not key in unique_keys:
                        unique_keys.append(key)

        sql += self.get_sql_column_definition(columns, separator=',')

        # Several primary keys ?
        if len(primary_key_columns) > 1:
            sql += ",PRIMARY KEY("
            for i, column in enumerate(primary_key_columns):
                sql += ("," if i > 0 else "") + f"{self.escape_identifier(column.name)}"
            sql += ")" # end PRIMARY KEY

        # Unique together ?
        for unique_key in unique_keys:
            sql += ",UNIQUE("
            for i, key in enumerate(unique_key):
                sql += ("," if i > 0 else "") + f"{self.escape_identifier(key)}"
            sql += ")" # UNIQUE
        
        sql += ")" # end CREATE TABLE

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            self.execute_query(sql, cursor=cursor)


    def add_table_columns(self, table: str|tuple, columns: list[str|Header], *, keep_notnull = False, cursor: T_Cursor = None):
        """
        Add column(s) to a table.

        NOTE: This method does not intend to manage all cases, but only those usefull for zut library internals.
        """    
        if len(columns) > 1 and not self.can_add_several_columns:
            for column in columns:
                self.add_table_columns(table, [column], keep_notnull=keep_notnull)
            return

        schema, table = self.split_name(table)
        
        sql = "ALTER TABLE "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += self.escape_identifier(table)
        sql += f" ADD "
        sql += self.get_sql_column_definition(columns, skip_notnull=not keep_notnull, skip_primary_key='raise')

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            self.execute_query(sql, cursor=cursor)


    @classmethod
    def get_temp_table_name(cls, base: str):
        return f"{cls.temporary_prefix}{slugify(base, separator='_')[:40]}_tmp_{token_hex(4)}"
   

    def drop_schema(self, schema: str = None, *, if_exists = False, cursor: T_Cursor = None):
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")
        
        if not schema:
            schema = self.schema or self.default_schema
            if not schema:
                raise ValueError("No schema defined for this Db")
        
        query = "DROP SCHEMA "
        if if_exists:
            query += "IF EXISTS "
        query += f"{self.escape_identifier(schema)}"
        
        with self.cursor(autoclose=False) as cursor:
            self.execute_query(query, cursor=cursor)
    

    def create_schema(self, schema: str = None, *, if_not_exists = False, cursor: T_Cursor = None):
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")

        if not schema:
            schema = self.schema or self.default_schema
            if not schema:
                raise ValueError("No schema defined for this Db")
        
        query = "CREATE SCHEMA "
        if if_not_exists:
            if self.scheme == 'sqlserver':
                if self.schema_exists(schema, cursor=cursor):
                    return
            else:
                query += "IF NOT EXISTS "
        query += f"{self.escape_identifier(schema)}"
        
        with self.cursor(autoclose=False) as cursor:
            self.execute_query(query, cursor=cursor)

    # endregion


    #region Convert    

    def convert_value(self, value: Any):
        """ Convert a value to types supported by the underlying connection. """        
        if isinstance(value, (Enum,Flag)):
            return value.value
        elif isinstance(value, (datetime,time)):
            if value.tzinfo:
                if self.accept_aware_datetime:
                    return value
                elif self.tz:
                    value = make_naive(value, self.tz)
                else:
                    raise ValueError(f"Cannot store tz-aware datetimes with {type(self).__name__} without providing `tz` argument")
            return value
        else:
            return value

    #endregion


    #region Migrate

    def migrate(self, dir: str|Path, *, cursor: T_Cursor = None, **file_kwargs):        
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            last_name = self.get_last_migration_name(cursor=cursor)

            if last_name is None:
                sql_utils = self.get_sqlutils_path()
                if sql_utils:
                    self._logger.info("Deploy SQL utils ...")
                    self.execute_file(sql_utils, cursor=cursor)

                self._logger.info("Create migration table ...")
                self.execute_query(f"CREATE TABLE migration(id {self.int_sql_type} NOT NULL PRIMARY KEY {self.identity_definition_sql}, name {self.get_sql_fulltype(str, key=True)} NOT NULL UNIQUE, deployed_utc {self.datetime_sql_type}{f'({self.datetime_sql_precision})' if self.datetime_sql_precision is not None else ''} NOT NULL)", cursor=cursor)
                last_name = ''
            
            for path in sorted((dir if isinstance(dir, Path) else Path(dir)).glob('*.sql')):
                if path.stem == '' or path.stem.startswith('~') or path.stem.endswith('~'):
                    continue # skip
                if path.stem > last_name:
                    self._apply_migration(path, cursor=cursor, **file_kwargs)


    def _apply_migration(self, path: Path, *, cursor: T_Cursor = None, **file_kwargs):
        self._logger.info("Apply migration %s ...", path.stem)

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            self.execute_file(path, cursor=cursor, **file_kwargs)
            self.execute_query(f"INSERT INTO migration (name, deployed_utc) VALUES({self.sql_placeholder}, {self.sql_placeholder})", [path.stem, self.convert_value(now_naive_utc())], cursor=cursor)


    def get_last_migration_name(self, *, cursor: T_Cursor = None) -> str|None:
        if not self.table_exists("migration", cursor=cursor):
            return None
        
        try:
            return self.get_scalar("SELECT name FROM migration ORDER BY name DESC", limit=1, cursor=cursor)
        except NotFoundError:
            return ''

    #endregion


    #region Check if available
                
    def is_available(self, *, migration: tuple[str,str]|str = None):
        if migration:
            if isinstance(migration, tuple):
                migration_app, migration_name = migration
            else:
                pos = migration.index(':')
                migration_app = migration[:pos]
                migration_name = migration[pos+1:]
        
        try:
            with self.cursor():
                if migration:
                    from django.db.migrations.recorder import MigrationRecorder
                    recorder = MigrationRecorder(self.connection)
                    recorded_migrations = recorder.applied_migrations()
                    for an_app, a_name in recorded_migrations.keys():
                        if an_app == migration_app and a_name == migration_name:
                            return True
                    return False
                else:
                    return True
        except:
            return False
        
    #endregion


    #region Load (copy and merge)

    def load_from_csv(self,
                    csv_files: Path|str|IOBase|list[Path|str|IOBase],
                    table: str|tuple|type = None,
                    *,
                    headers: list[Header|str] = None,
                    optional: str|Sequence[str]|Literal['*',True]|None = None,
                    merge: Literal['append','truncate','create','recreate','auto','auto|append','auto|truncate']|tuple[Header|str]|list[Header|str] = 'auto',
                    create_model: str|tuple|type|list[Header] = None,
                    create_pk: bool|str = None,
                    create_additional: dict[str|Any]|list[Header] = None,
                    consts: dict[str|Any] = None,
                    insert_consts: dict[str|Any] = None,
                    foreign_keys: list[FK] = None,
                    # CSV format
                    encoding = 'utf-8',
                    delimiter: str = None,
                    decimal_separator: str = None,
                    quotechar = '"',
                    nullval: str = None,
                    no_headers: bool = None,
                    # Title and file helpers (similar to zut.load_tabular())                            
                    title: str|bool = False,
                    src_name: str|bool|None = None,
                    dir: str|Path|Literal[False]|None = None,
                    **kwargs) -> int:
        """
        Load CSV file(s) to a table. The table will be created if it does not already exist.
        
        - `headers`: list of CSV headers to use. If not provided, headers will be determined from the first line of the first input CSV file.
        
        - `optional`: optional headers will be discared if they do not exist in the destination.

        - `merge`:
            - If `append`, data will simply be appended.
            - If `truncate`, destination table will be created if it does not already exist, or truncated if it already exists.
            - If `create`, destination table will be created if it does not already exist. Data will simply be appended.
            - If `recreate`, destination table will be droped if exist, and (re)created.
            - If a tuple (or list), reconciliate using the given header names as keys.
            - If `auto` or `auto|append` (default):
                - [`id`] if header `id` is present in the CSV headers;
                - or the first unique key found in `create_model` if given;
                - or the first unique key in the destination table;
                - or (if there is no unique key): `append`.
            - If `auto|truncate`, same as `auto` but if no key is found, truncate destination table before.

        - `create_pk`: if a non-empty string or True (means `id`), destination table will be created (if necessary) with
        an auto-generated primary key named as the value of `create_pk`, if it is not already in CSV headers.

        - `create_model`: can be a Django model, the name (or tuple) of a table, or a list of columns. If set, destination
        table will be created (if necessaray) with SQL types and unique keys matching `create_model` columns.

        - `create_additional`: can be a dictionnary (column name: default value) or a list of columns. If set, destination
        table will be created (if necessary) with these columns (in addition to those provided by `create_model` if any).

        - `consts`: set constant values when a row is inserted or updated (during a merge). If the colunm name (key of the
        dictionnary) ends with '?', there will first be a check that the column exist and the constant will be ignored
        if the column does not exist.

        - `insert_consts`: same as `consts` but only set when a row is inserted.
        """

        # Prepare csv_files and table parameters
        target_model = None
        if not table:
            if not self.table:
                raise ValueError("No table given")
            schema, table = self.split_name(table)
        elif isinstance(table, (str,tuple)):
            schema, table = self.split_name(table)
        elif isinstance(table, type): # Django model
            target_model = table
            schema = self.default_schema
            table = table._meta.db_table
        else:
            raise TypeError(f"table: {table}")

        if isinstance(csv_files, (Path,str,IOBase)):
            csv_files = [csv_files]
        if not csv_files:
            raise ValueError("csv_files cannot be empty")
        for i in range(len(csv_files)):
            if not isinstance(csv_files[i], IOBase):
                if dir is not False:
                    csv_files[i] = files.indir(csv_files[i], dir, title=title, **kwargs)
                if not files.exists(csv_files[i]):
                    raise FileNotFoundError(f"Input CSV file does not exist: {csv_files[i]}")
                
        if title:
            if src_name is None or src_name is True:
                if len(csv_files) == 1:
                    src = csv_files[0]
                    if isinstance(src, IOBase):
                        src_name = getattr(src, 'name', f'<{type(src).__name__}>')
                    else:
                        src_name = src
            self._logger.info(f"Load{f' {title}' if title and not title is True else ''}{f' from {src_name}' if src_name else ''} …")
        
        # Determine merge param
        if merge is None or merge in {'auto', 'auto|append', 'auto|truncate'}:
            merge = self.get_load_auto_key(target_model or (schema, table), input_headers=headers or csv_files[0], convert_to_input=not target_model, default='truncate' if 'truncate' in merge else 'append', encoding=encoding, delimiter=delimiter, quotechar=quotechar)
        elif isinstance(merge, (list,tuple)):
            merge = tuple(column.name if isinstance(column, Header) else column for column in merge)            
            for i, column in enumerate(merge):
                if not isinstance(column, str):
                    raise TypeError(f"merge[{i}]: {type(column).__name__}")
        elif isinstance(merge, str):
            if not merge in {'append', 'truncate', 'create', 'recreate'}:
                raise ValueError(f"Invalid merge value: {merge}")
        else:
            raise TypeError(f"merge: {type(merge).__name__}")
        
        # Determine CSV parameters and headers
        if not delimiter:
            if isinstance(merge, self._LoadCacheMixin):
                delimiter = merge._delimiter

        if not delimiter or (not headers and not no_headers):
            examined_columns, examined_delimiter, _ = examine_csv_file(csv_files[0], encoding=encoding, delimiter=delimiter, quotechar=quotechar, force_delimiter=False)
            if not delimiter:
                delimiter = examined_delimiter or get_default_decimal_separator()
            if not headers and not no_headers:
                headers = examined_columns

        if not decimal_separator:
            decimal_separator = get_default_decimal_separator(csv_delimiter=delimiter)

        if not headers and isinstance(merge, self._LoadCacheMixin):
            headers = merge._headers

        if headers:
            headers = [header if isinstance(header, Header) else Header(header) for header in headers]

        if optional:
            if optional == '*':
                optional = True
            elif isinstance(optional, str):
                optional = [str]

        nonoptional_headers = headers
        has_optional_headers = False
        
        # Add foreign keys from Django model
        if target_model and foreign_keys is None:
            foreign_keys = self._get_load_foreign_keys(headers, target_model)

        foreign_keys_by_source_column_name: dict[str,FK] = {}
        if foreign_keys:
            for foreign_key in foreign_keys:
                for column in foreign_key.source_columns:
                    foreign_keys_by_source_column_name[column] = foreign_key

        # Start transaction with database
        total_rowcount = 0
        with self.transaction():
            # Determine if we must (re)create the destination table
            if isinstance(merge, self._LoadCacheMixin) and merge._model_table_exists is not None and merge._model == (schema, table):
                table_existed = merge._model_table_exists
            else:
                table_existed = self.table_exists((schema, table))

            if table_existed:
                if merge == 'recreate':
                    self._logger.debug(f"Drop table {f'{schema}.' if schema else ''}{table}") 
                    self.drop_table((schema, table))                        
                    must_create = True
                else:
                    must_create = False
            else:
                must_create = True

            # Create the destination table
            if must_create:
                if not headers:
                    raise ValueError(f"Cannot create table without headers")

                # (adapt headers to `create_model`)
                if create_model:
                    if isinstance(create_model, str):
                        create_model = self.split_name(create_model)
                    
                    if isinstance(merge, self._LoadCacheMixin) and merge._model_columns_by_name is not None and merge._model == create_model:
                        model_columns_by_name = merge._model_columns_by_name
                    else:
                        model_columns_by_name = self._get_load_model_columns_by_name(create_model)

                    for column in headers:
                        model_column = model_columns_by_name.get(column.name)
                        if model_column:
                            if model_column.identity:
                                raise ValueError("Cannot load an identity column")
                            column.merge(model_column)
                
                # (ensure a unique key is created for the merge key)
                if isinstance(merge, tuple):
                    for column in headers:
                        if column.name in merge:
                            if not column.unique:
                                column.unique = [merge]
                            elif isinstance(column.unique, list):
                                if not merge in column.unique:
                                    column.unique.append(merge)

                destination_columns_by_name: dict[str,Header] = {}
                for header in headers:
                    foreign_key = foreign_keys_by_source_column_name.get(header.name)
                    if foreign_key:
                        if foreign_key.destination_column not in destination_columns_by_name:
                            column = Header(foreign_key.destination_column)
                            column.type = foreign_key.related_pk_type if foreign_key.related_pk_type else int
                            destination_columns_by_name[header.name] = column
                    else:
                        destination_columns_by_name[header.name] = header

                if create_additional:
                    if isinstance(create_additional, dict):
                        create_additional: list[Header] = [Header(name, default=default, null=default is None) for (name, default) in create_additional.items()]
                    else:
                        for i in range(len(create_additional)):
                            if not isinstance(create_additional[i], Header):
                                create_additional[i] = Header(create_additional)

                    for column in create_additional:
                        if not column.name in destination_columns_by_name:
                            destination_columns_by_name[column.name] = column

                if create_pk:
                    if not isinstance(create_pk, str):
                        create_pk = 'id'
                    pk_found = False

                    for column in headers:
                        if column.primary_key or column.name == create_pk:
                            pk_found = True
                            column.primary_key = True

                    if not pk_found:
                        pk_column = Header(create_pk, primary_key=True, identity=True, sql_type='bigint')
                        destination_columns_by_name = {pk_column.name: pk_column, **destination_columns_by_name}
                        
                self._logger.debug(f"Create destination table {f'{schema}.' if schema else ''}{table}")
                if schema:
                    self.create_schema(schema, if_not_exists=True)
                self.create_table((schema, table), destination_columns_by_name.values())

            # Update headers with types from existing destination table
            else:
                if isinstance(merge, self._LoadCacheMixin) and merge._model_columns_by_name is not None and merge._model == (schema, table):
                    destination_columns_by_name = merge._model_columns_by_name
                else:
                    destination_columns_by_name = {column.name: column for column in self.get_headers((schema, table), typeonly=True)}

                # (select headers that are in destination table or foreign keys, if optional is set)
                nonoptional_headers: list[Header] = []
                for header in headers:
                    column = destination_columns_by_name.get(header.name)
                    if column:
                        header.merge(column)
                        nonoptional_headers.append(header)
                    else:
                        foreign_key = foreign_keys_by_source_column_name.get(header.name)
                        if foreign_key:
                            if foreign_key.related_pk_type:
                                header.type = foreign_key.related_pk_type
                            nonoptional_headers.append(header)
                        elif optional and (optional is True or header.name in optional):
                            has_optional_headers = True
                        else:
                            nonoptional_headers.append(header)
                
            # Remove optional consts if necessary
            def remove_optional_consts(consts: dict[str,Any]):
                if any(name.endswith('?') for name in consts.keys()):
                    new_consts = {}
                    for name, value in consts.items():
                        is_optional = name.endswith('?')
                        actual_name = name[:-1] if is_optional else name
                        if not is_optional or actual_name in destination_columns_by_name:
                            new_consts[actual_name] = value
                    return new_consts
                else:
                    return consts

            if consts:
                consts = remove_optional_consts(consts)
                    
            if insert_consts:
                insert_consts = remove_optional_consts(insert_consts)

            # Determine if we must perform conversions at load time
            conversions: dict[str,Header] = {}
            if decimal_separator != '.' and headers:
                for header in headers:
                    if header.type:
                        if issubclass(header.type, (float,Decimal)):
                            conversions[header.name] = header
                        elif issubclass(header.type, datetime):
                            if self.tz:
                                conversions[header.name] = header
                        elif issubclass(header.type, list):
                            conversions[header.name] = header
            
            # Truncate destination table
            if merge == 'truncate':
                if table_existed:
                    if self._logger.isEnabledFor(logging.DEBUG):
                        self._logger.debug(f"Truncate table {f'{schema}.' if schema else ''}{table}") 
                    self.truncate_table((schema, table))
            
            # Prepare temporary table if we're reconciliating
            if (isinstance(merge, tuple) and table_existed) or has_optional_headers or conversions or consts or insert_consts or foreign_keys:
                temp_table = self.get_temp_table_name(table)
                self.drop_table(temp_table, if_exists=True)                    
                self._logger.debug(f"Create {temp_table}")                                
                if not headers:
                    raise ValueError(f"Cannot create table without headers")
                self.create_table(temp_table, [Header(header.name, sql_type=self.str_sql_type if header.name in conversions else header.sql_type) for header in headers])
            else:
                temp_table = None # load directly to destination table
                
            # Perform actual copy of CSV files
            for csv_file in csv_files:                        
                if temp_table: # copy to temporary table if we're reconciliating
                    self._logger.debug(f"Load {temp_table} from csv file {csv_file}")
                    total_rowcount += self.copy_from_csv(csv_file, temp_table, headers, encoding=encoding, delimiter=delimiter, quotechar=quotechar, nullval=nullval, no_headers=no_headers)
                else:
                    self._logger.debug(f"Load table {f'{schema}.' if schema else ''}{table} from csv file {csv_file}")
                    total_rowcount += self.copy_from_csv(csv_file, (schema, table), headers, encoding=encoding, delimiter=delimiter, quotechar=quotechar, nullval=nullval, no_headers=no_headers)

            # Merge from temporary table to destination table if we're reconciliating
            if temp_table:
                if self._logger.isEnabledFor(logging.DEBUG):
                    msg = f"Merge {temp_table} to {f'{schema}.' if schema else ''}{table}"
                    if isinstance(merge, tuple):
                        msg += f" using key {', '.join(merge)}"
                    self._logger.debug(msg)
                
                self.merge_table(temp_table, (schema, table),
                                 columns=nonoptional_headers,
                                 key=merge if isinstance(merge, tuple) else None,
                                 consts=consts,
                                 insert_consts=insert_consts,
                                 foreign_keys=foreign_keys,
                                 conversions=conversions)
                
                self._logger.debug("Drop %s", temp_table)
                self.drop_table(temp_table)

        if title:
            self._logger.info(f"{total_rowcount:,}{f' {title}' if title and not title is True else ' rows'} imported{f' from {src_name}' if src_name else ''}")
        
        return total_rowcount


    def copy_from_csv(self,
                    csv_file: Path|str|IOBase,
                    table: str|tuple = None,
                    headers: list[Header|str] = None,
                    *,
                    buffer_size = 65536,
                    cursor: T_Cursor = None,
                    # CSV format
                    encoding = 'utf-8',
                    delimiter: str = None,
                    quotechar = '"',
                    nullval: str = None,
                    no_headers: bool = None) -> int:
        
        raise NotImplementedError() 


    def merge_table(self,
                    src_table: str|tuple,
                    dst_table: str|tuple = None,
                    columns: Iterable[Header|str] = None,
                    *,
                    key: str|tuple[str] = None,
                    consts: dict[str|Any] = None,
                    insert_consts: dict[str|Any] = None,
                    foreign_keys: list[FK] = None,
                    conversions: dict[str,str|type|Header] = {},
                    cursor: T_Cursor = None):
        
        # Prepare table arguments
        src_schema, src_table = self.split_name(src_table)

        if not dst_table:
            if not self.table:
                raise ValueError("No table given")
            dst_table = self.table
        dst_schema, dst_table = self.split_name(dst_table)

        # Prepare columns argument
        if columns:
            columns = [column.name if isinstance(column, Header) else column for column in columns]
        else:
            columns = self.get_columns((src_schema, src_table))

        foreign_keys_column_names = set()
        if foreign_keys:
            for foreing_key in foreign_keys:
                for column in foreing_key.source_columns:
                    foreign_keys_column_names.add(column)
        
        # Prepare SQL parts
        key_sql = ""
        if key:
            if isinstance(key, str):
                key = [key]
            for key_column in key:
                key_sql += (", " if key_sql else "") + self.escape_identifier(key_column)

        from_sql = (f"{self.escape_identifier(src_schema)}." if src_schema else "") + f"{self.escape_identifier(src_table)} s"

        insert_sql = ""
        select_sql = ""
        join_sql = ""
        set_sql = ""
        foreign_key_check_sqls: list[str] = []
        naive_tzkey = None

        def append_standard_column(column: str):
            nonlocal insert_sql, select_sql, set_sql, naive_tzkey

            conversion_fmt = '{value}'
            conversion = conversions.get(column)
            if conversion:
                if isinstance(conversion, Header):
                    conversion = self.get_sql_fulltype(conversion)
                elif isinstance(conversion, type):
                    if issubclass(conversion, Decimal):
                        conversion = self.float_sql_type # we cannot use decimal because we don't know precision and scale
                    else:
                        conversion = self.get_sql_fulltype(conversion)
                elif not isinstance(conversion, str):
                    raise TypeError(f"conversions[{column}]: {conversion}")
                
                if '{value}' in conversion:
                    conversion_fmt = conversion
                else:                
                    conversion = conversion.lower()
                    if conversion.endswith('[]'): # array
                        conversion_fmt = "CAST(string_to_array({value}, '|') AS "+conversion+")"
                    elif conversion.startswith(('float','double','real','decimal','numeric')):
                        conversion_fmt = "CAST(replace(replace({value}, ',', '.'), ' ', '') AS "+conversion+")"
                    elif conversion == 'timestamptz':
                        if not naive_tzkey:
                            if not self.tz:
                                raise ValueError("Cannot convert to timestamptz when tz not set")
                            naive_tzkey = get_tzkey(self.tz)
                        conversion_fmt = "CAST(CASE WHEN {value} SIMILAR TO '%[0-9][0-9]:[0-9][0-9]' AND SUBSTRING({value}, length({value})-5, 1) IN ('-', '+') THEN {value}::timestamptz ELSE {value}::timestamp AT TIME ZONE "+self.escape_literal(naive_tzkey)+" END AS "+conversion+")"
                    else:
                        conversion_fmt = "CAST({value} AS "+conversion+")"

            escaped_column_name = self.escape_identifier(column)

            insert_sql += (", " if insert_sql else "")       
            select_sql += (", " if select_sql else "")
            insert_sql += escaped_column_name
            select_sql += conversion_fmt.format(value=f"s.{escaped_column_name}")

            if key and not column in key:
                set_sql += (", " if set_sql else "") + f"{escaped_column_name} = excluded.{escaped_column_name}"

        def append_consts(consts: dict[str,Any], *, insert_only = False):
            nonlocal insert_sql, select_sql, set_sql

            if not consts:
                return
            
            for column_name, value in consts.items():
                escaped_column_name = self.escape_identifier(column_name)
                if value == Header.DEFAULT_NOW:
                    escaped_literal = 'CURRENT_TIMESTAMP'
                elif isinstance(value, str) and value.startswith('sql:'):
                    escaped_literal = value[len('sql:'):]
                else:
                    escaped_literal = self.escape_literal(value)

                insert_sql += (", " if insert_sql else "") + escaped_column_name
                select_sql += (", " if select_sql else "") + escaped_literal
                if not insert_only:
                    set_sql += (", " if set_sql else "") + f"{escaped_column_name} = excluded.{escaped_column_name}"

        def append_foreign_key(foreign_key: FK, alias: str):
            nonlocal insert_sql, select_sql, join_sql, set_sql, foreign_key_check_sqls

            escaped_destination_column_name = self.escape_identifier(foreign_key.destination_column)
            insert_sql += (", " if insert_sql else "") + escaped_destination_column_name
            select_sql += (", " if select_sql else "") + f"{alias}.{self.escape_identifier(foreign_key.related_pk)}"            
            if key and not foreign_key.destination_column in key:
                set_sql += (", " if set_sql else "") + f"{escaped_destination_column_name} = excluded.{escaped_destination_column_name}"

            my_join_sql = f"LEFT OUTER JOIN {self.escape_identifier(foreign_key.related_schema or self.default_schema)}.{self.escape_identifier(foreign_key.related_table)} {alias} ON "
            for i, source_column in enumerate(foreign_key.source_columns):
                foreign_column = foreign_key.related_columns[i]
                my_join_sql += (" AND " if i > 0 else "") + f"{alias}.{self.escape_identifier(foreign_column)} = s.{self.escape_identifier(source_column)}"
                
            join_sql += ("\n" if join_sql else "") + my_join_sql

            # Build check SQL
            columns_sql = ""
            columns_notnull_sql = ""
            for i, source_column in enumerate(foreign_key.source_columns):
                foreign_column = foreign_key.related_columns[i]
                columns_sql += (", " if i > 0 else "") + f"s.{self.escape_identifier(source_column)}"
                columns_notnull_sql += (" OR " if i > 0 else "") + f"s.{self.escape_identifier(source_column)} IS NOT NULL"
                
            check_sql = f"SELECT {columns_sql}"
            check_sql += f"\nFROM {from_sql}"
            check_sql += f"\n{my_join_sql}"
            check_sql += f"\nWHERE ({columns_notnull_sql})"
            check_sql += f"\nAND {alias}.{self.escape_identifier(foreign_key.related_pk)} IS NULL"
            check_sql += f"\nGROUP BY {columns_sql}"

            foreign_key_check_sqls.append(check_sql)

        for column in columns:
            if not column in foreign_keys_column_names:
                append_standard_column(column)

        append_consts(consts)
        append_consts(insert_consts, insert_only=True)

        if foreign_keys:
            for i, foreign_key in enumerate(foreign_keys):
                append_foreign_key(foreign_key, f"fk{i+1}")

        # Assemble SQL statement
        merge_sql = "INSERT INTO "
        if dst_schema:    
            merge_sql += f"{self.escape_identifier(dst_schema)}."
        merge_sql += f"{self.escape_identifier(dst_table)}"
        merge_sql += f" ({insert_sql})"
        merge_sql += f"\nSELECT {select_sql}"
        merge_sql += f"\nFROM {from_sql}"
        if join_sql:
            merge_sql += f"\n{join_sql}"
        if key:
            merge_sql += f"\nON CONFLICT ({key_sql})"
            merge_sql += f"\nDO UPDATE SET {set_sql}"

        # Execute SQL statements
        with self.transaction():
            with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
                
                # Foreign key checks
                fk_missing = []
                for check_sql in foreign_key_check_sqls:
                    result = self.execute_query(check_sql, cursor=cursor)
                    if result:
                        tab = result.as_tab()
                        self._logger.error(f"{result.rowcount} foreign key{'s' if result.rowcount > 1 else ''} not found for {result.columns}" + f"\n{tab[0:1000]}{'…' if len(tab) > 1000 else ''}")
                        fk_missing.append(result.columns[1] if len(result.columns) == 1 else result.columns)

                if fk_missing:
                    raise ValueError(f"Foreign key missing for {', '.join(str(missing) for missing in fk_missing)}")
                
                # Merge statement
                cursor.execute(merge_sql)


    def get_load_auto_key(self,
                          model: str|tuple|type|list[Header],
                          *,
                          input_headers: list[str|Header]|str|Path = None, # headers or CSV file
                          convert_to_input = False,
                          default: str = 'append',
                          # For determining headers from `input_headers` if this is a file
                          encoding = 'utf-8',
                          delimiter: str = None,
                          quotechar = '"') -> tuple[str]|str:

        headers: list[Header]|None = None
        delimiter: str|None = None
        model = self.split_name(model) if isinstance(model, str) else model
        model_table_exists: bool = None
        model_columns_by_name: dict[str,Header] = None

        if input_headers:
            if isinstance(input_headers, (str,Path)):
                columns, delimiter = examine_csv_file(input_headers, encoding=encoding, delimiter=delimiter, quotechar=quotechar, force_delimiter=False)
                if columns:
                    headers = [Header(column) for column in columns]
                if not delimiter:
                    delimiter = get_default_csv_delimiter()
            else:
                headers = [header if isinstance(header, Header) else Header(header) for header in input_headers]

        if headers and any(header.name == 'id' for header in headers):
            key = ('id',)
        elif model:
            if isinstance(model, (str,tuple)): # This is actually a table                
                model_table_exists = self.table_exists(model)
            
            if model_table_exists is False:
                key = None
            else:
                model_columns_by_name = self._get_load_model_columns_by_name(model)
                key = self._select_load_auto_key(model_columns_by_name.values(), input_headers=headers, convert_to_input=convert_to_input)
        elif headers:
            key = self._select_load_auto_key(headers)
        else:
            key = None

        cache = self._TupleWithLoadCache(key) if key else self._StrWithLoadCache(default)
        cache._headers = headers
        cache._delimiter = delimiter
        cache._model = model
        cache._model_table_exists = model_table_exists
        cache._model_columns_by_name = model_columns_by_name
        return cache


    def _get_load_model_columns_by_name(self, model: str|tuple|type|list[Header]) -> dict[str,Header]:
        """
        - `model`: can be a Django model, the name (or tuple) of a table, or a list of columns.
        """
        if isinstance(model, list):
            by_name = {}
            for column in model:
                if not isinstance(column, Header):
                    column = Header(column)
                by_name[column.name] = column
            return by_name
        else:
            return {header.name: header for header in self.get_headers(model, typeonly=False)}


    def _select_load_auto_key(self, model: Iterable[Header], *, input_headers: Iterable[Header]|None = None, convert_to_input = False):
        input_header_names = set(header.name for header in input_headers) if input_headers else None

        def convert_to_input_columns(model_key: tuple[str]):
            if input_header_names is None:
                return model_key
            
            input_column_names = []

            for model_column_name in model_key:
                if model_column_name in input_header_names:
                    input_column_names.append(model_column_name)
                elif input_headers and model_column_name.endswith('_id'):
                    base = model_column_name[:-len('_id')]
                    if base in input_header_names:
                        input_column_names.append(base)
                    else:
                        found = False
                        for header in input_headers:
                            if header.name.startswith(f'{base}_'):
                                found = True
                                input_column_names.append(header.name)
                        if not found:
                            return None
                else:
                    return None
            
            return tuple(input_column_names)

        for column in model:
            if column.name == 'id':
                continue

            if column.unique:
                if column.unique is True:
                    keys = [(column.name,)]
                elif column.unique:
                    keys = column.unique

                for key in keys:
                    converted_key = convert_to_input_columns(key)
                    if converted_key:
                        return converted_key if convert_to_input else key
        
        return None
    

    def _get_load_foreign_keys(self, headers: Iterable[Header], target_model: type):
        from django.db.models import Field, ForeignKey

        from zut.django import get_field_python_type

        results: list[FK] = []

        field: Field
        for field in target_model._meta.fields:
            if isinstance(field, ForeignKey):
                prefix = f"{field.name}_"
                source_columns = [header.name for header in headers if header.name.startswith(prefix)]
                if source_columns:
                    results.append(FK(source_columns, field.related_model,
                                              related_pk=field.related_model._meta.pk.attname,
                                              related_pk_type=get_field_python_type(field.related_model._meta.pk),
                                              destination_column=field.attname))

        return results


    class _LoadCacheMixin:
        def __init__(self, *args, **kwargs):
            self._headers: list[Header]|None = None
            self._delimiter: str|None = None
            self._model: tuple|type|list[Header]|None = None
            self._model_table_exists: bool = None
            self._model_columns_by_name: dict[str,Header] = None

    class _TupleWithLoadCache(Tuple[str], _LoadCacheMixin):
        pass

    class _StrWithLoadCache(str, _LoadCacheMixin):
        pass

    #endregion


    #region Dump

    def dumper(self,               
               # DB-specific options
               table: str|tuple = None, *,
               add_autoincrement_pk: bool|str = False,
               batch: int|None = None,
               # Common TabularDumper options
               headers: Iterable[Header|Any]|None = None,
               append = False,
               archivate: bool|str|Path|None = None,
               title: str|bool|None = None,
               dst_name: str|bool = True,
               dir: str|Path|Literal[False]|None = None,
               delay: bool = False,
               defaults: dict[str,Any] = None,
               optional: str|Sequence[str]|Literal['*',True]|None = None,
               add_columns: bool|Literal['warn'] = False,
               no_tz: tzinfo|str|bool|None = None,
               # Destination mask values
               **kwargs) -> DbDumper[T_Connection, T_Cursor]:
        
        if no_tz is None:
            no_tz = self.tz

        extended_kwargs = {
                'headers': headers,
                'append': append,
                'archivate': archivate,
                'title': title,
                'dst_name': dst_name,
                'dir': dir,
                'delay': delay,
                'defaults': defaults,
                'optional': optional,
                'add_columns': add_columns,
                'no_tz': no_tz,
                **kwargs
            }

        return DbDumper(self,
                        table=table,
                        add_autoincrement_pk=add_autoincrement_pk,
                        batch=batch,
                        **extended_kwargs)
    
    #endregion


class FK:
    def __init__(self, source_columns: str|Iterable[str], related_table: str|tuple[str|None,str]|type, *, related_columns: str|Iterable[str] = None, related_pk: str = 'id', related_pk_type: type|None = None, destination_column: str = None):
        if isinstance(source_columns, str):
            self.source_columns = (source_columns,)
        else:
            self.source_columns = tuple(column for column in source_columns)

        if isinstance(related_table, tuple):
            self.related_schema, self.related_table = related_table
        elif isinstance(related_table, str):
            self.related_schema = None
            self.related_table = related_table
        elif isinstance(related_table, type):
            self.related_schema = None
            self.related_table = related_table._meta.db_table
        else:
            raise TypeError(f"related_table: {related_table}")
        
        source_prefix = self._find_source_prefix()

        if related_columns:
            if isinstance(related_columns, str):
                self.related_columns = (related_columns,)
            else:
                self.related_columns = tuple(column for column in related_columns)
            if len(self.related_columns) != len(self.source_columns):
                raise ValueError(f"{len(related_columns)} foreign_columns for {len(source_columns)} columns")
        else:
            self.related_columns = tuple(column[len(source_prefix):] for column in self.source_columns)            

        self.related_pk = related_pk
        self.related_pk_type = related_pk_type

        if destination_column:
            self.destination_column = destination_column
        elif source_prefix:
            self.destination_column = f'{source_prefix}{self.related_pk}'
        else:
            self.destination_column = f'{self.related_table}{self.related_pk}'


    def __repr__(self):
        return f"FK({', '.join(self.source_columns)}) -> {self.destination_column}: {f'{self.related_schema}.' if self.related_schema else ''}{self.related_table}({', '.join(self.related_columns)}) -> {self.related_pk}" + (f" ({self.related_pk_type.__name__})" if self.related_pk_type else "")


    def _find_source_prefix(self):        
        size = len(self.source_columns)

        # if size is 0, return empty string 
        if (size == 0):
            raise ValueError("Source columns cannot be empty")

        if (size == 1):
            foreign_table_prefix = f"{self.related_table}_"
            if self.source_columns[0].startswith(foreign_table_prefix): # e.g. source_column 'cluster_name', foreign table 'cluster'
                return foreign_table_prefix
            
            pos = self.related_table.rfind('_')
            if pos > 0:
                part_prefix = f"{self.related_table[pos+1:]}_"
                if self.source_columns[0].startswith(part_prefix): # e.g. source_column 'cluster_name', foreign table 'vmware_cluster':
                    return part_prefix

            return ''

        # sort the array of strings 
        values = sorted(self.source_columns)
        
        # find the minimum length from first and last string 
        end = min(len(values[0]), len(values[size - 1]))

        # find the common prefix between  the first and last string 
        i = 0
        while (i < end and values[0][i] == values[size - 1][i]):
            i += 1

        prefix = values[0][0: i]
        return prefix


class DbResult(ColumnsProvider, Generic[T_Connection, T_Cursor]):
    def __init__(self, db: Db[T_Connection, T_Cursor], cursor: T_Cursor, *, rows: list[tuple]|None, columns: tuple[str], query_id, tz: tzinfo|None):
        super().__init__()
        self._columns = columns if isinstance(columns, tuple) else tuple(columns)
        self.db = db
        self.cursor = cursor
        self._query_id = query_id
        self._tz = tz
        self._formatted_rows: list[Row] = []
        self._input_rows = rows
        self._input_rows_iterator = None
        self._input_rows_iteration_stopped = False

    def __iter__(self):       
        return self.Iterator(self)
        
    def __bool__(self):
        try:
            next(iter(self))
            return True
        except StopIteration:
            return False

    def _next_input_row(self):
        if self._input_rows_iterator is None:
            if self._input_rows is not None:
                self._input_rows_iterator = iter(self._input_rows)
            else:
                self._input_rows_iterator = iter(self.cursor)
        
        if self._input_rows_iteration_stopped:
            raise StopIteration()
    
        try:
            values = next(self._input_rows_iterator)
        except StopIteration:
            self._input_rows_iterator_stopped = True
            raise

        return values

    def _format_input_row(self, row):
        if self._tz:
            tz = self._tz if self._tz == 'localtime' else parse_tz(self._tz)
        else:
            tz = self.db.tz

        if tz:
            for i, value in enumerate(row):
                if isinstance(value, (datetime,time)):
                    if not is_aware(value):
                        row[i] = make_aware(value, tz)
        return row
    
    @property
    def rowcount(self) -> int|None:
        value = self.cursor.rowcount
        return None if value == -1 else value
    
    @property
    def lastrowid(self):
        if self.db.scheme == 'postgresql':
            self.cursor.execute("SELECT lastval()")
            return next(iter(self.cursor))[0]
        elif self.db.scheme == 'sqlserver':
            self.cursor.execute("SELECT @@IDENTITY")
            return next(iter(self.cursor))[0]
        
        return self.cursor.lastrowid
    
    def single(self):
        iterator = iter(self)
        try:
            row = next(iterator)
        except StopIteration:
            row = None
            
        if row is None:
            raise NotFoundError()

        try:
            next(iterator)
            raise SeveralFoundError()
        except StopIteration:
            pass

        return row
    
    def as_dicts(self):
        """
        Return results as a list of row dictionnaries.
        """
        return [row.as_dict() for row in iter(self)]
    
    def as_tab(self):
        dst = StringIO()        
        self.to_dumper(TabDumper(dst))
        return dst.getvalue()
    
    def tab(self):
        self.to_dumper('tab')
    
    def to_dumper(self, dumper: TabularDumper|IOBase|str|Path, close=True, **kwargs):
        """
        Send results to the given tabular dumper.
        
        If dumper is `tab`, `csv`, a stream or a str/path, create the appropriate Tab/CSV/Excel dumper.
        
        Return a tuple containing the list of columns and the number of exported rows.
        """
        if isinstance(dumper, TabularDumper):
            if dumper.headers is not None:
                if [header.name for header in dumper.headers] != self.columns:
                    raise ValueError("Invalid headers in given dumper")
            else:
                dumper.headers = self.headers
        else:
            dumper = tabular_dumper(dumper, headers=self.headers, **kwargs)

        try:
            for row in iter(self):
                dumper.append(row.values)        
            return self.columns, dumper.count
        finally:
            if close:
                dumper.close()
    
    class Iterator:
        def __init__(self, dbresults: DbResult[T_Connection, T_Cursor]):
            self.dbresults = dbresults
            self.next_index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.next_index < len(self.dbresults._formatted_rows):
                formatted_row = self.dbresults._formatted_rows[self.next_index]
            else:
                input_row = self.dbresults._next_input_row()
                formatted_values = self.dbresults._format_input_row(input_row)
                formatted_row = Row(self.dbresults, formatted_values, skip_convert=True) # ColumnProvider's headers are just columns without any parameter, so there is nothing to convert
                self.dbresults._formatted_rows.append(formatted_row)
            
            self.next_index += 1
            return formatted_row


class DbDumper(TabularDumper[Db[T_Connection, T_Cursor]]):
    """ 
    Line-per-line INSERT commands (to be used when `InsertSqlDumper` is not available).
    """
    def __init__(self, origin: Db[T_Connection, T_Cursor]|T_Connection|str, *,
                 table: str|tuple|None = None,
                 add_autoincrement_pk: bool|str = False,
                 batch: int|None = None,
                 **kwargs):
        
        if isinstance(origin, Db):
            dst = origin
            self._close_dst = False
        else:
            dst = get_db(origin, autocommit=False)
            self._close_dst = True
        
        if table:
            self._schema, self._table = dst.split_name(table)
        elif dst.table:
            self._schema, self._table = dst.schema, dst.table
        else:
            raise ValueError("Table name not provided")

        dst_name = kwargs.pop('dst_name', None)
        if not dst_name:
            dst_name = f"{self._schema + '.' if self._schema else ''}{self._table}"

        super().__init__(dst, dst_name=dst_name, **kwargs)

        self._add_autoincrement_pk = 'id' if add_autoincrement_pk is True else add_autoincrement_pk
        self._insert_sql_headers: list[Header] = []
        self._insert_sql_single: str = None
        self._insert_sql_batch: str = None
        if self.dst.scheme == 'sqlite':
            self._max_params = 999
        elif self.dst.scheme == 'sqlserver':
            self._max_params = 2100
        else:
            self._max_params = 65535 # postgresql limit
        self.batch = batch

        self._cursor = None
        self._batch_rows = []
        self._executed_batch_count = 0

        self._insert_schema = self._schema
        self._insert_table = self._table

    @property
    def cursor(self):
        """
        Reused cursor (only for inserting data).
        """
        if self._cursor is None:
            self._cursor = self.dst.connection.cursor()
        return self._cursor

    def close(self, *final_queries):
        """
        Export remaining rows, execute optional final SQL queries, and then close the dumper.
        """
        super().close()

        self.flush(*final_queries)

        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None
        
        if self._close_dst:
            if not self.dst.autocommit:
                self.dst.connection.commit()
            self.dst.close()

    def _build_insert_sqls(self, additional_headers: list[Header]):
        self._insert_sql_headers += additional_headers

        into_sql = f""
        if self._insert_schema:
            into_sql += f"{self.dst.escape_identifier(self._insert_schema)}."
        into_sql += self.dst.escape_identifier(self._insert_table)

        into_sql += "("
        values_sql = "("
        need_comma = False
        for header in self._insert_sql_headers:
            if need_comma:
                into_sql += ","
                values_sql += ","
            else:
                need_comma = True
            into_sql += f"{self.dst.escape_identifier(header.name)}"
            values_sql += self.dst.sql_placeholder
        into_sql += ")"
        values_sql += ")"

        max_batch = int(self._max_params / len(self._insert_sql_headers))
        if self.batch is None or max_batch < self.batch:
            self.batch = max_batch

        self._insert_sql_single = f"INSERT INTO {into_sql} VALUES {values_sql}"
        self._insert_sql_batch = f"INSERT INTO {into_sql} VALUES "
        for i in range(self.batch):
            self._insert_sql_batch += (',' if i > 0 else '') + values_sql

    def open(self) -> list[Header]|None:
        # Called at first exported row, before headers are analyzed.
        # Return list of existing headers if table exists, None if not.
        if self.dst.table_exists((self._schema, self._table)):
            if not self.append_to_existing:
                self.dst.truncate_table((self._schema, self._table))
            
            headers = [header for header in self.dst.get_headers((self._schema, self._table)) if not header.identity]
            self._build_insert_sqls(headers)
            return headers
        else:
            return None
    
    def export_headers(self, headers: list[Header]):
        # Called at first exported row, if there are no pre-existing headers (= table does not exist) => create table
        columns = [header for header in headers]
        
        if self._add_autoincrement_pk and not any(header.name == self._add_autoincrement_pk for header in headers):
            columns.insert(0, Header(name=self._add_autoincrement_pk, type=int, primary_key=True, identity=True))

        self.dst.create_table((self._schema, self._table), columns)

        self._build_insert_sqls(headers)

    def new_headers(self, headers: list[Header]) -> bool|None:
        self.dst.add_table_columns((self._schema, self._table), headers)
        self._build_insert_sqls(headers)
        return True

    def _prepare_and_export_row(self, row: Iterable|dict):
        if not self.headers:
            raise ValueError(f"Cannot dump to db without headers")
        return super()._prepare_and_export_row(row)

    def _convert_value(self, value: Any):
        value = super()._convert_value(value)
        value = self.dst.convert_value(value)
        return value

    def export(self, row: list):
        self._batch_rows.append(row)
        if len(self._batch_rows) >= self.batch:
            self._export_batch()

    def _export_batch(self):
        kwargs = {}
        if self.dst.scheme == 'postgresql':
            kwargs['prepare'] = True
            
        inlined_row = []
        while len(self._batch_rows) / self.batch >= 1:
            for row in self._batch_rows[:self.batch]:
                inlined_row += row
                
            if self._logger.isEnabledFor(logging.DEBUG):
                t0 = time_ns()
                if self._executed_batch_count == 0:
                    self._d_total = 0
            
            self.cursor.execute(self._insert_sql_batch, inlined_row, **kwargs)
            self._executed_batch_count += 1

            if self._logger.isEnabledFor(logging.DEBUG):
                t = time_ns()
                d = t - t0
                self._d_total += d
                self._logger.debug(f"Batch {self._executed_batch_count}: {self.batch:,} rows inserted in {d/1e6:,.1f} ms (avg: {self._d_total/1e3/(self._executed_batch_count * self.batch):,.1f} ms/krow, inst: {d/1e3/self.batch:,.1f} ms/krow)")
            
            self._batch_rows = self._batch_rows[self.batch:]

    def flush(self, *final_queries):
        """
        Export remaining rows, and then execute optional final SQL queries.
        """
        super().flush()

        kwargs = {}
        if self.dst.scheme == 'postgresql':
            kwargs['prepare'] = True
        
        self._export_batch()

        if self._batch_rows:
            if self._logger.isEnabledFor(logging.DEBUG):
                t0 = time_ns()

            for row in self._batch_rows:
                while len(row) < len(self._insert_sql_headers):
                    row.append(None)
                self.cursor.execute(self._insert_sql_single, row, **kwargs)
                            
            if self._logger.isEnabledFor(logging.DEBUG):
                d = time_ns() - t0
                self._logger.debug(f"Remaining: {len(self._batch_rows):,} rows inserted one by one in {d/1e6:,.1f} ms ({d/1e3/(len(self._batch_rows)):,.1f} ms/krow)")

            self._batch_rows.clear()

        for final_query in final_queries:
            self.dst.execute_query(final_query)


def _get_connection_from_wrapper(db):    
    if type(db).__module__.startswith(('django.db.backends.', 'django.utils.connection')):
        return db.connection
    elif type(db).__module__.startswith(('psycopg_pool.pool',)):
        return db.connection()
    elif type(db).__module__.startswith(('psycopg2.pool',)):
        return db.getconn()
    else:
        return db


def get_db(origin, *, autocommit=True) -> Db:
    """
    Create a new Db instance (if origin is not already one).
    - `autocommit`: commit transactions automatically (applies only for connections created by the Db instance).
    """
    from zut.db.mariadb import MariaDb
    from zut.db.postgresql import PostgreSql
    from zut.db.postgresqlold import PostgreSqlOld
    from zut.db.sqlite import Sqlite
    from zut.db.sqlserver import SqlServer

    if isinstance(origin, str):
        db_cls = get_db_class_from_url(origin)
        if db_cls is None:
            raise ValueError(f"Invalid db url: {origin}")
        return db_cls(origin, autocommit=autocommit)
    
    elif isinstance(origin, dict) and 'ENGINE' in origin: # Django
        engine = origin['ENGINE']
        if engine in {"django.db.backends.postgresql", "django.contrib.gis.db.backends.postgis"}:
            if not PostgreSql.missing_dependency:
                return PostgreSql(origin, autocommit=autocommit)
            elif not PostgreSqlOld.missing_dependency:
                return PostgreSqlOld(origin, autocommit=autocommit)
            else:
                raise ValueError(f"PostgreSql and PostgreSqlOld not available (psycopg missing)")
        elif engine in {"django.db.backends.mysql", "django.contrib.gis.db.backends.mysql"}:
            return MariaDb(origin, autocommit=autocommit)
        elif engine in {"django.db.backends.sqlite3", "django.db.backends.spatialite"}:
            return Sqlite(origin, autocommit=autocommit)
        elif engine in {"mssql"}:
            return SqlServer(origin, autocommit=autocommit)
        else:
            raise ValueError(f"Invalid db: unsupported django db engine: {engine}")
        
    elif isinstance(origin, Db):
        return origin
    
    else:
        db_cls = get_db_class_from_connection(origin)
        if db_cls is None:
            raise ValueError(f"Invalid db: unsupported origin type: {type(origin)}")
        return db_cls(origin)
    

def get_db_class_from_url(url: str) -> type[Db]|None:
    from zut.db.mariadb import MariaDb
    from zut.db.postgresql import PostgreSql
    from zut.db.postgresqlold import PostgreSqlOld
    from zut.db.sqlite import Sqlite
    from zut.db.sqlserver import SqlServer

    if not isinstance(url, str):
        return None

    r = urlparse(url)
    if r.scheme in {'postgresql', 'postgres', 'pg'}:
        if not PostgreSql.missing_dependency:
            db_cls = PostgreSql
        elif not PostgreSqlOld.missing_dependency:
            db_cls = PostgreSqlOld
        else:
            raise ValueError(f"PostgreSql and PostgreSqlOld not available (psycopg missing)")
    elif r.scheme in {'mariadb', 'mysql'}:
        db_cls = MariaDb
    elif r.scheme in {'sqlite', 'sqlite3'}:
        db_cls = Sqlite
    elif r.scheme in {'sqlserver', 'sqlservers', 'mssql', 'mssqls'}:
        db_cls = SqlServer
    else:
        return None
    
    if db_cls.missing_dependency:
        raise ValueError(f"Cannot use db {r.scheme} (missing {db_cls.missing_dependency} dependency)")
    
    return db_cls


def get_db_class_from_connection(connection) -> type[Db]|None:
    from zut.db.mariadb import MariaDb
    from zut.db.postgresql import PostgreSql
    from zut.db.postgresqlold import PostgreSqlOld
    from zut.db.sqlite import Sqlite
    from zut.db.sqlserver import SqlServer

    connection = _get_connection_from_wrapper(connection)

    type_fullname: str = type(connection).__module__ + '.' + type(connection).__qualname__
    if type_fullname == 'psycopg2.extension.connection':
        db_cls = PostgreSqlOld
    elif type_fullname == 'psycopg.Connection':
        db_cls = PostgreSql
    elif type_fullname == 'MySQLdb.connections.Connection':
        db_cls = MariaDb
    elif type_fullname == 'sqlite3.Connection':
        db_cls = Sqlite
    elif type_fullname == 'pyodbc.Connection':
        db_cls = SqlServer
    else:
        return None
    
    if db_cls.missing_dependency:
        raise ValueError(f"Cannot use db (missing {db_cls.missing_dependency} dependency)")
    
    return db_cls
