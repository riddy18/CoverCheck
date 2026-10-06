from typing import Literal
from pydantic import BaseModel


class Criterion(BaseModel):
    description: str
    category: Literal["diagnosis", "prior_treatment", "duration", "documentation", "other"]
    source_quote: str


class PolicyExtraction(BaseModel):
    policy_title: str
    covered_services: list[str]
    criteria: list[Criterion]
    exclusions: list[str]
