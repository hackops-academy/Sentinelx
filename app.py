import uuid
import threading
import os
import sys
import time
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from config import MISSING_TOOLS, TOOLS
from core.scanner import Scanner
from utils.validator import validate_target

# --- FLASK CONFIGURATION ---
# We disable the default Flask banner to keep our custom CLI cool
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)

# Suppress standard logging to keep terminal clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# In-memory storage for active scans
active_scans = {}

# --- TERMINAL UI COLORS ---
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# --- ROUTE LOGIC (SAME AS BEFORE) ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        target = request.form.get("target")
        
        if not validate_target(target):
            return jsonify({"status": "error", "message": "Invalid Target URL or IP"}), 400

        if MISSING_TOOLS:
            return jsonify({"status": "error", "message": f"Missing tools: {', '.join(MISSING_TOOLS)}"}), 500

        scan_id = str(uuid.uuid4())
        scanner = Scanner(scan_id, target)
        active_scans[scan_id] = scanner

        scan_thread = threading.Thread(target=scanner.run_full_scan)
        scan_thread.daemon = True
        scan_thread.start()

        return jsonify({"status": "success", "scan_id": scan_id})

    return render_template("index.html", missing=MISSING_TOOLS)

@app.route("/status/<scan_id>")
def status(scan_id):
    scanner = active_scans.get(scan_id)
    if not scanner:
        return jsonify({"error": "Scan not found"}), 404
    
    return jsonify({
        "progress": scanner.progress,
        "status": scanner.status,
        "current_tool": scanner.current_tool,
        "completed": scanner.completed
    })

@app.route("/result/<scan_id>")
def result(scan_id):
    scanner = active_scans.get(scan_id)
    if not scanner or not scanner.completed:
        return redirect(url_for('index'))
    return render_template("result.html", results=scanner.results, target=scanner.target)

# --- CLI LAUNCHER FUNCTIONS ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.CYAN}
   _____            __  _            __  __
  / ___/___  ____  / /_(_)___  ___  / /  / / __  __
  \__ \/ _ \/ __ \/ __/ / __ \/ _ \/ / / /   \/ /
 ___/ /  __/ / / / /_/ / / / /  __/ / / / /\   /
/____/\___/_/ /_/\__/_/_/ /_/\___/_/_/_/_/  \_/
                                       
        {Colors.GREEN}[ HACKOPS EDITION v2.0 ]{Colors.RESET}
    """
    print(banner)

def loading_effect(task):
    """Simulates a system check"""
    sys.stdout.write(f"{Colors.BOLD}[*] {task}{Colors.RESET}")
    sys.stdout.flush()
    time.sleep(0.5)
    sys.stdout.write(f"\r{Colors.GREEN}[+] {task} ... OK{Colors.RESET}\n")
    time.sleep(0.2)

def launcher():
    clear_screen()
    print_banner()
    
    print(f"\n{Colors.CYAN}--- SYSTEM INITIALIZATION ---{Colors.RESET}")
    loading_effect("Loading Core Modules")
    loading_effect("Checking Network Interface")
    
    # Check Tools
    if MISSING_TOOLS:
        print(f"{Colors.RED}[!] WARNING: Missing Tools: {', '.join(MISSING_TOOLS)}{Colors.RESET}")
        print(f"{Colors.YELLOW}    Some scans will be unavailable.{Colors.RESET}")
    else:
        loading_effect("Verifying External Tools (Nmap/Nikto)")

    print(f"\n{Colors.CYAN}--- CONTROL PANEL ---{Colors.RESET}")
    print(f"{Colors.GREEN}1.{Colors.RESET} Start Web Interface (Standard)")
    print(f"{Colors.GREEN}2.{Colors.RESET} Exit")
    
    choice = input(f"\n{Colors.BOLD}root@sentinelx:~# {Colors.RESET}")

    if choice == '1':
        print(f"\n{Colors.GREEN}[+] Starting Server on http://127.0.0.1:5000{Colors.RESET}")
        print(f"{Colors.YELLOW}[i] Press CTRL+C to stop.{Colors.RESET}")
        print("-" * 40)
        # We run the app directly now
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        print(f"\n{Colors.RED}[!] System Shutdown.{Colors.RESET}")
        sys.exit()

if __name__ == "__main__":
    try:
        launcher()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Force Shutdown Initiated.{Colors.RESET}")
    
