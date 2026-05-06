from app.ocr import extract_text
from app.validation import extract_fields, validate
from app.fraud import fraud_score
from app.rag import compliance_check

def run_pipeline(image_path):
    text = extract_text(image_path)
    fields = extract_fields(text)

    return {
        "fields": fields,
        "validation": validate(fields),
        "fraud_score": fraud_score(fields),
        "compliance": compliance_check(str(fields))
    }
