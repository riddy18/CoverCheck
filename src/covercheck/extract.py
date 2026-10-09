import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from covercheck.schemas import PolicyExtraction

MODEL = os.environ.get("COVERCHECK_MODEL", "gemini-3.8-flash")

PROMPT = """You extract coverage criteria from Medicare coverage policies.
Use only what the policy text states. For each criterion, include a short
verbatim quote from the policy that supports it. Copy quotes exactly,
character for character; do not paraphrase or merge sentences.

<policy>
{text}
</policy>"""


def extract(text: str, client: genai.Client | None = None) -> PolicyExtraction:
    client = client or genai.Client()
    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT.format(text=text),
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=PolicyExtraction,
        ),
    )
    return PolicyExtraction.model_validate_json(response.text)


def main() -> None:
    load_dotenv()
    text = Path(sys.argv[1]).read_text()
    print(extract(text).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
