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
from rapidata.api_client.models.attach_category_rapid_blueprint import AttachCategoryRapidBlueprint
from rapidata.api_client.models.bounding_box_rapid_blueprint import BoundingBoxRapidBlueprint
from rapidata.api_client.models.compare_rapid_blueprint import CompareRapidBlueprint
from rapidata.api_client.models.free_text_rapid_blueprint import FreeTextRapidBlueprint
from rapidata.api_client.models.line_rapid_blueprint import LineRapidBlueprint
from rapidata.api_client.models.locate_rapid_blueprint import LocateRapidBlueprint
from rapidata.api_client.models.named_entity_rapid_blueprint import NamedEntityRapidBlueprint
from rapidata.api_client.models.polygon_rapid_blueprint import PolygonRapidBlueprint
from rapidata.api_client.models.scrub_rapid_blueprint import ScrubRapidBlueprint
from rapidata.api_client.models.transcription_rapid_blueprint import TranscriptionRapidBlueprint
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

SIMPLEWORKFLOWCONFIGMODELBLUEPRINT_ONE_OF_SCHEMAS = ["AttachCategoryRapidBlueprint", "BoundingBoxRapidBlueprint", "CompareRapidBlueprint", "FreeTextRapidBlueprint", "LineRapidBlueprint", "LocateRapidBlueprint", "NamedEntityRapidBlueprint", "PolygonRapidBlueprint", "ScrubRapidBlueprint", "TranscriptionRapidBlueprint"]

