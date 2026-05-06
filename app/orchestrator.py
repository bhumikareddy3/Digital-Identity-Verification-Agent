import asyncio
import logging
from typing import Dict, Any

from app.ocr import extract_text
from app.validation import extract_fields, validate
from app.fraud import fraud_score
from app.rag import compliance_check

logging.basicConfig(level=logging.INFO)


class PipelineError(Exception):
    pass


async def run_ocr(image_path: str) -> str:
    try:
        logging.info("Running OCR...")
        return extract_text(image_path)
    except Exception as e:
        raise PipelineError(f"OCR failed: {e}")


async def run_validation(text: str) -> Dict[str, Any]:
    try:
        logging.info("Extracting & validating fields...")
        fields = extract_fields(text)
        validation_result = validate(fields)
        return {"fields": fields, "validation": validation_result}
    except Exception as e:
        raise PipelineError(f"Validation failed: {e}")


async def run_fraud(fields: Dict[str, Any]) -> float:
    try:
        logging.info("Running fraud detection...")
        return fraud_score(fields)
    except Exception as e:
        raise PipelineError(f"Fraud detection failed: {e}")


async def run_compliance(fields: Dict[str, Any]) -> Dict[str, Any]:
    try:
        logging.info("Running compliance check (RAG)...")
        return compliance_check(str(fields))
    except Exception as e:
        raise PipelineError(f"Compliance check failed: {e}")


def make_final_decision(validation, fraud, compliance):
    score = 0

    if validation.get("valid"):
        score += 0.4
    if fraud < 0.5:
        score += 0.3
    if compliance.get("compliant"):
        score += 0.3

    decision = "APPROVED" if score >= 0.7 else "REJECTED"

    return {
        "decision": decision,
        "confidence": round(score, 2)
    }


async def run_pipeline(image_path: str) -> Dict[str, Any]:
    try:
        # Step 1: OCR
        text = await run_ocr(image_path)

        # Step 2: Validation
        val_result = await run_validation(text)
        fields = val_result["fields"]

        # Step 3: Run fraud & compliance in parallel
        fraud_task = asyncio.create_task(run_fraud(fields))
        compliance_task = asyncio.create_task(run_compliance(fields))

        fraud_result, compliance_result = await asyncio.gather(
            fraud_task, compliance_task
        )

        # Step 4: Final decision
        decision = make_final_decision(
            val_result["validation"],
            fraud_result,
            compliance_result
        )

        return {
            "fields": fields,
            "validation": val_result["validation"],
            "fraud_score": fraud_result,
            "compliance": compliance_result,
            "final_decision": decision
        }

    except PipelineError as pe:
        logging.error(pe)
        return {"error": str(pe)}

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"error": "Internal pipeline failure"}