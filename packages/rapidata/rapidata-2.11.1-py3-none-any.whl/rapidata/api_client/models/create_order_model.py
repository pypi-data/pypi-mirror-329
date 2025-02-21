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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from rapidata.api_client.models.ab_test_selection_a_inner import AbTestSelectionAInner
from rapidata.api_client.models.create_order_model_referee import CreateOrderModelReferee
from rapidata.api_client.models.create_order_model_user_filters_inner import CreateOrderModelUserFiltersInner
from rapidata.api_client.models.create_order_model_workflow import CreateOrderModelWorkflow
from rapidata.api_client.models.feature_flag_model import FeatureFlagModel
from typing import Optional, Set
from typing_extensions import Self

class CreateOrderModel(BaseModel):
    """
    This model is used to create a simple order
    """ # noqa: E501
    t: StrictStr = Field(description="Discriminator value for CreateOrderModel", alias="_t")
    order_name: StrictStr = Field(description="The name is used as an identifier for an order and can be freely chosen.", alias="orderName")
    workflow: CreateOrderModelWorkflow
    referee: CreateOrderModelReferee
    aggregator: Optional[StrictStr] = Field(default=None, description="The aggregator is used to determine how the data will be aggregated. The default behavior is enough for most cases")
    feature_flags: Optional[List[FeatureFlagModel]] = Field(default=None, description="The feature flags are used to enable or disable certain features.", alias="featureFlags")
    priority: Optional[StrictInt] = Field(default=None, description="The priority is used to prioritize over other orders.")
    is_sticky: Optional[StrictBool] = Field(default=None, description="Indicates if the underlying campaign should be sticky.", alias="isSticky")
    user_filters: List[CreateOrderModelUserFiltersInner] = Field(description="The user filters are used to restrict the order to only collect votes from a specific demographic.", alias="userFilters")
    validation_set_id: Optional[StrictStr] = Field(default=None, description="The validation set id can be changed to point to a specific validation set. if not provided a sane default will be  used.", alias="validationSetId")
    selections: Optional[List[AbTestSelectionAInner]] = Field(default=None, description="The selections are used to determine which tasks are shown to a user.")
    __properties: ClassVar[List[str]] = ["_t", "orderName", "workflow", "referee", "aggregator", "featureFlags", "priority", "isSticky", "userFilters", "validationSetId", "selections"]

    @field_validator('t')
    def t_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['CreateOrderModel']):
            raise ValueError("must be one of enum values ('CreateOrderModel')")
        return value

    @field_validator('aggregator')
    def aggregator_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['NonCommittal', 'MajorityVote', 'SimpleMatchup', 'LocateCluster', 'Classification', 'Locate', 'BoundingBox', 'Line', 'Transcription', 'SinglePointLocate', 'FreeText', 'Scrub']):
            raise ValueError("must be one of enum values ('NonCommittal', 'MajorityVote', 'SimpleMatchup', 'LocateCluster', 'Classification', 'Locate', 'BoundingBox', 'Line', 'Transcription', 'SinglePointLocate', 'FreeText', 'Scrub')")
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
        """Create an instance of CreateOrderModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of workflow
        if self.workflow:
            _dict['workflow'] = self.workflow.to_dict()
        # override the default output from pydantic by calling `to_dict()` of referee
        if self.referee:
            _dict['referee'] = self.referee.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in feature_flags (list)
        _items = []
        if self.feature_flags:
            for _item_feature_flags in self.feature_flags:
                if _item_feature_flags:
                    _items.append(_item_feature_flags.to_dict())
            _dict['featureFlags'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in user_filters (list)
        _items = []
        if self.user_filters:
            for _item_user_filters in self.user_filters:
                if _item_user_filters:
                    _items.append(_item_user_filters.to_dict())
            _dict['userFilters'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in selections (list)
        _items = []
        if self.selections:
            for _item_selections in self.selections:
                if _item_selections:
                    _items.append(_item_selections.to_dict())
            _dict['selections'] = _items
        # set to None if aggregator (nullable) is None
        # and model_fields_set contains the field
        if self.aggregator is None and "aggregator" in self.model_fields_set:
            _dict['aggregator'] = None

        # set to None if feature_flags (nullable) is None
        # and model_fields_set contains the field
        if self.feature_flags is None and "feature_flags" in self.model_fields_set:
            _dict['featureFlags'] = None

        # set to None if priority (nullable) is None
        # and model_fields_set contains the field
        if self.priority is None and "priority" in self.model_fields_set:
            _dict['priority'] = None

        # set to None if validation_set_id (nullable) is None
        # and model_fields_set contains the field
        if self.validation_set_id is None and "validation_set_id" in self.model_fields_set:
            _dict['validationSetId'] = None

        # set to None if selections (nullable) is None
        # and model_fields_set contains the field
        if self.selections is None and "selections" in self.model_fields_set:
            _dict['selections'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateOrderModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "_t": obj.get("_t") if obj.get("_t") is not None else 'CreateOrderModel',
            "orderName": obj.get("orderName"),
            "workflow": CreateOrderModelWorkflow.from_dict(obj["workflow"]) if obj.get("workflow") is not None else None,
            "referee": CreateOrderModelReferee.from_dict(obj["referee"]) if obj.get("referee") is not None else None,
            "aggregator": obj.get("aggregator"),
            "featureFlags": [FeatureFlagModel.from_dict(_item) for _item in obj["featureFlags"]] if obj.get("featureFlags") is not None else None,
            "priority": obj.get("priority"),
            "isSticky": obj.get("isSticky"),
            "userFilters": [CreateOrderModelUserFiltersInner.from_dict(_item) for _item in obj["userFilters"]] if obj.get("userFilters") is not None else None,
            "validationSetId": obj.get("validationSetId"),
            "selections": [AbTestSelectionAInner.from_dict(_item) for _item in obj["selections"]] if obj.get("selections") is not None else None
        })
        return _obj


