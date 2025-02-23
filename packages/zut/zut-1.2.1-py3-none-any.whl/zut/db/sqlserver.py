from __future__ import annotations

import logging
import re
from typing import Any, Generator, TYPE_CHECKING
from urllib.parse import unquote, urlparse

from zut import Header, build_url
from zut.db import Db

if TYPE_CHECKING:
    from pyodbc import Connection, Cursor

try:
    from pyodbc import connect, drivers
    _missing_dependency = None
except ImportError:
    _missing_dependency = "pyodbc"


class SqlServer(Db[Connection, Cursor] if TYPE_CHECKING else Db):
    """
    Database adapter for Microsoft SQL Server (using `pyodbc` driver).
    """
    scheme = 'sqlserver' # or sqlservers (if encrypted)
    default_port = 1433
    default_schema = 'dbo'
    identifier_quotechar_begin = '['
    identifier_quotechar_end = ']'
    sql_placeholder = '?'
    sql_named_placeholder = ':%s'
    only_positional_params = True
    split_multi_statement_files = True
    identity_definition_sql = 'IDENTITY'
    bool_sql_type = 'bit'
    datetime_sql_type = 'datetime'
    accept_aware_datetime = False
    procedure_caller = 'EXEC'
    procedure_params_parenthesis = False
    can_cascade_truncate = False
    can_add_several_columns = True
    function_requires_schema = True
    temporary_prefix = '#'
    missing_dependency = _missing_dependency

    def create_connection(self, *, autocommit: bool|None, **kwargs):
        def escape(s):
            if ';' in s or '{' in s or '}' in s or '=' in s:
                return "{" + s.replace('}', '}}') + "}"
            else:
                return s
            
        r = urlparse(self._connection_url)
        
        server = unquote(r.hostname) or '(local)'
        if r.port:
            server += f',{r.port}'

        # Use "ODBC Driver XX for SQL Server" if available ("SQL Server" seems not to work with LocalDB, and takes several seconds to establish connection on my standard Windows machine with SQL Server Developer).
        driver = "SQL Server"
        for a_driver in sorted(drivers(), reverse=True):
            if re.match(r'^ODBC Driver \d+ for SQL Server$', a_driver):
                driver = a_driver
                break

        connection_string = 'Driver={%s};Server=%s;Database=%s;' % (escape(driver), escape(server), escape(r.path.lstrip('/')))

        if r.username:
            connection_string += 'UID=%s;' % escape(unquote(r.username))
            if r.password:
                connection_string += 'PWD=%s;' % escape(unquote(r.password))
        else:
            connection_string += 'Trusted_Connection=yes;'
            
        connection_string += f"Encrypt={'yes' if r.scheme in {'mssqls', 'sqlservers'} else 'no'};"
        return connect(connection_string, autocommit=autocommit, **kwargs)


    def _get_url_from_connection(self):
        with self.cursor(autoclose=False) as cursor:
            cursor.execute("SELECT @@SERVERNAME, local_tcp_port, SUSER_NAME(), DB_NAME() FROM sys.dm_exec_connections WHERE session_id = @@spid")
            host, port, user, dbname = next(iter(cursor))
        return build_url(scheme=self.scheme, username=user, hostname=host, port=port, path='/'+dbname)


    def _paginate_parsed_query(self, selectpart: str, orderpart: str, *, limit: int|None, offset: int|None) -> str:
        if orderpart:
            result = f"{selectpart} {orderpart} OFFSET {offset or 0} ROWS"
            if limit is not None:
                result += f" FETCH NEXT {limit} ROWS ONLY"
            return result
        elif limit is not None:
            if offset is not None:
                raise ValueError("an ORDER BY clause is required for OFFSET")
            return f"SELECT TOP {limit} * FROM ({selectpart}) s"
        else:
            return selectpart


    def _log_cursor_notices(self, cursor):
        if cursor.messages:                        
            for nature, message in cursor.messages:
                level, message = sqlserver_parse_notice(nature, message)
                self._logger.log(level, message)


    def _traverse_cursor(self, cursor: Cursor, *, warn: bool, query_id):
        columns = []
        rows = []
        set_num = 1

        while True:
            if cursor.description:
                columns = [info[0] for info in cursor.description]

                if warn:
                    set_id = f'{query_id} (set {set_num})' if query_id is not None else f'(set {set_num})'
                    self._warn_if_rows(cursor, columns=columns, query_id=set_id)
                    rows = [] # indicates to QueryResults to not report rows that we just warned about

                else:
                    rows = [row for row in iter(cursor)]

            else:
                columns = []
                rows = []

            if not cursor.nextset():
                break

            set_num += 1
            self._log_cursor_notices(cursor)

        # Return rows and columns from the last result set
        return rows, columns


    def table_exists(self, table: str|tuple = None, *, cursor = None) -> bool:
        schema, table = self.split_name(table)

        sql = "SELECT CASE WHEN EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = ? AND table_name = ?) THEN 1 ELSE 0 END"
        params = [schema or self.default_schema, table]

        return self.get_scalar(sql, params, cursor=cursor) == 1
    
    
    def schema_exists(self, schema: str = None, *, cursor = None) -> bool:
        if not schema:
            schema = self.schema or self.default_schema

        query = "SELECT CASE WHEN EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = ?) THEN 1 ELSE 0 END"
        return self.get_scalar(query, [schema], cursor=cursor) == 1


    def _get_table_columns(self, table, *, cursor, typeonly: bool) -> Generator[dict,Any,Any]|list[Header|dict]|tuple[list[dict],list[dict]]:
        schema, table = self.split_name(table)

        if table.startswith('#'):
            table = self.get_scalar("(SELECT name FROM tempdb.sys.objects WHERE object_id = OBJECT_ID('tempdb.dbo.' + ?))", [table], cursor=cursor)
            syschema_prefix = 'tempdb.'
        else:
            syschema_prefix = ''

        columns = self.execute_query(f"""
SELECT
    c.column_name AS name
    ,CAST(CASE WHEN c.is_nullable = 'YES' THEN 1 ELSE 0 END AS bit) AS "null"
    ,c.data_type AS sql_type
    ,CASE 
	    WHEN c.character_maximum_length IS NOT NULL AND c.character_maximum_length != -1 AND c.data_type NOT IN ('text', 'ntext') THEN c.character_maximum_length
	    WHEN c.numeric_precision IS NOT NULL AND c.data_type IN ('decimal', 'numeric') THEN c.numeric_precision
	    WHEN c.datetime_precision IS NOT NULL AND c.data_type IN ('datetime2', 'time') THEN c.datetime_precision
    END AS sql_precision
    ,CASE
        WHEN c.numeric_scale IS NOT NULL AND c.data_type IN ('decimal', 'numeric') THEN c.numeric_scale
    END AS sql_scale
    ,CASE WHEN c.collation_name IS NOT NULL THEN concat(' COLLATE ', c.collation_name) ELSE '' END AS sql_suffix
FROM {syschema_prefix}information_schema.columns c
WHERE c.table_schema = :schema AND c.table_name = :table
ORDER BY c.ordinal_position
""", {'schema': schema or self.default_schema, 'table': table}, cursor=cursor).as_dicts()

        if typeonly:
            return columns
        
        indexes = self.execute_query(f"""
WITH index_details AS (
	SELECT
		i.name AS [index]
		,c.name AS [column]
		,ic.key_ordinal AS column_order_in_index
		,ic.column_id AS column_order_in_table
		,i.is_unique AS [unique]
		,i.is_primary_key AS [primary_key]
		,c.is_identity AS [identity]
	FROM {syschema_prefix}sys.indexes i
	INNER JOIN {syschema_prefix}sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
	INNER JOIN {syschema_prefix}sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id  
	WHERE {'i.object_id = OBJECT_ID(:table)' if syschema_prefix else 'OBJECT_SCHEMA_NAME(i.object_id) = :schema AND OBJECT_NAME(i.object_id) = :table'}
)
,index_columns AS (
	SELECT
		[index]
		,string_agg([column], ',') WITHIN GROUP (ORDER BY column_order_in_index) AS [columns]
	FROM index_details
	GROUP BY
		[index]
)
,index_order AS (
	SELECT
		[index]
		,string_agg(RIGHT('000'+CAST(column_order_in_table AS VARCHAR(3)),3), ',') WITHIN GROUP (ORDER BY column_order_in_table) AS [index_order]
	FROM index_details
	GROUP BY
		[index]
)
SELECT
	i.[index]
	,ic.[columns]
	,io.[index_order]
	,i.[unique]
	,i.[primary_key]
	,i.[identity]
FROM (
	SELECT
		i.[index]
		,i.[unique]
		,i.[primary_key]
		,i.[identity]
	FROM index_details i
	GROUP BY
		i.[index]
		,i.[unique]
		,i.[primary_key]
		,i.[identity]
) i
INNER JOIN index_columns ic ON ic.[index] = i.[index]
INNER JOIN index_order io ON io.[index] = i.[index]
ORDER BY index_order
""", {'schema': schema or self.default_schema, 'table': f'tempdb..{table}' if syschema_prefix else table}, cursor=cursor).as_dicts()

        return columns, indexes


def sqlserver_parse_notice(nature: str, message: str) -> tuple[int, str]:
    m = re.match(r"^\[Microsoft\]\[[\w\d ]+\]\[SQL Server\](.+)$", message)
    if m:
        message = m[1]

    if nature == '[01000] (0)':
        nature = 'PRINT'
    elif nature == '[01000] (50000)':
        nature = 'RAISERROR'
    elif nature == '[01003] (8153)': # Avertissement : la valeur NULL est éliminée par un agrégat ou par une autre opération SET
        return logging.INFO, message
    
    m = re.match(r'^\[?(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s?[\]\:](?P<message>.+)$', message, re.DOTALL|re.IGNORECASE)
    if m:
        return getattr(logging, m['level']), m['message'].lstrip()
    
    if nature == 'PRINT':
        return logging.INFO, message
    else:
        return logging.WARNING, message
