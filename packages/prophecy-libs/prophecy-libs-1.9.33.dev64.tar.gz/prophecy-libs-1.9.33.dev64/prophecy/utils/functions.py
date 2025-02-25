from pyspark.sql import Column
import inspect

from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import StructType


def get_alias(column: Column):
    try:
        return column._jc.expr().name()
    except:
        return column._jc.expr().sql()

def flatten_struct(df: DataFrame, parent_column: str, struct_type: StructType) -> DataFrame:
    expanded_columns = [col(f"`{parent_column}`.`{field.name}`").alias(field.name) for field in struct_type.fields]
    new_df = df
    for column in expanded_columns:
        new_df = new_df.withColumn(get_alias(column), column)
    new_df = new_df.drop(parent_column)

    return new_df


def add_rule(df: DataFrame, column: Column) -> DataFrame:
    column_name = get_alias(column)
    df = df.withColumn(column_name, column)
    column_schema = df.schema[column_name]
    is_multi_column_output = next(
    (field.metadata.get("isMultiColumnOutput", False)
     for field in df.schema.fields
     if field.name == column_name),
    False
     )
    if is_multi_column_output and isinstance(column_schema.dataType, StructType):
        return flatten_struct(df, column_name, column_schema.dataType)
    else:
        return df


def get_column_metadata():
    return {"isMultiColumnOutput": True}


def execute_rule(rule_func):
    """
    Decorator to be used with rule definitions. This will do lazy evaluation of
    default values of rules param.
    """
    def get_value(argument):
        if isinstance(argument, Column):
            return argument
        if callable(argument):
            return argument()
        else:
            return argument
    def wrapper(*args, **kwargs):
        args_with_default = {}
        for (name, param) in inspect.signature(rule_func).parameters.items():
            if param.default is not param.empty:
                args_with_default[name] = param.default
            else:
                args_with_default[name] = None
        to_be_updated_keys = list(args_with_default.keys())[0:len(args)]
        for index in range(len(args)):
            args_with_default.update({to_be_updated_keys[index]: args[index]})
        updated_args = {**args_with_default, **kwargs}
        result = rule_func(**{key: get_value(value) for (key, value) in updated_args.items()})
        return result
    return wrapper