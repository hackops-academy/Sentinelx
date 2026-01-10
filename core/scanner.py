import subprocess
import re
from config import TOOLS

class Scanner:
    def __init__(self, scan_id, target):
        self.scan_id = scan_id
        self.target = target
        self.results = {}
        self.status = "Queued"
        self.progress = 0
        self.current_tool = ""
        self.completed = False

    def clean_output(self, text):
        """Removes ANSI color codes from terminal output for Web Display"""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def run_command(self, command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300 # 5 min timeout per tool
            )
            output = result.stdout if result.stdout else result.stderr
            return self.clean_output(output)
        except subprocess.TimeoutExpired:
            return "Error: Tool execution timed out."
        except Exception as e:
            return str(e)

    def run_full_scan(self):
        self.status = "Scanning"
        
        # 1. Nmap (Fast Scan)
        self.current_tool = "Nmap"
        self.progress = 10
        if TOOLS["nmap"]:
            # -F for fast mode, --unprivileged for Termux compatibility
            cmd = f"{TOOLS['nmap']} -F --unprivileged {self.target}" 
            self.results["Nmap"] = self.run_command(cmd)
        
        # 2. WhatWeb
        self.current_tool = "WhatWeb"
        self.progress = 40
        if TOOLS["whatweb"]:
            cmd = f"{TOOLS['whatweb']} {self.target}"
            self.results["WhatWeb"] = self.run_command(cmd)

        # 3. Nikto
        self.current_tool = "Nikto"
        self.progress = 70
        if TOOLS["nikto"]:
            cmd = f"{TOOLS['nikto']} -h {self.target} -Tuning 1" # Tuning 1 is faster
            self.results["Nikto"] = self.run_command(cmd)

        self.progress = 100
        self.status = "Completed"
        self.completed = True
