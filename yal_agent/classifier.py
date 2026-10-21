from pydantic import ValidationError

from . import config
from .guards import InputRejected, check_input
from .llm_client import call_llm
from .schemas import Intent, IntentResult


def classify(text, model: str | None = None) -> dict:
    out = {
        "input": text if isinstance(text, str) else repr(text),
        "result": None,
        "error": None,
        "model": model or config.MODEL,
        "latency_ms": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cost": 0.0,
    }

    # 1. Input guard
    try:
        cleaned = check_input(text)
    except InputRejected as e:
        out["error"] = f"input_rejected:{e}"
        out["result"] = _safe_unknown(
            "Input rejected before model call."
        )
        return out

    # 2. Call model
    try:
        resp = call_llm(cleaned, model)
    except Exception as e:
        out["error"] = (
            f"api_error:{type(e).__name__}:{str(e)[:150]}"
        )
        out["result"] = _safe_unknown(
            "Model call failed."
        )
        return out

    out.update({
        k: resp[k]
        for k in (
            "latency_ms",
            "input_tokens",
            "output_tokens",
            "cost",
            "model",
        )
    })

    # 3. Validate structured output
    try:
        result = IntentResult(**resp["raw"])
    except ValidationError:
        out["error"] = "schema_validation_failed"
        out["result"] = _safe_unknown(
            "Model output failed validation."
        )
        return out

    # 4. Low confidence → clarification
    if result.confidence < config.CONFIDENCE_THRESHOLD:
        result.needs_clarification = True

    out["result"] = result.model_dump(mode="json")

    return out


def _safe_unknown(reason: str) -> dict:
    return IntentResult(
        intent=Intent.UNKNOWN,
        confidence=0.0,
        needs_clarification=True,
        clarification_question=(
            "Could you please rephrase your request?"
        ),
        rationale=reason,
    ).model_dump(mode="json")