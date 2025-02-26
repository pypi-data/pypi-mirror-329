# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.featurestore.contracts.column import ColumnType

# Declare any spark type that should be serialized here.
columnType_serializable_const = set([ColumnType.FLOAT, ColumnType.DOUBLE, ColumnType.BINARY])


def _get_lookup_key(featureset, row):
    prefix, suffix_column_name = _get_lookup_key_pattern(featureset, featureset.online_materialization_version)

    return _get_lookup_key_udf(prefix, suffix_column_name, row)


def _get_lookup_key_udf(prefix, suffix_column_names, row):
    suffix_parts = []

    for index_column in suffix_column_names:
        suffix_parts.append(index_column)
        suffix_parts.append(row[index_column])

    suffix = ":".join(suffix_parts)
    return f"{prefix}:{suffix}"


def _get_lookup_key_pattern(featureset, materialization_version=None):
    prefix = f"featurestore:{featureset.feature_store_guid}:featureset:{featureset.name}:version:{featureset.version}:"
    # update when feature set has online materialize prefix returned from backend
    if materialization_version:
        prefix = f"{prefix}{materialization_version}:"

    suffix_column_names = []

    for entity in featureset.entities:
        for index_column in entity.index_columns:
            suffix_column_names.append(index_column.name)

    return prefix.lower(), suffix_column_names


def _get_redis_function_key_format(key_columns):
    key_cols_formatted = "{"
    for key in key_columns:
        key_cols_formatted = key_cols_formatted + "'" + key + "'"
        if not key == key_columns[-1]:
            key_cols_formatted += ","
    key_cols_formatted += "}"
    return key_cols_formatted


def _get_redis_function_value_column_name_format(value_columns):
    value_cols_formatted = "{"
    for value in value_columns:
        value_cols_formatted = value_cols_formatted + "'" + value + "'"
        if not value == value_columns[-1]:
            value_cols_formatted += ","
    value_cols_formatted += "}"
    return value_cols_formatted


def _get_serializable_column_datatype():
    return set(columnType_serializable_const)
