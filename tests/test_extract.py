from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from covercheck.extract import MODEL, extract
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
SAMPLE_JSON = SAMPLE.model_dump_json()


class FakeModels:
    def __init__(self, text):
        self.text = text
        self.kwargs = None

    def generate_content(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(text=self.text)


class FakeClient:
    def __init__(self, text=SAMPLE_JSON):
        self.models = FakeModels(text)


def test_extract_returns_schema():
    result = extract("policy text", client=FakeClient())
    assert result.criteria[0].category == "prior_treatment"


def test_extract_requests_structured_output():
    client = FakeClient()
    extract("policy text", client=client)
    assert client.models.kwargs["model"] == MODEL
    assert client.models.kwargs["config"].response_schema is PolicyExtraction
    assert "policy text" in client.models.kwargs["contents"]


def test_malformed_response_raises():
    with pytest.raises(ValidationError):
        extract("policy text", client=FakeClient(text='{"policy_title": "x"}'))


def test_invalid_category_rejected():
    with pytest.raises(ValidationError):
        Criterion(description="x", category="vibes", source_quote="y")
