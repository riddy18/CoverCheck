from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from covercheck.extract import extract
from covercheck.schemas import Criterion, PolicyExtraction

SAMPLE = PolicyExtraction(
    policy_title="Test Policy",
    covered_services=["MRI lumbar spine"],
    criteria=[
        Criterion(
            description="6 weeks of conservative therapy",
            category="prior_treatment",
            source_quote="after 6 weeks of conservative treatment",
        )
    ],
    exclusions=[],
)


class FakeClient:
    def __init__(self):
        self.messages = SimpleNamespace(
            parse=lambda **kwargs: SimpleNamespace(parsed_output=SAMPLE)
        )


def test_extract_returns_schema():
    result = extract("policy text", client=FakeClient())
    assert result.criteria[0].category == "prior_treatment"


def test_invalid_category_rejected():
    with pytest.raises(ValidationError):
        Criterion(description="x", category="vibes", source_quote="y")
