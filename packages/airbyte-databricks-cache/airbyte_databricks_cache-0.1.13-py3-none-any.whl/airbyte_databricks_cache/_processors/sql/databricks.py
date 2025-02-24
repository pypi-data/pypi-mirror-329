"""A Databricks implementation of the SQL processor."""

from __future__ import annotations
from databricks.sqlalchemy.base import DatabricksDialect

from concurrent.futures import ThreadPoolExecutor
from textwrap import indent
from typing import TYPE_CHECKING

import sqlalchemy
import airbyte
from overrides import overrides
from pydantic import Field
from sqlalchemy import text

from airbyte import exceptions as exc
from airbyte._writers.jsonl import JsonlWriter
from airbyte.constants import DEFAULT_CACHE_SCHEMA_NAME
from airbyte.secrets.base import SecretString
from airbyte.shared import SqlProcessorBase
from airbyte.shared.sql_processor import SqlConfig
from airbyte.types import SQLTypeConverter
from airbyte.constants import (
    AB_EXTRACTED_AT_COLUMN,
    AB_META_COLUMN,
    AB_RAW_ID_COLUMN,
    DEBUG_MODE,
)
from sqlalchemy.engine import Connection, Engine
from sqlalchemy import text, create_engine
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.sql.base import Executable
from sqlalchemy.engine.cursor import CursorResult
from airbyte._util.name_normalizers import LowerCaseNormalizer
import functools
from airbyte.logs import get_global_file_logger

if TYPE_CHECKING:
    from pathlib import Path

    from sqlalchemy.engine import Connection


MAX_UPLOAD_THREADS = 8


#
# HACK
# databricks sql dialect only implements those methods that are required for its e2e tests,
# but pyairbyte complains, hence we mark the property as None and it uses json.dumps as a backup
#
DatabricksDialect._json_serializer = None

# end of HACK

# Note for future:
# the size of the file beings uploaded to databricks volume can be tweaked as follows, if required:
# airbyte._writers.file_writers.FileWriterBase.MAX_BATCH_SIZE = 10_000

class DatabricksConfig(SqlConfig):

    access_token: str = Field(...)
    server_hostname: str = Field(...)
    http_path: str = Field(...)
    catalog: str = Field(...)
    schema_name: str = Field(...)
    table_prefix: str = Field(default="")
    staging_volume_w_location: str = Field(...)

    @overrides
    def get_sql_alchemy_url(self) -> SecretString:
        """Return the SQLAlchemy URL to use."""
        return SecretString(
            f"databricks://token:{self.access_token}@{self.server_hostname}?" +
            f"http_path={self.http_path}&catalog={self.catalog}&schema={self.schema_name}"
        )

    @overrides
    def get_database_name(self) -> str:
        """Return the name of the database."""
        return self.schema_name

    @overrides
    def get_sql_engine(self) -> Engine:
        """Return a new SQL engine to use."""
        return create_engine(
            url=self.get_sql_alchemy_url(),
            echo=DEBUG_MODE,
            execution_options={
                "schema_translate_map": {None: self.schema_name}
            },
            future=True,
            connect_args={
                # this connect arg is requried for databricks
                # ref: https://docs.databricks.com/en/dev-tools/python-sql-connector.html#manage-files-in-unity-catalog-volumes
                "staging_allowed_local_path": "/"
            },
            pool_pre_ping=True,
            pool_recycle=300
        )


class DatabricksSQLTypeConverter(SQLTypeConverter):

    @overrides
    def to_sql_type(  # noqa: PLR0911  # Too many return statements
        self,
        json_schema_property_def: dict[str, str | dict | list],
    ) -> sqlalchemy.types.TypeEngine:
        """Convert a value to a SQL type.
        override: convert certail sqlalchemy types into databricks types

        """
        sql_type = super().to_sql_type(json_schema_property_def)

        if isinstance(sql_type, sqlalchemy.types.VARCHAR):
            # variant doesnt work because sqlalchemy complains. there is a dataricks issue to support it: https://github.com/databricks/databricks-sql-python/issues/424
            return "STRING"
        if isinstance(sql_type, sqlalchemy.types.DECIMAL):
            return "DOUBLE"
        # Note: do not convert sqlalchemy.types.JSON to string here, as it is deal with JIT so as to identify them separate from string and use to_json in the COPY TO statement
        return sql_type


class DatabricksNormalizer(LowerCaseNormalizer):

    @staticmethod
    @functools.cache
    def normalize(name: str) -> str:
        """Normalize the name, truncating to 255 characters."""
        return LowerCaseNormalizer.normalize(name)[:255]


