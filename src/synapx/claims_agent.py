import json
from pathlib import Path
from typing import Final, Union

from .llm import OpenRouterClient
from .pdf import extract_text_from_pdf
from .schema import AgentOutput

MOCK_RESPONSE: Final[dict] = {
    "extractedFields": {
        "policy_info": {
            "policy_number": "54-235667",
            "policyholder_name": "John Doe",
            "effective_date": "2016-01-01",
            "expiration_date": "2017-01-01",
        },
        "incident_info": {
            "date": "2016-12-05",
            "time": "08:30 AM",
            "location": "Main St & 5th Ave, New York, NY",
            "description": "Rear-ended by another vehicle while stopped at a red light. No injuries reported.",
        },
        "involved_parties": [
            {"name": "John Doe", "role": "Driver", "contact_info": "555-0101"},
            {"name": "Jane Smith", "role": "Other Driver", "contact_info": "555-0102"},
        ],
        "asset_details": [
            {"asset_type": "Vehicle", "asset_id": "VIN1234567890", "estimated_damage": "1500.00"}
        ],
        "claim_type": "Collision",
        "initial_estimate": 1500.0,
    },
    "recommendedRoute": "Fast-track",
    "reasoning": "Estimated damage ($1,500) is well below the $25,000 threshold. No injuries or fraud indicators found.",
}

SYSTEM_PROMPT: Final[str] = """
You are an expert insurance claims agent.
Extract data from the following FNOL (First Notice of Loss) text into JSON.

Routing Rules:
1. If estimated damage < $25,000 -> \"Fast-track\"
2. If any mandatory field (Policy Number, Date, Description) is missing -> \"Manual review\"
3. If description contains words like \"fraud\", \"inconsistent\", \"staged\" -> \"Investigation Flag\"
4. If claim type = \"injury\" or injuries mentioned -> \"Specialist Queue\"

Return ONLY valid JSON with the following structure:
{
  "extractedFields": {
    "policy_info": { "policy_number": null, "policyholder_name": null, "effective_date": null, "expiration_date": null },
    "incident_info": { "date": null, "time": null, "location": null, "description": null },
    "involved_parties": [{ "name": null, "role": null, "contact_info": null }],
    "asset_details": [{ "asset_type": null, "asset_id": null, "estimated_damage": null }],
    "claim_type": null,
    "initial_estimate": null
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Explain your routing decision here"
}
"""


class ClaimsAgent:
    def __init__(self) -> None:
        self.client = OpenRouterClient()
        self.mode = "openrouter" if self.client.is_available else "mock"

        if self.mode == "openrouter":
            print(f"Connected to OpenRouter using model {self.client.model_name}")
        else:
            print("WARNING: Valid OpenRouter API Key not found. Running in MOCK mode.")

    def build_prompt(self, raw_text: str) -> str:
        return f"{SYSTEM_PROMPT}\n\nFNOL Text:\n{raw_text[:8000]}"

    def analyze_claim(self, raw_text: str) -> AgentOutput:
        if not raw_text.strip():
            raise ValueError("Empty text cannot be analyzed.")

        if self.mode == "mock":
            return AgentOutput(**MOCK_RESPONSE)

        try:
            content = self.client.request(self.build_prompt(raw_text))
            return AgentOutput.model_validate_json(content)
        except Exception as error:
            print(f"Error calling LLM (OpenRouter): {error}")
            print("Falling back to mock data for stability.")
            return AgentOutput(**MOCK_RESPONSE)

    def process_file(self, pdf_path: Union[str, Path]) -> AgentOutput:
        raw_text = extract_text_from_pdf(pdf_path)
        if not raw_text.strip():
            raise RuntimeError("No text extracted. PDF may be scanned or image-only.")
        return self.analyze_claim(raw_text)
