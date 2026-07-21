from pathlib import Path


DOCUMENT_TYPES = {

    "method": "Method Statement",
    "sop": "SOP",
    "procedure": "Procedure",
    "specification": "Specification",
    "spec": "Specification",
    "drawing": "Drawing",
    "inspection": "Inspection Report",
    "test": "Test Report",
    "commissioning": "Commissioning",
    "rfi": "RFI",
    "runbook": "Runbook",
    "manual": "Manual",
}


DISCIPLINES = {

    "electrical": "Electrical",
    "hvac": "HVAC",
    "mechanical": "Mechanical",
    "civil": "Civil",
    "network": "Network",
    "fire": "Fire Protection",
    "security": "Security",
    "ups": "Electrical",
    "generator": "Electrical",
    "cooling": "HVAC",
}


def classify_document(filename: str):

    name = Path(filename).stem.lower()

    document_type = "General"

    discipline = "General"

    for key, value in DOCUMENT_TYPES.items():

        if key in name:
            document_type = value
            break

    for key, value in DISCIPLINES.items():

        if key in name:
            discipline = value
            break

    return {

        "document_type": document_type,

        "discipline": discipline,

        "project": "AI EPC Data Center"

    }