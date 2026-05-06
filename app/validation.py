import re

def extract_fields(text):
    return {
        "aadhaar": re.findall(r"\d{4}\s\d{4}\s\d{4}", text),
        "pan": re.findall(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
    }

def validate(data):
    return {
        "aadhaar_valid": len(data["aadhaar"]) > 0,
        "pan_valid": len(data["pan"]) > 0
    }
