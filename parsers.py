def parse_tally_payload(data: dict) -> dict:
    fields = data.get("data", {}).get("fields", [])
    
    parsed = {}
    
    for field in fields:
        label = field.get("label", "").lower().replace(" ", "_")
        value = field.get("value", "")
        
        if "email" in label:
            parsed["email"] = value
        elif "name" in label:
            parsed["name"] = value
        elif "message" in label or "comment" in label:
            parsed["message"] = value
        elif label.startswith("utm_"):
            parsed[label] = value
    
    parsed["source_tag"] = "tally"
    
    return parsed