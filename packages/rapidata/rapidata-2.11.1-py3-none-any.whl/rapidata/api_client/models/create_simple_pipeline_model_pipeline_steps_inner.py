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
from rapidata.api_client.models.dataset_evaluation_step_model import DatasetEvaluationStepModel
from rapidata.api_client.models.send_completion_mail_step_model import SendCompletionMailStepModel
from rapidata.api_client.models.workflow_aggregation_step_model import WorkflowAggregationStepModel
from rapidata.api_client.models.workflow_labeling_step_model import WorkflowLabelingStepModel
from rapidata.api_client.models.workflow_split_model import WorkflowSplitModel
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

CREATESIMPLEPIPELINEMODELPIPELINESTEPSINNER_ONE_OF_SCHEMAS = ["DatasetEvaluationStepModel", "SendCompletionMailStepModel", "WorkflowAggregationStepModel", "WorkflowLabelingStepModel", "WorkflowSplitModel"]

class CreateSimplePipelineModelPipelineStepsInner(BaseModel):
    """
    Base model for a pipeline step
    """
    # data type: DatasetEvaluationStepModel
    oneof_schema_1_validator: Optional[DatasetEvaluationStepModel] = None
    # data type: SendCompletionMailStepModel
    oneof_schema_2_validator: Optional[SendCompletionMailStepModel] = None
    # data type: WorkflowAggregationStepModel
    oneof_schema_3_validator: Optional[WorkflowAggregationStepModel] = None
    # data type: WorkflowLabelingStepModel
    oneof_schema_4_validator: Optional[WorkflowLabelingStepModel] = None
    # data type: WorkflowSplitModel
    oneof_schema_5_validator: Optional[WorkflowSplitModel] = None
    actual_instance: Optional[Union[DatasetEvaluationStepModel, SendCompletionMailStepModel, WorkflowAggregationStepModel, WorkflowLabelingStepModel, WorkflowSplitModel]] = None
    one_of_schemas: Set[str] = { "DatasetEvaluationStepModel", "SendCompletionMailStepModel", "WorkflowAggregationStepModel", "WorkflowLabelingStepModel", "WorkflowSplitModel" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    discriminator_value_class_map: Dict[str, str] = {
    }

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
        instance = CreateSimplePipelineModelPipelineStepsInner.model_construct()
        error_messages = []
        match = 0
        # validate data type: DatasetEvaluationStepModel
        if not isinstance(v, DatasetEvaluationStepModel):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasetEvaluationStepModel`")
        else:
            match += 1
        # validate data type: SendCompletionMailStepModel
        if not isinstance(v, SendCompletionMailStepModel):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SendCompletionMailStepModel`")
        else:
            match += 1
        # validate data type: WorkflowAggregationStepModel
        if not isinstance(v, WorkflowAggregationStepModel):
            error_messages.append(f"Error! Input type `{type(v)}` is not `WorkflowAggregationStepModel`")
        else:
            match += 1
        # validate data type: WorkflowLabelingStepModel
        if not isinstance(v, WorkflowLabelingStepModel):
            error_messages.append(f"Error! Input type `{type(v)}` is not `WorkflowLabelingStepModel`")
        else:
            match += 1
        # validate data type: WorkflowSplitModel
        if not isinstance(v, WorkflowSplitModel):
            error_messages.append(f"Error! Input type `{type(v)}` is not `WorkflowSplitModel`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in CreateSimplePipelineModelPipelineStepsInner with oneOf schemas: DatasetEvaluationStepModel, SendCompletionMailStepModel, WorkflowAggregationStepModel, WorkflowLabelingStepModel, WorkflowSplitModel. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in CreateSimplePipelineModelPipelineStepsInner with oneOf schemas: DatasetEvaluationStepModel, SendCompletionMailStepModel, WorkflowAggregationStepModel, WorkflowLabelingStepModel, WorkflowSplitModel. Details: " + ", ".join(error_messages))
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

        # deserialize data into DatasetEvaluationStepModel
        try:
            instance.actual_instance = DatasetEvaluationStepModel.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SendCompletionMailStepModel
        try:
            instance.actual_instance = SendCompletionMailStepModel.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into WorkflowAggregationStepModel
        try:
            instance.actual_instance = WorkflowAggregationStepModel.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into WorkflowLabelingStepModel
        try:
            instance.actual_instance = WorkflowLabelingStepModel.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into WorkflowSplitModel
        try:
            instance.actual_instance = WorkflowSplitModel.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into CreateSimplePipelineModelPipelineStepsInner with oneOf schemas: DatasetEvaluationStepModel, SendCompletionMailStepModel, WorkflowAggregationStepModel, WorkflowLabelingStepModel, WorkflowSplitModel. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into CreateSimplePipelineModelPipelineStepsInner with oneOf schemas: DatasetEvaluationStepModel, SendCompletionMailStepModel, WorkflowAggregationStepModel, WorkflowLabelingStepModel, WorkflowSplitModel. Details: " + ", ".join(error_messages))
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

    def to_dict(self) -> Optional[Union[Dict[str, Any], DatasetEvaluationStepModel, SendCompletionMailStepModel, WorkflowAggregationStepModel, WorkflowLabelingStepModel, WorkflowSplitModel]]:
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


