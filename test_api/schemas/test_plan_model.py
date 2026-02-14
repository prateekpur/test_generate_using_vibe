from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TestCaseModel(BaseModel):
    test_name: str
    description: str

    method: str
    path: str

    headers: Dict[str, str] = Field(default_factory=dict)
    query_params: Dict[str, Any] = Field(default_factory=dict)
    path_params: Dict[str, Any] = Field(default_factory=dict)

    body: Optional[Dict[str, Any]]

    expected_status: int

    expected_response_contains: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "forbid"


class TestPlanModel(BaseModel):
    endpoint: str
    method: str
    test_cases: List[TestCaseModel]

    class Config:
        extra = "forbid"
