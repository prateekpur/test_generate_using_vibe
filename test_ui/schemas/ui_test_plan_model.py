from typing import List, Optional, Literal
from pydantic import BaseModel, Field


ActionType = Literal[
    "goto",
    "click",
    "fill",
    "press",
    "expect_text",
    "expect_title_contains",
    "expect_url_contains",
    "wait_for_selector",
]


class UITestStepModel(BaseModel):
    action: ActionType
    selector: Optional[str] = None
    value: Optional[str] = None
    expected: Optional[str] = None
    timeout_ms: int = Field(default=5000, ge=100, le=120000)

    class Config:
        extra = "forbid"


class UITestCaseModel(BaseModel):
    test_name: str
    description: str
    path: str = "/"
    steps: List[UITestStepModel]

    class Config:
        extra = "forbid"


class UITestPlanModel(BaseModel):
    app_name: str = "web_app"
    test_cases: List[UITestCaseModel]

    class Config:
        extra = "forbid"
