# coding: utf-8

"""
    Rapidata.Dataset

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: v1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from rapidata.api_client.models.get_compare_workflow_result_overview_result import GetCompareWorkflowResultOverviewResult
from rapidata.api_client.models.get_compare_workflow_result_overview_small_result import GetCompareWorkflowResultOverviewSmallResult
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

COMPAREWORKFLOWGETRESULTOVERVIEWGET200RESPONSE_ONE_OF_SCHEMAS = ["GetCompareWorkflowResultOverviewResult", "GetCompareWorkflowResultOverviewSmallResult"]

class CompareWorkflowGetResultOverviewGet200Response(BaseModel):
    """
    CompareWorkflowGetResultOverviewGet200Response
    """
    # data type: GetCompareWorkflowResultOverviewResult
    oneof_schema_1_validator: Optional[GetCompareWorkflowResultOverviewResult] = None
    # data type: GetCompareWorkflowResultOverviewSmallResult
    oneof_schema_2_validator: Optional[GetCompareWorkflowResultOverviewSmallResult] = None
    actual_instance: Optional[Union[GetCompareWorkflowResultOverviewResult, GetCompareWorkflowResultOverviewSmallResult]] = None
    one_of_schemas: Set[str] = { "GetCompareWorkflowResultOverviewResult", "GetCompareWorkflowResultOverviewSmallResult" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = CompareWorkflowGetResultOverviewGet200Response.model_construct()
        error_messages = []
        match = 0
        # validate data type: GetCompareWorkflowResultOverviewResult
        if not isinstance(v, GetCompareWorkflowResultOverviewResult):
            error_messages.append(f"Error! Input type `{type(v)}` is not `GetCompareWorkflowResultOverviewResult`")
        else:
            match += 1
        # validate data type: GetCompareWorkflowResultOverviewSmallResult
        if not isinstance(v, GetCompareWorkflowResultOverviewSmallResult):
            error_messages.append(f"Error! Input type `{type(v)}` is not `GetCompareWorkflowResultOverviewSmallResult`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in CompareWorkflowGetResultOverviewGet200Response with oneOf schemas: GetCompareWorkflowResultOverviewResult, GetCompareWorkflowResultOverviewSmallResult. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in CompareWorkflowGetResultOverviewGet200Response with oneOf schemas: GetCompareWorkflowResultOverviewResult, GetCompareWorkflowResultOverviewSmallResult. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into GetCompareWorkflowResultOverviewResult
        try:
            instance.actual_instance = GetCompareWorkflowResultOverviewResult.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into GetCompareWorkflowResultOverviewSmallResult
        try:
            instance.actual_instance = GetCompareWorkflowResultOverviewSmallResult.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into CompareWorkflowGetResultOverviewGet200Response with oneOf schemas: GetCompareWorkflowResultOverviewResult, GetCompareWorkflowResultOverviewSmallResult. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into CompareWorkflowGetResultOverviewGet200Response with oneOf schemas: GetCompareWorkflowResultOverviewResult, GetCompareWorkflowResultOverviewSmallResult. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], GetCompareWorkflowResultOverviewResult, GetCompareWorkflowResultOverviewSmallResult]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


