import re
import json

def mask_half_sensitive_info(match):
    match_str = match.group(0)
    half_length = len(match_str) // 2
    return match_str[:half_length] + '****'

def mask_sensitive_info(log_message):
    sensitive_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        r'\b\d{3}[-.\s]??\d{2}[-.\s]??\d{4}\b',
        r'\b\d{4}[-.\s]??\d{4}[-.\s]??\d{4}[-.\s]??\d{4}\b',
        r'\b\d{10}\b',
        r'\b\d{6,10}\b',
        r'\b[A-Z][a-z]*\b',
        r'\b[A-Z][a-z]*\b',
    ]
    
    for pattern in sensitive_patterns:
        log_message = re.sub(pattern, mask_half_sensitive_info, log_message)
    
    return log_message

def mask_sensitive_info_in_json(log_json):
    try:
        log_data = json.loads(log_json)
        masked_log_data = {key: mask_sensitive_info(str(value)) for key, value in log_data.items()}
        return json.dumps(masked_log_data)
    except json.JSONDecodeError:
        return log_json

def sensitive_info_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            try:
                json.loads(result)
                result = mask_sensitive_info_in_json(result)
            except json.JSONDecodeError:
                result = mask_sensitive_info(result)
        return result
    return wrapper