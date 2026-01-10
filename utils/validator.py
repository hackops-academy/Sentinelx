import re
from urllib.parse import urlparse

def validate_target(target):
    if not target:
        return False
        
    # Remove http/https to check domain/ip structure
    target_clean = target.replace("https://", "").replace("http://", "").split("/")[0]
    
    # Regex for Domain or IP
    regex = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"
    
    return re.match(regex, target_clean) is not None
