import json
import csv
import time
from pathlib import Path

from yal_agent.classifier import classify


# Find the project root regardless of where the script is launched.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "intent_test_cases.jsonl"
RESULTS_DIR = PROJECT_ROOT / "results"
PREDICTIONS_FILE = RESULTS_DIR / "predictions.csv"
SUMMARY_FILE = RESULTS_DIR / "baseline_report.json"


def load_test_cases():
    cases = []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                case = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            if "text" not in case or "expected_intent" not in case:
                raise ValueError(
                    f"Line {line_number} needs text and expected_intent."
                )

            cases.append(case)

    return cases


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cases = load_test_cases()

    if not cases:
        print("No test cases found.")
        return

    rows = []
    correct = 0
    errors = 0
    total_latency_ms = 0
    total_input_tokens = 0
    total_output_tokens = 0

    print(f"Running {len(cases)} test cases...")
    print("This may take a few minutes.\n")

    for index, case in enumerate(cases, start=1):
        start = time.perf_counter()

        try:
            output = classify(case["text"])
            result = output.get("result", {})
            predicted = result.get("intent", "UNKNOWN")
            error = output.get("error")
            latency_ms = output.get("latency_ms", 0) or 0
            input_tokens = output.get("input_tokens", 0) or 0
            output_tokens = output.get("output_tokens", 0) or 0

        except Exception as exc:
            predicted = "UNKNOWN"
            error = f"{type(exc).__name__}: {exc}"
            latency_ms = int((time.perf_counter() - start) * 1000)
            input_tokens = 0
            output_tokens = 0
            result = {}

        expected = case["expected_intent"]
        is_correct = predicted == expected and error is None

        if is_correct:
            correct += 1

        if error is not None:
            errors += 1

        total_latency_ms += latency_ms
        total_input_tokens += input_tokens
        total_output_tokens += output_tokens

        rows.append({
            "text": case["text"],
            "expected_intent": expected,
            "predicted_intent": predicted,
            "correct": is_correct,
            "confidence": result.get("confidence", ""),
            "needs_clarification": result.get("needs_clarification", ""),
            "error": error or "",
            "latency_ms": latency_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        })

        status = "PASS" if is_correct else "CHECK"
        print(f"[{index}/{len(cases)}] {status}: {expected} -> {predicted}")

    # Save individual predictions for later inspection.
    with PREDICTIONS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    successful_calls = len(cases) - errors
    accuracy = correct / len(cases)
    average_latency_ms = total_latency_ms / len(cases)

    report = {
        "total_cases": len(cases),
        "correct_predictions": correct,
        "accuracy": round(accuracy, 4),
        "accuracy_percent": round(accuracy * 100, 2),
        "api_or_processing_errors": errors,
        "successful_calls": successful_calls,
        "average_latency_ms": round(average_latency_ms, 2),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "cost": 0.0,
        "note": (
            "Cost is recorded as zero because provider pricing is not configured. "
            "This does not prove the service is free."
        ),
    }

    with SUMMARY_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print("\n--- BASELINE REPORT ---")
    print(json.dumps(report, indent=2))
    print(f"\nPredictions saved to: {PREDICTIONS_FILE}")
    print(f"Summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
