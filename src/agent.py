import json
import sys
from pathlib import Path

from synapx.claims_agent import ClaimsAgent


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/agent.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        fallback_path = Path(__file__).resolve().parents[1] / "data" / "input" / pdf_path
        if fallback_path.exists():
            pdf_path = fallback_path
        else:
            print(f"File not found: {pdf_path}")
            sys.exit(1)

    print(f"Processing {pdf_path}...")

    agent = ClaimsAgent()
    try:
        result = agent.process_file(pdf_path)
    except Exception as error:
        print(f"Failed to process PDF: {error}")
        sys.exit(1)

    print("\n--- Analysis Result ---")
    print(json.dumps(result.model_dump(), indent=2))

    output_dir = Path(__file__).resolve().parents[1] / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "output.json"
    output_path.write_text(json.dumps(result.model_dump(), indent=2), encoding="utf-8")

    print(f"\nSaved output to {output_path}")


if __name__ == "__main__":
    main()
