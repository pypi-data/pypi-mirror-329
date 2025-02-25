from typing import Optional, List, Dict
from collections import defaultdict
from enum import Enum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Any, Dict


class ParameterType(str, Enum):
    """ParameterType determines the data type of a parameter."""

    # STRING indicates the parameter accepts string/text values.
    STRING: str = "string"


class BodyEncoding(str, Enum):
    """BodyEncoding determines how the HTTP body will be encoded."""

    # FORM indicates the body will be encoded using URL encoding.
    FORM: str = "application/x-www-form-urlencoded"

    # JSON indicates the body will be encoded as JSON.
    JSON: str = "application/json"


@dataclass_json
@dataclass
class ParameterOption:
    value: str
    text: str


@dataclass_json
@dataclass(frozen=True)
class ToolParameter:
    name: str
    description: str
    type: ParameterType
    required: Optional[bool] = False
    options: Optional[List[ParameterOption]] = field(default_factory=lambda: [])


@dataclass_json
@dataclass(frozen=True)
class ToolWebhookConfiguration:
    name: str


@dataclass_json
@dataclass(frozen=True)
class ActionHTTPBodyDefinition:
    encoding: BodyEncoding
    json_template: Optional[str] = ""
    form_field_templates: Optional[Dict[str, str]] = field(
        default_factory=lambda: defaultdict(dict)
    )


@dataclass_json
@dataclass(frozen=True)
class ActionHTTPDefinition:
    method: str
    url_template: str
    header_templates: Optional[Dict[str, str]] = None
    body: Optional[ActionHTTPBodyDefinition] = None


@dataclass_json
@dataclass(frozen=True)
class Tool:
    id: str
    name: str
    description: str
    parameters: List[ToolParameter] = field(default_factory=lambda: [])
    webhook: Optional[ToolWebhookConfiguration] = None
