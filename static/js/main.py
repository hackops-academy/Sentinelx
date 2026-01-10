function startScan() {
    const target = document.getElementById("target").value;
    const statusPanel = document.getElementById("status-panel");
    const statusText = document.getElementById("status-text");
    const toolText = document.getElementById("tool-text");
    const fill = document.getElementById("progress-fill");

    if(!target) { alert("ENTER TARGET"); return; }

    statusPanel.classList.remove("hidden");
    statusText.innerText = "INITIALIZING";

    // Start Scan
    fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `target=${encodeURIComponent(target)}`
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === "error") {
            alert(data.message);
            return;
        }
        pollStatus(data.scan_id);
    });
}

function pollStatus(scanId) {
    const interval = setInterval(() => {
        fetch(`/status/${scanId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("status-text").innerText = data.status.toUpperCase();
            document.getElementById("tool-text").innerText = data.current_tool.toUpperCase();
            document.getElementById("progress-fill").style.width = data.progress + "%";

            if(data.completed) {
                clearInterval(interval);
                window.location.href = `/result/${scanId}`;
            }
        });
    }, 2000); // Check every 2 seconds
}
