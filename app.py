import uuid
import threading
from flask import Flask, render_template, request, jsonify, redirect, url_for
from config import MISSING_TOOLS
from core.scanner import Scanner
from utils.validator import validate_target

app = Flask(__name__)

# In-memory storage for active scans (In production, use a database like SQLite/Redis)
active_scans = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        target = request.form.get("target")
        
        if not validate_target(target):
            return jsonify({"status": "error", "message": "Invalid Target URL or IP"}), 400

        if MISSING_TOOLS:
            return jsonify({"status": "error", "message": f"Missing tools: {', '.join(MISSING_TOOLS)}"}), 500

        # Generate unique Scan ID
        scan_id = str(uuid.uuid4())
        
        # Initialize Scanner Object
        scanner = Scanner(scan_id, target)
        active_scans[scan_id] = scanner

        # Start scan in a background thread
        scan_thread = threading.Thread(target=scanner.run_full_scan)
        scan_thread.daemon = True
        scan_thread.start()

        return jsonify({"status": "success", "scan_id": scan_id})

    return render_template("index.html", missing=MISSING_TOOLS)

@app.route("/status/<scan_id>")
def status(scan_id):
    """API to poll scan progress"""
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