class DatabricksSqlProcessor(SqlProcessorBase):
    supports_merge_insert = False
    file_writer_class = JsonlWriter
    sql_config: DatabricksConfig
    normalizer = DatabricksNormalizer
    type_converter_class = DatabricksSQLTypeConverter  # creating our own typeconverter

    @overrides
    def _quote_identifier(self, identifier: str) -> str:
        """
            Return the given identifier, quoted.
            override: use backticks instead of duble quotes for databricks
        """
        return f'`{identifier}`'

    @overrides
    def _execute_sql(self, sql: str | TextClause | Executable) -> CursorResult:
        """
            Execute the given SQL statement.
            override: logging for any SQL being executed
        """
        logger = get_global_file_logger()  # here to makde sure the hacked version is picked up
        if logger is None:
            print("WARN logging is disabled as no temp directory available. Use AIRBYTE_LOGGING_ROOT to configure logging if required")
        else:
            logger.info(f"executing SQL on databricks:")
            logger.info(f"{sql}")
        return super()._execute_sql(sql)

    @overrides
    def _swap_temp_table_with_final_table(
        self,
        stream_name: str,
        temp_table_name: str,
        final_table_name: str,
    ) -> None:
        """Merge the temp table into the main one.

        This implementation requires MERGE support in the SQL DB.
        Databases that do not support this syntax can override this method.

        override: split SQL statements sp can run on Databricks
        """
        if final_table_name is None:
            raise exc.PyAirbyteInternalError(
                message="Arg 'final_table_name' cannot be None.")
        if temp_table_name is None:
            raise exc.PyAirbyteInternalError(
                message="Arg 'temp_table_name' cannot be None.")

        _ = stream_name
        deletion_name = f"{final_table_name}_deleteme"
        commands = "\n".join(
            [
                f"ALTER TABLE {self._fully_qualified(final_table_name)} RENAME "
                f"TO {deletion_name};",
                f"ALTER TABLE {self._fully_qualified(temp_table_name)} RENAME "
                f"TO {final_table_name};",
                f"DROP TABLE {self._fully_qualified(deletion_name)};",
            ]
        )
        for command in commands.split("\n"):
            self._execute_sql(command)

    # @overrides a final class
    def _get_sql_column_definitions(
        self,
        stream_name: str,
    ) -> dict[str, sqlalchemy.types.TypeEngine]:
        """
            Return the column definitions for the given stream.
            override: to replace types for AB_RAW_ID_COLUMN and AB_META_COLUMN

        """
        columns: dict[str, sqlalchemy.types.TypeEngine] = {}
        properties = self.catalog_provider.get_stream_properties(stream_name)
        for property_name, json_schema_property_def in properties.items():
            clean_prop_name = self.normalizer.normalize(property_name)
            columns[clean_prop_name] = self.type_converter.to_sql_type(
                json_schema_property_def,
            )

        # override: replace with STRING to avoid VARCHAR that databricks doesnt support without size
        # self.type_converter_class.get_string_type()
        columns[AB_RAW_ID_COLUMN] = "STRING"
        columns[AB_EXTRACTED_AT_COLUMN] = sqlalchemy.TIMESTAMP()
        columns[AB_META_COLUMN] = self.type_converter_class.get_json_type()

        return columns

    # @overrides final table
    def _create_table_for_loading(
        self,
        /,
        stream_name: str,
        batch_id: str,
    ) -> str:
        """Create a new table for loading data."""
        temp_table_name = self._get_temp_table_name(stream_name, batch_id)
        column_definition_str = ",\n  ".join(
            # f"{self._quote_identifier(column_name)} {sql_type}"
            # this is the override - replace JSON with STRING JIT
            f"{self._quote_identifier(column_name)} {'STRING' if isinstance(sql_type, sqlalchemy.types.JSON) else sql_type}"
            for column_name, sql_type in self._get_sql_column_definitions(stream_name).items()
        )
        self._create_table(temp_table_name, column_definition_str)

        return temp_table_name

    @overrides
    def _ensure_final_table_exists(
        self,
        stream_name: str,
        *,
        create_if_missing: bool = True,
    ) -> str:
        """Create the final table if it doesn't already exist.

        Return the table name.
        override: replace JSON with STRING
        """
        table_name = self.get_sql_table_name(stream_name)
        did_exist = self._table_exists(table_name)
        if not did_exist and create_if_missing:
            column_definition_str = ",\n  ".join(
                # f"{self._quote_identifier(column_name)} {sql_type}"
                # this is the override - replace JSON with STRING JIT
                f"{self._quote_identifier(column_name)} {'STRING' if isinstance(sql_type, sqlalchemy.types.JSON) else sql_type}"
                for column_name, sql_type in self._get_sql_column_definitions(
                    stream_name,
                ).items()
            )
            self._create_table(table_name, column_definition_str)

        return table_name

    @overrides
    def _write_files_to_new_table(
        self,
        files: list[Path],
        stream_name: str,
        batch_id: str,
    ) -> str:
        """
            Write files to a new table.
            override: databricks specific SQL commands for PUT and COPY INTO
        """
        temp_table_name = self._create_table_for_loading(
            stream_name=stream_name,
            batch_id=batch_id,
        )
        internal_sf_stage_name = (
            # airbyte.get_secret("databricks_staging_volume_w_location")
            self.sql_config.staging_volume_w_location
            + "/" + stream_name
        )

        def path_str(path: Path) -> str:
            return str(path.absolute()).replace("\\", "\\\\")

        def upload_file(file_path: Path) -> None:
            query = f"PUT '{path_str(file_path)}' INTO '{internal_sf_stage_name}/{file_path.name}';"
            self._execute_sql(query)

        with ThreadPoolExecutor(max_workers=MAX_UPLOAD_THREADS) as executor:
            try:
                executor.map(upload_file, files)
            except Exception as e:
                raise exc.PyAirbyteInternalError(
                    message="Failed to upload batch files to Snowflake.",
                    context={"files": [str(f) for f in files]},
                ) from e

        columns_list = [
            self._quote_identifier(c)
            for c in list(self._get_sql_column_definitions(stream_name).keys())
        ]
        files_list = ", ".join([f"'{f.name}'" for f in files])
        columns_list_str: str = indent("\n, ".join(columns_list), " " * 12)
        variant_cols_str: str = (
            "\n" + " " * 21 + ", ").join([f"$1:{col}" for col in columns_list])

        column_definitions = self._get_sql_column_definitions(stream_name)

        # removing _airbyte_meta as when it is = '{}', which is almost always, and spark doesnt read that col,
        # leading to failure of code because col doesnt exist in cast(`_airbyte_meta` as MAP<STRING, STRING>)
        # ref: AB_META_COLUMN is hardcoded as {} in this file: .venv/lib/python3.11/site-packages/airbyte/records.py
        del column_definitions['_airbyte_meta']

        # we cast so as to not use spark inferred schema when reading json files
        l_column_definition_str_w_cast = []
        for column_name, sql_type in column_definitions.items():
            if isinstance(sql_type, sqlalchemy.types.JSON):
                # struct/maps read from spark are identified as json by sqlalchemy
                # these cols lose information if they are casted to string directly , so we identify the ones that are json, and perform to_json before casting to 'string' type
                # replace JSON with STRING JIT
                sql_type = 'STRING'
                # e.g. "cast(to_json(`col1`) as variant) as `col1`"
                l_column_definition_str_w_cast.append(
                    f"cast(to_json({self._quote_identifier(column_name)}) as {sql_type}) as {self._quote_identifier(column_name)}")
            else:
                # e.g. "cast(`col1` as string) as `col1`"
                l_column_definition_str_w_cast.append(
                    f"cast({self._quote_identifier(column_name)} as {sql_type}) as {self._quote_identifier(column_name)}")

        column_definition_str_w_cast = ",\n  ".join(
            l_column_definition_str_w_cast)

        copy_statement = f""" 
            COPY INTO {temp_table_name}
            -- FROM '{internal_sf_stage_name}' 
            -- we will need to cast since databricks COPY INTO infers colmns
            FROM (
                SELECT 
                {column_definition_str_w_cast}
                FROM '{internal_sf_stage_name}'
                )
            FILEFORMAT = JSON
            FILES = ( {files_list} )
            -- FORMAT_OPTIONS ('inferSchema' = 'true', 'mergeSchema' = 'true')
            COPY_OPTIONS ('mergeSchema' = 'true')
        """
        self._execute_sql(text(copy_statement))
        return temp_table_name

    @overrides
    def _add_column_to_table(
        self,
        table: sqlalchemy.Table,
        column_name: str,
        column_type: sqlalchemy.types.TypeEngine,
    ) -> None:
        """
        Add a column to the given table.
        override: replace JSON with STRING
        """
        if isinstance(column_type, sqlalchemy.types.JSON):
            # # this is the override - replace JSON with STRING JIT
            column_type = 'STRING'

        self._execute_sql(
            text(
                f"ALTER TABLE {self._fully_qualified(table.name)} "
                f"ADD COLUMN {column_name} {column_type}"
            ),
        )
