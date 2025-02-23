import logging
import re
from typing import Type


def get_display_name(column: str, idx: int = None) -> str:
    if idx:
        return f"{column} ({idx:03})"
    else:
        return column


def get_internal_name(column: str, idx: int = None) -> str:
    return get_sanitized_name(get_display_name(column, idx))


def get_import_name(column: str, idx: int = None) -> str:
    return get_display_name(column, idx)


def get_sanitized_name(displayName: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()


def log_error(error_message: str, error_type: Type[BaseException] = ValueError) -> None:
    """
    Logs an error message and raises an exception of the specified type.

    Args:
        error_message (str): The error message to log and include in the exception.
        error_type (Type[BaseException]): The type of exception to raise. Defaults to ValueError.

    Raises:
        BaseException: The exception of the specified type with the provided error message.
    """
    logging.error(error_message)
    raise error_type(error_message)


def clean_meta_data(data):
    for element in data:
        for column in [
            "attributeGroupInternalName",
            "focusOrder",
            "changedBy",
            "changedDate",
            "createdBy",
            "creationDate",
            "metadataTemplateId",
            "conflictState",
            "focusAggregationFunction",
            "focusAggregationGroupByTargetType",
            "focusAggregationSourceColumnInternalName",
            "focusGroupByTargetInternalName",
            "parentAttributeGroupInternalName",
        ]:
            element.pop(column, None)

    return data