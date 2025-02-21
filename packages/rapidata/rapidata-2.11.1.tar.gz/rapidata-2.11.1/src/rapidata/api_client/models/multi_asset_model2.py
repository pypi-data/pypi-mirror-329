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
from typing import Any, ClassVar, Dict, List
from rapidata.api_client.models.file_asset_model1_metadata_inner import FileAssetModel1MetadataInner
from typing import Optional, Set
from typing_extensions import Self

class MultiAssetModel2(BaseModel):
    """
    MultiAssetModel2
    """ # noqa: E501
    t: StrictStr = Field(description="Discriminator value for MultiAssetModel", alias="_t")
    assets: List[GetCompareWorkflowResultsResultAsset]
    metadata: List[FileAssetModel1MetadataInner]
    identifier: StrictStr
    __properties: ClassVar[List[str]] = ["_t", "assets", "metadata", "identifier"]

    @field_validator('t')
    def t_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['MultiAssetModel']):
            raise ValueError("must be one of enum values ('MultiAssetModel')")
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
        """Create an instance of MultiAssetModel2 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in assets (list)
        _items = []
        if self.assets:
            for _item_assets in self.assets:
                if _item_assets:
                    _items.append(_item_assets.to_dict())
            _dict['assets'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in metadata (list)
        _items = []
        if self.metadata:
            for _item_metadata in self.metadata:
                if _item_metadata:
                    _items.append(_item_metadata.to_dict())
            _dict['metadata'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MultiAssetModel2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "_t": obj.get("_t") if obj.get("_t") is not None else 'MultiAssetModel',
            "assets": [GetCompareWorkflowResultsResultAsset.from_dict(_item) for _item in obj["assets"]] if obj.get("assets") is not None else None,
            "metadata": [FileAssetModel1MetadataInner.from_dict(_item) for _item in obj["metadata"]] if obj.get("metadata") is not None else None,
            "identifier": obj.get("identifier")
        })
        return _obj

from rapidata.api_client.models.get_compare_workflow_results_result_asset import GetCompareWorkflowResultsResultAsset
# TODO: Rewrite to not use raise_errors
MultiAssetModel2.model_rebuild(raise_errors=False)