class SimpleWorkflowConfigModelBlueprint(BaseModel):
    """
    The blueprint to use when creating rapids for this workflow.  The blueprint determines what kind of rapids will be created and what data they will contain.
    """
    # data type: TranscriptionRapidBlueprint
    oneof_schema_1_validator: Optional[TranscriptionRapidBlueprint] = None
    # data type: ScrubRapidBlueprint
    oneof_schema_2_validator: Optional[ScrubRapidBlueprint] = None
    # data type: PolygonRapidBlueprint
    oneof_schema_3_validator: Optional[PolygonRapidBlueprint] = None
    # data type: NamedEntityRapidBlueprint
    oneof_schema_4_validator: Optional[NamedEntityRapidBlueprint] = None
    # data type: LocateRapidBlueprint
    oneof_schema_5_validator: Optional[LocateRapidBlueprint] = None
    # data type: LineRapidBlueprint
    oneof_schema_6_validator: Optional[LineRapidBlueprint] = None
    # data type: FreeTextRapidBlueprint
    oneof_schema_7_validator: Optional[FreeTextRapidBlueprint] = None
    # data type: CompareRapidBlueprint
    oneof_schema_8_validator: Optional[CompareRapidBlueprint] = None
    # data type: AttachCategoryRapidBlueprint
    oneof_schema_9_validator: Optional[AttachCategoryRapidBlueprint] = None
    # data type: BoundingBoxRapidBlueprint
    oneof_schema_10_validator: Optional[BoundingBoxRapidBlueprint] = None
    actual_instance: Optional[Union[AttachCategoryRapidBlueprint, BoundingBoxRapidBlueprint, CompareRapidBlueprint, FreeTextRapidBlueprint, LineRapidBlueprint, LocateRapidBlueprint, NamedEntityRapidBlueprint, PolygonRapidBlueprint, ScrubRapidBlueprint, TranscriptionRapidBlueprint]] = None
    one_of_schemas: Set[str] = { "AttachCategoryRapidBlueprint", "BoundingBoxRapidBlueprint", "CompareRapidBlueprint", "FreeTextRapidBlueprint", "LineRapidBlueprint", "LocateRapidBlueprint", "NamedEntityRapidBlueprint", "PolygonRapidBlueprint", "ScrubRapidBlueprint", "TranscriptionRapidBlueprint" }

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
        instance = SimpleWorkflowConfigModelBlueprint.model_construct()
        error_messages = []
        match = 0
        # validate data type: TranscriptionRapidBlueprint
        if not isinstance(v, TranscriptionRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `TranscriptionRapidBlueprint`")
        else:
            match += 1
        # validate data type: ScrubRapidBlueprint
        if not isinstance(v, ScrubRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `ScrubRapidBlueprint`")
        else:
            match += 1
        # validate data type: PolygonRapidBlueprint
        if not isinstance(v, PolygonRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `PolygonRapidBlueprint`")
        else:
            match += 1
        # validate data type: NamedEntityRapidBlueprint
        if not isinstance(v, NamedEntityRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `NamedEntityRapidBlueprint`")
        else:
            match += 1
        # validate data type: LocateRapidBlueprint
        if not isinstance(v, LocateRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `LocateRapidBlueprint`")
        else:
            match += 1
        # validate data type: LineRapidBlueprint
        if not isinstance(v, LineRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `LineRapidBlueprint`")
        else:
            match += 1
        # validate data type: FreeTextRapidBlueprint
        if not isinstance(v, FreeTextRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FreeTextRapidBlueprint`")
        else:
            match += 1
        # validate data type: CompareRapidBlueprint
        if not isinstance(v, CompareRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `CompareRapidBlueprint`")
        else:
            match += 1
        # validate data type: AttachCategoryRapidBlueprint
        if not isinstance(v, AttachCategoryRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AttachCategoryRapidBlueprint`")
        else:
            match += 1
        # validate data type: BoundingBoxRapidBlueprint
        if not isinstance(v, BoundingBoxRapidBlueprint):
            error_messages.append(f"Error! Input type `{type(v)}` is not `BoundingBoxRapidBlueprint`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in SimpleWorkflowConfigModelBlueprint with oneOf schemas: AttachCategoryRapidBlueprint, BoundingBoxRapidBlueprint, CompareRapidBlueprint, FreeTextRapidBlueprint, LineRapidBlueprint, LocateRapidBlueprint, NamedEntityRapidBlueprint, PolygonRapidBlueprint, ScrubRapidBlueprint, TranscriptionRapidBlueprint. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in SimpleWorkflowConfigModelBlueprint with oneOf schemas: AttachCategoryRapidBlueprint, BoundingBoxRapidBlueprint, CompareRapidBlueprint, FreeTextRapidBlueprint, LineRapidBlueprint, LocateRapidBlueprint, NamedEntityRapidBlueprint, PolygonRapidBlueprint, ScrubRapidBlueprint, TranscriptionRapidBlueprint. Details: " + ", ".join(error_messages))
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

        # deserialize data into TranscriptionRapidBlueprint
        try:
            instance.actual_instance = TranscriptionRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into ScrubRapidBlueprint
        try:
            instance.actual_instance = ScrubRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into PolygonRapidBlueprint
        try:
            instance.actual_instance = PolygonRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into NamedEntityRapidBlueprint
        try:
            instance.actual_instance = NamedEntityRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into LocateRapidBlueprint
        try:
            instance.actual_instance = LocateRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into LineRapidBlueprint
        try:
            instance.actual_instance = LineRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FreeTextRapidBlueprint
        try:
            instance.actual_instance = FreeTextRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into CompareRapidBlueprint
        try:
            instance.actual_instance = CompareRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AttachCategoryRapidBlueprint
        try:
            instance.actual_instance = AttachCategoryRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into BoundingBoxRapidBlueprint
        try:
            instance.actual_instance = BoundingBoxRapidBlueprint.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into SimpleWorkflowConfigModelBlueprint with oneOf schemas: AttachCategoryRapidBlueprint, BoundingBoxRapidBlueprint, CompareRapidBlueprint, FreeTextRapidBlueprint, LineRapidBlueprint, LocateRapidBlueprint, NamedEntityRapidBlueprint, PolygonRapidBlueprint, ScrubRapidBlueprint, TranscriptionRapidBlueprint. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into SimpleWorkflowConfigModelBlueprint with oneOf schemas: AttachCategoryRapidBlueprint, BoundingBoxRapidBlueprint, CompareRapidBlueprint, FreeTextRapidBlueprint, LineRapidBlueprint, LocateRapidBlueprint, NamedEntityRapidBlueprint, PolygonRapidBlueprint, ScrubRapidBlueprint, TranscriptionRapidBlueprint. Details: " + ", ".join(error_messages))
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

    def to_dict(self) -> Optional[Union[Dict[str, Any], AttachCategoryRapidBlueprint, BoundingBoxRapidBlueprint, CompareRapidBlueprint, FreeTextRapidBlueprint, LineRapidBlueprint, LocateRapidBlueprint, NamedEntityRapidBlueprint, PolygonRapidBlueprint, ScrubRapidBlueprint, TranscriptionRapidBlueprint]]:
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


