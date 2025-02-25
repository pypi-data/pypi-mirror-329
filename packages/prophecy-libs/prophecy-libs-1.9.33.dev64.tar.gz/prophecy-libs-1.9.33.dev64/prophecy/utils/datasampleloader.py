from typing import Optional, Dict, Tuple, List, Iterator
from pyspark.sql import DataFrame, Row
from pyspark.sql.functions import expr
from pyspark.sql.types import StructType, StringType, ArrayType, MapType, BinaryType
import json


class DataSampleLoaderLib:
    # Constants
    MAX_ROWS: int = 10000  # Maximum number of rows to cache or process at a time
    TOTAL_ROWS_SIZE_THRESHOLD: int = (
        1024 * 1024 * 2.5
    )  # 2.5MB threshold for total rows size in JSON format
    CHAR_LIMIT: int = 1024 * 200  # 200KB character limit for truncating string columns

    # Class-level variables (shared state)
    _dataframes_map: Dict[str, Tuple[DataFrame, bool, int]] = (
        {}
    )  # Map to store registered DataFrames
    _row_cache: List = []  # Cache for storing rows of the DataFrame
    _cached_dataframe_schema: Optional[StructType] = (
        None  # Schema of the cached DataFrame
    )
    _cached_dataframe_key: Optional[str] = None  # Key of the cached DataFrame
    _real_dataframe_offset: int = 0  # Offset for the real DataFrame

    @classmethod
    def interim_key(cls, component: str, port: str) -> str:
        """
        Generate an interim key for a component and port.
        Used to uniquely identify interim DataFrames.
        """
        return f"{component}__{port}_interim"

    @classmethod
    def interim_key_dx(cls, component: str, port: str) -> str:
        """
        Generate an interim key with a '_dx' suffix for a component and port.
        Used to uniquely identify interim DataFrames with a specific suffix.
        """
        return f"{component}__{port}_interim_dx"

    @classmethod
    def _get_entry_from_dataframes_map(cls, key: str) -> Tuple[DataFrame, bool, int]:
        """
        Retrieve an entry from the _dataframes_map using the provided key.
        Returns a tuple containing the DataFrame, a boolean indicating if truncated columns should be created, and the row limit.
        """
        return cls._dataframes_map.get(key, (None, False, cls.MAX_ROWS))

    @classmethod
    def _get_json_encoded_len(cls, schema: StructType) -> int:
        """
        Calculate the length of the JSON encoded representation of the schema.
        This is used to estimate the payload size for caching.
        """
        total_fields = len(schema.fields)
        fields_name_len = 0
        try:
            for f in schema.fields:
                print("field: ", f, f.name)
                fields_name_len += len(f.name)
        except Exception as e:
            print("calculating fields name length", e)
            fields_name_len = total_fields * 5

        return fields_name_len + (3 * total_fields)

    @classmethod
    def _cache_dataframe_rows(
        cls, df: DataFrame, create_truncated_columns: bool, df_offset: int, limit: int
    ) -> None:
        """
        Cache rows of the DataFrame in memory.
        If create_truncated_columns is True, create a new DataFrame with truncated columns.
        The cached rows are stored in _row_cache.
        """
        cls._row_cache.clear()

        df_new = (
            cls._create_truncated_columns_dataframe(df)
            if create_truncated_columns
            else df
        )
        cls._cached_dataframe_schema = df_new.schema

        iterator: Iterator[Row] = None
        try:
            iterator = df_new.offset(df_offset).limit(limit).toLocalIterator()
        except Exception as e:
            iterator = iter(df_new.limit(df_offset + limit).tail(limit))
        finally:
            _real_dataframe_offset = df_offset

        json_encoded_len_to_subtract = cls._get_json_encoded_len(df.schema)

        size_so_far = 0
        try:
            for row in iterator:
                row_json = json.dumps(row.asDict(recursive=True))
                row_size = len(row_json.encode("utf-8")) - json_encoded_len_to_subtract
                # Stop if we exceed constraints
                if (
                    size_so_far + row_size > cls.TOTAL_ROWS_SIZE_THRESHOLD
                    and len(cls._row_cache) != 0
                ):
                    break

                cls._row_cache.append(row_json)
                size_so_far += row_size
        except Exception as e:
            print(e)

        print(f"Cached in memory: Memory={size_so_far}, Rows={len(cls._row_cache)}")

    @classmethod
    def _create_truncated_columns_dataframe(
        cls, df: DataFrame, limit: int = CHAR_LIMIT
    ) -> DataFrame:
        """
        Create a new DataFrame with truncated columns.
        Truncates columns of types StringType, ArrayType, MapType, StructType, and BinaryType to the specified limit.
        """
        truncatable_types = (StringType, ArrayType, MapType, StructType, BinaryType)
        if not any(
            isinstance(field.dataType, truncatable_types) for field in df.schema.fields
        ):
            return df

        # Process binary columns first
        # binary_columns = [
        #     field.name for field in df.schema.fields
        #     if isinstance(field.dataType, BinaryType)
        # ]
        # result_df = df.drop(*binary_columns) if binary_columns else df

        # Build all column expressions at once
        for field in df.schema.fields:
            if isinstance(field.dataType, truncatable_types):
                substitute_col = ""
                if isinstance(field.dataType, StringType):
                    substitute_col = f"{field.name}"
                elif isinstance(field.dataType, BinaryType):
                    substitute_col = f"BASE64({field.name})"
                else:
                    substitute_col = f"TO_JSON({field.name})"
                df = df.withColumn(
                    field.name,
                    expr(
                        f"CASE WHEN LENGTH({substitute_col}) > {limit} THEN CONCAT(SUBSTRING({substitute_col}, 1, {limit - 3}), '...') ELSE {substitute_col} END"
                    ).cast("string"),
                )

        return df

    @classmethod
    def register(
        cls,
        key: str,
        df: DataFrame,
        limit: int = MAX_ROWS,
        create_truncated_columns: bool = True,
    ) -> DataFrame:
        """
        Register a DataFrame with an optional truncation.
        Stores the DataFrame in _dataframes_map with the provided key.
        """
        cls._dataframes_map[key] = (df, create_truncated_columns, limit)
        if cls._cached_dataframe_key == key:
            cls._clear_cache()

        return df

    @classmethod
    def get_cached_data(
        cls, key: str, cache_offset: int, df_offset: int
    ) -> Optional[List]:
        """
        Get cached data for the DataFrame identified by the key.
        If the DataFrame is not cached or the cache is invalid, cache the DataFrame rows.
        Returns a list of cached rows starting from the specified cache_offset.
        """
        df, create_truncated_columns, limit = cls._get_entry_from_dataframes_map(key)

        if df is None:
            return None

        if (
            cls._cached_dataframe_key != key
            or not cls._row_cache
            or len(cls._row_cache) == 0
            or df_offset != cls._real_dataframe_offset
        ):
            cls._cached_dataframe_key = key
            cls._cache_dataframe_rows(df, create_truncated_columns, df_offset, limit)

        safe_offset = cache_offset if cache_offset > 0 else 0
        return cls._row_cache[safe_offset:]

    @classmethod
    def get_dataframe_for_display(
        cls, key: str, cache_offset: int = 0, df_offset: int = 0
    ) -> Optional[DataFrame]:
        """
        Get a DataFrame for display with caching.
        Converts cached JSON rows back to DataFrame rows and returns a new DataFrame.
        """
        df, _, _ = cls._get_entry_from_dataframes_map(key)
        data = cls.get_cached_data(key, cache_offset, df_offset)

        # Convert JSON rows back to dict
        rows = [Row(**(json.loads(row))) for row in data]

        return df.sparkSession.createDataFrame(
            data=rows, schema=cls._cached_dataframe_schema
        )

    @classmethod
    def get_payload(cls, key: str, job: str, df_offset: int = 0) -> Optional[str]:
        """
        Get payload with proper JSON handling.
        Returns a JSON string containing the job, schema, and data of the DataFrame.
        """
        data = cls.get_cached_data(key, 0, df_offset)
        df, _, _ = cls._get_entry_from_dataframes_map(key)

        if data is None or df is None:
            return None

        try:
            schema_json = df.schema.json()
            data_json = f'[{",".join(data)}]'  # json.dumps(data)

            result = df.sparkSession.createDataFrame(
                [(key, job, schema_json, data_json)], ["key", "job", "schema", "data"]
            )

            return result.toJSON().first()
        except Exception as e:
            print(f"Error creating payload: {str(e)}")  # Log error before raising
            raise ValueError(f"Error creating payload: {str(e)}")

    @classmethod
    def _clear_cache(cls) -> None:
        """
        Clear cached DataFrame rows.
        Resets the _row_cache, _cached_dataframe_key, and _real_dataframe_offset.
        """
        cls._row_cache.clear()
        cls._cached_dataframe_key = None
        cls._real_dataframe_offset = 0

    @classmethod
    def clear(cls) -> None:
        """
        Clear all cached DataFrame rows and the _dataframes_map.
        """
        cls._clear_cache()
        cls._dataframes_map = {}

    @classmethod
    def get_original_schema_for_dataframe(
        cls,
        key: str,
    ) -> Optional[DataFrame]:
        """
        Get the original schema for the DataFrame identified by the key.
        Returns an empty DataFrame with the original schema.
        """
        df, _, _ = cls._get_entry_from_dataframes_map(key)

        return df.sparkSession.createDataFrame(data=[], schema=df.schema)
