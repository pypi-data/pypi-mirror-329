import typing as t
from enum import Enum

import pydantic


class FieldType(str, Enum):
    SECRET = "SECRET"
    HIDDEN = "HIDDEN"
    MULTI_LINES = "MULTI_LINES"


def _extract_json_schema_extra(**kwargs) -> dict[str, t.Any]:
    json_schema_extra = (
        kwargs.pop("json_schema_extra") if "json_schema_extra" in kwargs else {}
    ) or {}
    return json_schema_extra


def SecretField(*args, **kwargs):
    json_schema_extra = _extract_json_schema_extra(**kwargs)
    json_schema_extra["x-field_type"] = FieldType.SECRET
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)


def HiddenField(*args, **kwargs):
    """
    A field we don't want a user to see + fill out, but not a secret.
    """
    json_schema_extra = _extract_json_schema_extra(**kwargs)
    json_schema_extra["x-field_type"] = FieldType.HIDDEN
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)


def MultiLinesField(*args, **kwargs):
    json_schema_extra = _extract_json_schema_extra(**kwargs)
    json_schema_extra["x-field_type"] = FieldType.MULTI_LINES
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)


def GroupedField(group: str, *args, **kwargs):
    """
    A field that we want to group together in the UI

    :param group: The title of the group to group the field under
    """
    json_schema_extra = _extract_json_schema_extra(**kwargs)
    json_schema_extra["x-field_group"] = group
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)


def IntegrationField(
    group: str | None = None,
    multiline: bool = False,
    secret: bool = False,
    *args,
    **kwargs,
):
    """
    A Field that can be used to combine multiple types of fields such as SecretField and GroupedField

    :param group: The title of the group to group the field under
    :param priority: The priority of the field, lower numbers are displayed first
    :param multiline: Whether the field should be a multi-line text field
    :param secret: Whether the field should be a secret field
    """
    json_schema_extra = _extract_json_schema_extra(**kwargs)
    if group:
        json_schema_extra["x-field_group"] = group

    if all([multiline, secret]):
        raise ValueError("Cannot have both multiline and secret fields")
    if multiline:
        json_schema_extra["x-field_type"] = FieldType.MULTI_LINES
    if secret:
        json_schema_extra["x-field_type"] = FieldType.SECRET
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)
