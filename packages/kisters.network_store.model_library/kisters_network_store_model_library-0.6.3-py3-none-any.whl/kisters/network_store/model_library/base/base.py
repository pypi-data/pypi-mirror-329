from __future__ import annotations

import enum
from datetime import datetime
from typing import Annotated, Any, Dict, List, Literal, Optional, Tuple, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    StringConstraints,
    model_validator,
)


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NetworkRef(Model):
    network_id: str
    network_datetime: Optional[datetime] = None
    element_group_uid: Optional[str] = None


UserMetadataKey = Annotated[str, Annotated[str, StringConstraints(pattern=r"^\w+$")]]
UserMetadataValue = Union[StrictBool, StrictInt, StrictFloat, StrictStr]


class TypeEnum(str, enum.Enum):
    INPUT = "input"
    STATE = "state"
    OUTPUT = "output"


class ExtractEnum(str, enum.Enum):
    MANDATORY_SINGLE = "mandatory_single"
    MANDATORY_MULTIPLE = "mandatory_multiple"
    OPTIONAL_SINGLE = "optional_single"
    OPTIONAL_MULTIPLE = "optional_multiple"


class Mapping(Model):
    description: Optional[str] = Field(None, description="Optional description")
    type: TypeEnum = Field(
        ...,
        description="Type of the model variable, e.g. input, state or model output. "
        "The classification depends of the relation of the time series to the model "
        "mechanics. Inputs stay unchanged of a model components. State are internal states "
        "of a model component, e.g. the water level of a reservoir. Outputs are "
        "are derived values from inputs and states.",
    )
    variable: str = Field(..., description="Name of the model variable")
    path: str = Field(
        ..., description="Path of the model variable in the model time series store"
    )


class TimeSeriesMapping(Model):
    """Attributes to identify a specific time series

    Leaving the the dispatch_info or ensemble_member properties unset means
    that the model adapter provides the missing information. Model Adapters may
    also ignore properties if they are irrelevant. For example, a model task
    may define a dispatch_info which would take precedence over the
    dispatch_info defined here when writing output.
    """

    store_id: Optional[str] = None
    path: str = Field(..., description="Path identifying the time series")
    t0: Optional[datetime] = None
    dispatch_info: Optional[str] = None
    ensemble_member: Optional[str] = None


class ElementMapping(Model):
    """Element attribute

    Very similar to the concept in the config store, but the UID is already defined"""

    attribute: str = Field(..., description="Attribute of an element in the adapter")
    attribute_index: Optional[int] = Field(
        None,
        description="Specific index of an attribute in the adapter, if it is an array",
    )


class DataMapping(Model):
    """Associate an element mapping with a time series mapping"""

    time_series: TimeSeriesMapping
    element: ElementMapping


class BaseElement(Model):
    domain: Optional[str] = None
    element_class: Optional[str] = None
    uid: str = Field(..., pattern="^[a-zA-Z]\\w*$", description="Unique identifier")
    rank: Optional[int] = Field(
        0,
        description="Optional rank to define the order of a flow reach, "
        "nesting for visualization, sequential execution order etc.",
    )
    display_name: Optional[str] = Field(
        None, description="String for labeling an element in a GUI"
    )
    created: Optional[datetime] = Field(
        None, description="Timestamp element was added to the network"
    )
    deleted: Optional[datetime] = Field(
        None, description="Timestamp element was removed from the network"
    )
    group_uid: Optional[str] = Field(
        None, description="UID of group to which link belongs"
    )
    user_metadata: Optional[Dict[UserMetadataKey, UserMetadataValue]] = Field(
        None, description="Optional dictionary of user-provided key-value pairs"
    )
    time_series_mappings: Optional[List[DataMapping]] = Field(
        None, description="List of timeseries mappings"
    )
    mapping: Optional[List[Mapping]] = Field(
        None, description="Time series mapping of model inputs, states and outputs"
    )

    @model_validator(mode="before")
    @classmethod
    def default_schematic_location(cls, data: Any) -> Any:
        if isinstance(data, dict) and data.get("display_name") is None:
            data["display_name"] = data.get("uid")
        return data


class Location(Model):
    x: float
    y: float
    z: float = 0.0


class LocationSet(str, enum.Enum):
    GEOGRAPHIC = "location"
    SCHEMATIC = "schematic_location"


class LocationExtent(BaseModel):
    """Mapping of dimensions to range, e.g. {"x": [-10, 10]}"""

    x: Optional[Tuple[float, float]] = None
    y: Optional[Tuple[float, float]] = None
    z: Optional[Tuple[float, float]] = None


class BaseLink(BaseElement):
    collection: Literal["links"] = "links"
    source_uid: str = Field(..., description="UID of source node")
    target_uid: str = Field(..., description="UID of target node")
    vertices: Optional[List[Location]] = Field(
        None,
        description="Additional geographical points refining the path"
        " from source to target nodes",
    )
    schematic_vertices: Optional[List[Location]] = Field(
        None,
        description="Additional schematic points refining the path"
        " from source to target nodes",
    )


class _Node(BaseElement):
    location: Location = Field(..., description="Geographical location")
    schematic_location: Optional[Location] = Field(
        None, description="Schematic location. Takes value of 'location' if unset."
    )

    @model_validator(mode="before")
    @classmethod
    def default_schematic_location(cls, data: Any) -> Any:
        if isinstance(data, dict) and data.get("schematic_location") is None:
            data["schematic_location"] = data.get("location")
        return data


class BaseControl(BaseElement):
    collection: Literal["controls"] = "controls"


class BaseNode(_Node):
    collection: Literal["nodes"] = "nodes"


class BaseGroup(_Node):
    collection: Literal["groups"] = "groups"
