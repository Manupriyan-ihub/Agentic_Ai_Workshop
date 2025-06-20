import re 

# Extract score from the result text
def extract_score_from_json(json_data):
    result_text = json_data.get("result", "")
    
    # Pattern to match number/100
    pattern = r'\b(\d+(?:\.\d+)?)/100\b'
    match = re.search(pattern, result_text)
    
    if match:
        return float(match.group(1))
    else:
        return None
