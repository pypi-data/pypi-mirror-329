from __future__ import annotations

import csv
import logging
from random import randint
import re
from contextlib import nullcontext
from io import IOBase, StringIO
from pathlib import Path
from typing import Any, Generator, TYPE_CHECKING, Iterable
from urllib.parse import ParseResult

from zut import Header, build_url, examine_csv_file, get_default_decimal_separator, skip_utf8_bom, get_logger
from zut.db import Db

if TYPE_CHECKING:
    from psycopg import Connection, Cursor

try:
    from psycopg import connect
    from psycopg.errors import Diagnostic
    _missing_dependency = None
except ImportError:
    _missing_dependency = "psycopg"


class PostgreSql(Db[Connection, Cursor] if TYPE_CHECKING else Db):
    """
    Database adapter for PostgreSQL (using `psycopg` (v3) driver).

    This is also the base class for :class:`PostgreSqlOldAdapter` (using `psycopg2` (v2) driver).
    """
    scheme = 'postgresql'
    default_port = 5432
    missing_dependency = _missing_dependency
    

    def _verify_scheme(self, r: ParseResult) -> ParseResult|None:
        # See: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
        if r.scheme == 'postgresql':
            return r
        elif r.scheme in {'pg', 'postgres'}:
            return r._replace(scheme='postgresql')
        else:
            return None

    
    def _register_notice_handler(self, cursor, query_id = None):
        if query_id is not None:
            logger = get_logger(self._logger.name + f':{query_id}')
        else:
            logger = self._logger
        
        return PostgreSqlNoticeManager(cursor.connection, logger)
    

    def create_connection(self, *, autocommit: bool, **kwargs):
        return connect(self._connection_url, autocommit=autocommit, **kwargs)
    
    def transaction(self):
        return self.connection.transaction()
    
    def _get_url_from_connection(self):
        with self.cursor(autoclose=False) as cursor:
            cursor.execute("SELECT session_user, inet_server_addr(), inet_server_port(), current_database()")
            user, host, port, dbname = next(iter(cursor))
        return build_url(scheme=self.scheme, username=user, hostname=host, port=port, path='/'+dbname)
    

    def table_exists(self, table: str|tuple = None, *, cursor = None) -> bool:
        schema, table = self.split_name(table)

        query = "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = %s AND tablename = %s)"
        return self.get_scalar(query, [schema or self.default_schema, table], cursor=cursor)
    
    
    def schema_exists(self, schema: str = None, *, cursor: Cursor = None) -> bool:
        if not schema:
            schema = self.schema or self.default_schema

        query = "SELECT EXISTS (SELECT FROM pg_namespace WHERE nspname = %s)"
        return self.get_scalar(query, [schema], cursor=cursor)


    def _get_table_columns(self, table, *, cursor, typeonly: bool) -> Generator[dict,Any,Any]|list[Header|dict]|tuple[list[dict],list[dict]]:
        schema, table = self.split_name(table)

        if schema == 'pg_temp':
            schema_sql = "LIKE 'pg_temp%%'"
            params = []
        else:
            schema_sql = "= %s"
            params = [schema or self.default_schema]
        params.append(table)

        columns = self.execute_query(f"""
SELECT
    c.column_name AS name
    ,c.is_nullable = 'YES' AS "null"
    ,CASE
    	WHEN c.data_type = 'ARRAY' THEN (CASE WHEN c.udt_name SIMILAR TO '_%%' THEN substring(c.udt_name, 2, 1000) ELSE c.udt_name END || '[]')
    	ELSE c.udt_name
    END AS sql_type
    ,CASE
		WHEN c.character_maximum_length IS NOT NULL THEN c.character_maximum_length
	    WHEN c.numeric_precision IS NOT NULL AND c.data_type = 'numeric' THEN c.numeric_precision
	    WHEN c.datetime_precision IS NOT NULL AND c.datetime_precision != 6 THEN c.datetime_precision		
	END AS sql_precision
    ,CASE
	    WHEN c.numeric_scale IS NOT NULL AND c.data_type = 'numeric' THEN c.numeric_scale
	END AS sql_scale
    ,c.is_identity = 'YES' AS "identity"
    ,CASE
    	WHEN c.column_default = 'statement_timestamp()' THEN 'CURRENT_TIMESTAMP'
    	WHEN regexp_match(c.column_default, '''(.+)''::[0-9a-z ]+') IS NOT NULL THEN replace((regexp_match(c.column_default, '''(.+)''::[0-9a-z ]+'))[1], '''''', '''') -- Extract value from "'value'::type"
    	ELSE c.column_default
    END AS "default"
FROM information_schema.tables t
INNER JOIN information_schema.columns c ON c.table_schema = t.table_schema AND c.table_name = t.table_name
WHERE t.table_schema {schema_sql}
AND t.table_name = %s
ORDER BY c.ordinal_position
""", params, cursor=cursor).as_dicts()
        
        if typeonly:
            return columns
        
        indexes = self.execute_query(f"""
SELECT
	"columns"
	,"unique"
	,"primary_key"
FROM (
	SELECT
		"index"
		,array_agg("column" ORDER BY column_order_in_index) AS "columns"
		,array_agg(column_order_in_table ORDER BY column_order_in_table) AS index_order
		,"unique"
		,"primary_key"
	FROM (
		SELECT
			idx.indexrelid AS "index"
		    ,k.i AS column_order_in_index
		    ,att.attnum AS column_order_in_table
		    ,att.attname AS "column"
		    ,idx.indisunique AS "unique"
		    ,idx.indisprimary AS "primary_key"
		FROM pg_index idx
		INNER JOIN pg_class tbl ON tbl.oid = idx.indrelid
		INNER JOIN pg_namespace sch ON sch.oid = tbl.relnamespace
		CROSS JOIN LATERAL unnest(idx.indkey) WITH ORDINALITY AS k(attnum, i)
		INNER JOIN pg_attribute AS att ON att.attrelid = idx.indrelid AND att.attnum = k.attnum
		WHERE sch.nspname {schema_sql} AND tbl.relname = %s
	) s
	GROUP BY
		"index"
		,"unique"
		,"primary_key"
) s
ORDER BY index_order
""", params, cursor=cursor).as_dicts()
        
        return columns, indexes
    

    def copy_from_csv(self,
                    csv_file: Path|str|IOBase,
                    table: str|tuple = None,
                    headers: list[Header|str] = None,
                    *,
                    buffer_size = 65536,
                    cursor: Cursor = None,
                    # CSV format
                    encoding = 'utf-8',
                    delimiter: str = None,
                    quotechar = '"',
                    nullval: str = None,
                    no_headers: bool = None) -> int:
        
        # Prepare table argument
        if not table:
            if not self.table:
                raise ValueError("No table given")
            table = self.table
        schema, table = self.split_name(table)
            
        # Determine CSV and headers parameters
        if not delimiter or (not headers and not no_headers):
            examined_columns, examined_delimiter, _ = examine_csv_file(csv_file, encoding=encoding, delimiter=delimiter, quotechar=quotechar, force_delimiter=False)
            if not delimiter:
                delimiter = examined_delimiter or get_default_decimal_separator()
            if not headers and not no_headers:
                headers = examined_columns

        if headers:
            headers = [header if isinstance(header, Header) else Header(header) for header in headers]

        # Prepare SQL statement                        
        sql = "COPY "        
        if schema:    
            sql += f"{self.escape_identifier(schema)}."
        sql += f"{self.escape_identifier(table)}"

        if headers:
            sql += " ("
            for i, header in enumerate(headers):
                sql += (", " if i > 0 else "") + self.escape_identifier(header.name)
            sql += ")"
            
        sql += f" FROM STDIN (FORMAT csv, ENCODING {self.escape_literal('utf-8' if encoding == 'utf-8-sig' else encoding)}, DELIMITER {self.escape_literal(delimiter)}, QUOTE {self.escape_literal(quotechar)}, ESCAPE {self.escape_literal(quotechar)}"
        if nullval is not None:
            sql += f", NULL {self.escape_literal(nullval)}"
        if not no_headers:
            sql += ", HEADER match"
        sql += ")"
        
        # Execute SQL statement
        with nullcontext(csv_file) if isinstance(csv_file, IOBase) else open(csv_file, "rb") as fp:
            skip_utf8_bom(fp)
            
            with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
                self._actual_copy_from_csv(cursor, sql, fp, buffer_size)

                return cursor.rowcount
            

    def _actual_copy_from_csv(self, cursor: Cursor, sql: str, fp: IOBase, buffer_size: int):
        with cursor.copy(sql) as copy:
            while True:
                data = fp.read(buffer_size)
                if not data:
                    break
                copy.write(data)


    def disable_missing_ids(self, table: str|tuple|type, actual_ids: Iterable[int], *, disabled_column_name = 'disabled'):
        target_schema, target_table = self.split_name(table)
        tmp_table = self.get_temp_table_name('disable')

        # Create the temporary table
        with self.cursor() as cursor:
            cursor.execute(f"CREATE TEMPORARY TABLE {tmp_table} (id bigint NOT NULL PRIMARY KEY)")

        # Prepare an in-memory CSV file with the list of ids to disable
        with StringIO(newline='') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(['id'])
            for id in actual_ids:
                if hasattr(id, '_meta'): # Django model
                    id = id.pk
                writer.writerow([id])
        
            # Load the memory file in the database using postgresql's COPY
            self.copy_from_csv(fp, tmp_table, ['id'], delimiter=',')

        # Mark missing in target table as disabled
        with self.cursor() as cursor:
            sql =f"""
            UPDATE {self.escape_identifier(target_schema or 'public')}.{self.escape_identifier(target_table)}
            SET {self.escape_identifier(disabled_column_name)} = true
            WHERE id NOT IN (SELECT id FROM {tmp_table})
            """
            cursor.execute(sql)
            return cursor.rowcount


    def enforce_id_seq_offset(self, app_label: str|None = None, *, min_offset: int|None = None, max_offset: int|None = None):
        """
        Ensure the given model (or all models if none is given) have sequence starting with a minimal value.
        This leaves space for custom, programmatically defined values.

        Unless `min_offset` and `max_offset` are specified, the minimal value is randomly chosen between 65537 (after
        max uint16 value) and 262144 (max uint18 value).

        Compatible with postgresql only.
        """
        if min_offset is None and max_offset is None:
            min_offset = 65537
            max_offset = 262144
        elif max_offset is None:
            max_offset = min_offset
        elif min_offset is None:
            min_offset = min(65537, max_offset)

        sql = f"""
    SELECT
        s.schema_name
        ,s.table_name
        ,s.column_names
        ,s.sequence_name
        ,q.seqstart AS sequence_start
    FROM (
        -- List all PKs with their associated sequence name (or NULL if this is not a serial or identity column)
        SELECT
            n.nspname AS schema_name
            ,c.relnamespace AS schema_oid
            ,c.relname AS table_name
            ,array_agg(a.attname) AS column_names
            ,substring(pg_get_serial_sequence(n.nspname || '.' || c.relname, a.attname), length(n.nspname || '.') + 1) AS sequence_name
        FROM pg_index i
        INNER JOIN pg_class c ON c.oid = i.indrelid
        INNER JOIN pg_namespace n ON n.oid = c.relnamespace
        INNER JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = any(i.indkey)
        WHERE i.indisprimary
        GROUP BY
            n.nspname
            ,c.relnamespace
            ,c.relname
            ,substring(pg_get_serial_sequence(n.nspname || '.' || c.relname, a.attname), length(n.nspname || '.') + 1)
    ) s
    LEFT OUTER JOIN pg_class c ON c.relnamespace = s.schema_oid AND c.relname = s.sequence_name
    LEFT OUTER JOIN pg_sequence q ON q.seqrelid = c.oid
    WHERE s.schema_name = 'public' AND s.table_name {"LIKE %s" if app_label else "IS NOT NULL"} AND q.seqstart = 1
    ORDER BY schema_name, table_name, column_names
    """
        params = [f'{app_label}_%'] if app_label else None

        seqs = []
        with self.cursor() as cursor:
            for row in cursor.execute(sql, params):
                seqs.append({'schema': row[0], 'table': row[1], 'column': row[2][0], 'name': row[3]})

        with self.cursor() as cursor:
            for seq in seqs:
                sql = f"SELECT MAX({self.escape_identifier(seq['column'])}) FROM {self.escape_identifier(seq['schema'])}.{self.escape_identifier(seq['table'])}"
                cursor.execute(sql)
                max_id = cursor.fetchone()[0] or 0
                
                start_value = max(max_id + 1, randint(min_offset, max_offset))
                self._logger.debug("Set start value of %s to %s", seq['name'], start_value)
                sql = f"ALTER SEQUENCE {self.escape_identifier(seq['name'])} START WITH {start_value} RESTART WITH {start_value}"
                cursor.execute(sql)


