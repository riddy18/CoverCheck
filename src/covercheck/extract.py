import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from covercheck.schemas import PolicyExtraction

MODEL = "claude-sonnet-5-5"

PROMPT = """You extract coverage criteria from Medicare coverage policies.
Use only what the policy text states. For each criterion, include a short
verbatim quote from the policy that supports it.

<policy>
{text}
</policy>"""


def extract(text: str, client: Anthropic | None = None) -> PolicyExtraction:
    client = client or Anthropic()
    response = client.messages.parse(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": PROMPT.format(text=text)}],
        output_format=PolicyExtraction,
    )
    return response.parsed_output


def main() -> None:
    load_dotenv()
    text = Path(sys.argv[1]).read_text()
    print(extract(text).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
