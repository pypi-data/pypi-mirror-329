from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MatcherType(str, Enum):
    NONE = "NONE"
    KEY_TO_KEY = "KEY_TO_KEY"
    KEY_TO_VALUE = "KEY_TO_VALUE"
    QUERY_TO_VALUE = "QUERY_TO_VALUE"


class Matcher(BaseModel):
    matcher_type: MatcherType
    key: str
    value: str


class Mock(BaseModel):
    name: str
    url: str
    method: str
    status_code: int
    body: Optional[str] = None
    body_patterns: Optional[str] = None
    matcher_type: Optional[MatcherType] = None