class PostgreSqlNoticeManager:
    """
    This class can be used as a context manager that remove the handler on exit.

    The actual handler required by psycopg 3 `connection.add_notice_handler()` is the `postgresql_notice_handler` method.
    """
    def __init__(self, connection: Connection, logger: logging):
        self.connection = connection
        self.logger = logger
        for handler in list(self.connection._notice_handlers):
            self.connection._notice_handlers.remove(handler)
        self.connection.add_notice_handler(self.handler)

    def __enter__(self):
        return self.handler
    
    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        self.connection._notice_handlers.remove(self.handler)

    def handler(self, diag: Diagnostic):
        return postgresql_notice_handler(diag, logger=self.logger)


def postgresql_notice_handler(diag: Diagnostic, logger: logging.Logger = None):
    """
    Handler required by psycopg 3 `connection.add_notice_handler()`.
    """
    # determine level
    level, message = postgresql_parse_notice(diag.severity_nonlocalized, diag.message_primary)
    
    # determine logger by parsing context
    if not logger:
        name = f'{PostgreSql.__module__}.{PostgreSql.__qualname__}'
        m = re.match(r"^fonction [^\s]+ (\w+)", diag.context or '')
        if m:
            name += f":{m[1]}"
        logger = get_logger(name)

    # write log
    logger.log(level, message)


def postgresql_parse_notice(severity: str, message: str) -> tuple[int, str]:
    m = re.match(r'^\[?(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)[\]\:](?P<message>.+)$', message, re.DOTALL)
    if m:
        return getattr(logging, m['level']), m['message'].lstrip()

    if severity.startswith('DEBUG'): # not sent to client (by default)
        return logging.DEBUG, message
    elif severity == 'LOG': # not sent to client (by default), written on server log (LOG > ERROR for log_min_messages)
        return logging.DEBUG, message
    elif severity == 'NOTICE': # sent to client (by default) [=client_min_messages]
        return logging.DEBUG, message
    elif severity == 'INFO': # always sent to client
        return logging.INFO, message
    elif severity == 'WARNING': # sent to client (by default) [=log_min_messages]
        return logging.WARNING, message
    elif severity in ['ERROR', 'FATAL']: # sent to client
        return logging.ERROR, message
    elif severity in 'PANIC': # sent to client
        return logging.CRITICAL, message
    else:
        return logging.WARNING, message
