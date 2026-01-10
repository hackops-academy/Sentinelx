import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCAN_DIR = os.path.join(BASE_DIR, "scans")
os.makedirs(SCAN_DIR, exist_ok=True)

# Helper to find tools in System PATH (works for Kali /bin and Termux /data/.../bin)
def get_tool_path(tool_name):
    path = shutil.which(tool_name)
    return path if path else None

# Dynamic Tool Configuration
TOOLS = {
    "whatweb": get_tool_path("whatweb"),
    "nikto": get_tool_path("nikto"),
    "nmap": get_tool_path("nmap"), # Added Nmap for advanced scanning
}

# Check if tools are missing
MISSING_TOOLS = [name for name, path in TOOLS.items() if path is None]
