from typing import TypedDict, List, Dict, Any, Optional


class TestCase(TypedDict):
    test_name: str
    description: str

    method: str
    path: str

    headers: Dict[str, str]
    query_params: Dict[str, Any]
    path_params: Dict[str, Any]

    body: Optional[Dict[str, Any]]

    expected_status: int

    expected_response_contains: Dict[str, Any]


class TestPlan(TypedDict):
    endpoint: str
    method: str
    test_cases: List[TestCase]
