# coding: utf-8

"""
    Rapidata.Dataset

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: v1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class Filter(BaseModel):
    """
    Filter
    """ # noqa: E501
    var_field: Optional[StrictStr] = Field(default=None, alias="field")
    value: Optional[Any] = None
    operator: Optional[StrictStr] = None
    logic: Optional[StrictStr] = None
    filters: Optional[List[Filter]] = None
    __properties: ClassVar[List[str]] = ["field", "value", "operator", "logic", "filters"]

    @field_validator('operator')
    def operator_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['Eq', 'Neq', 'Gt', 'Gte', 'Lt', 'Lte', 'Contains', 'StartsWith', 'EndsWith']):
            raise ValueError("must be one of enum values ('Eq', 'Neq', 'Gt', 'Gte', 'Lt', 'Lte', 'Contains', 'StartsWith', 'EndsWith')")
        return value

    @field_validator('logic')
    def logic_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['And', 'Or']):
            raise ValueError("must be one of enum values ('And', 'Or')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Filter from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in filters (list)
        _items = []
        if self.filters:
            for _item_filters in self.filters:
                if _item_filters:
                    _items.append(_item_filters.to_dict())
            _dict['filters'] = _items
        # set to None if var_field (nullable) is None
        # and model_fields_set contains the field
        if self.var_field is None and "var_field" in self.model_fields_set:
            _dict['field'] = None

        # set to None if value (nullable) is None
        # and model_fields_set contains the field
        if self.value is None and "value" in self.model_fields_set:
            _dict['value'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Filter from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "field": obj.get("field"),
            "value": obj.get("value"),
            "operator": obj.get("operator"),
            "logic": obj.get("logic"),
            "filters": [Filter.from_dict(_item) for _item in obj["filters"]] if obj.get("filters") is not None else None
        })
        return _obj

# TODO: Rewrite to not use raise_errors
Filter.model_rebuild(raise_errors=False)

