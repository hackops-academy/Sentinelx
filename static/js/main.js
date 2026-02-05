/* SENTINELX MAIN CONTROLLER 
    Handles interaction between the Cyber UI and Flask Backend
*/

// Main function triggered by the INITIATE_SCAN button
function startScan() {
    const targetInput = document.getElementById('target');
    const target = targetInput.value.trim();
    
    // UI Elements
    const statusPanel = document.getElementById('status-panel');
    const btnText = document.querySelector('.btn-text');
    const toolText = document.getElementById('tool-text');
    const statusText = document.getElementById('status-text');
    const progressBar = document.getElementById('progress-fill');

    // 1. Validation
    if (!target) {
        alert(">> ERROR: TARGET_IDENTIFIER_EMPTY");
        return;
    }

    // 2. Prepare UI (Lock interface)
    statusPanel.classList.remove('hidden');
    btnText.innerText = "SCAN_INITIATED...";
    document.querySelector('.cyber-btn').disabled = true;

    // 3. Send Request to Flask
    // We use FormData because app.py uses request.form.get("target")
    const formData = new FormData();
    formData.append('target', target);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "error") {
            throw new Error(data.message);
        }
        
        // Success: Start polling for status
        console.log("Scan started with ID:", data.scan_id);
        pollStatus(data.scan_id);
    })
    .catch(error => {
        console.error("Error:", error);
        alert(`>> SYSTEM FAILURE: ${error.message}`);
        resetUI();
    });
}

// Function to check scan progress every 1 second
function pollStatus(scanId) {
    const toolText = document.getElementById('tool-text');
    const statusText = document.getElementById('status-text');
    const progressBar = document.getElementById('progress-fill');

    const intervalId = setInterval(() => {
        fetch(`/status/${scanId}`)
        .then(response => response.json())
        .then(data => {
            
            // Update the Cyber UI
            progressBar.style.width = data.progress + "%";
            toolText.innerText = (data.current_tool || "INITIALIZING").toUpperCase();
            statusText.innerText = (data.status || "RUNNING").toUpperCase();

            // Check if complete
            if (data.completed) {
                clearInterval(intervalId);
                statusText.innerText = "COMPLETED";
                statusText.style.color = "#00ff00"; // Green
                
                // Small delay before redirect for effect
                setTimeout(() => {
                    window.location.href = `/result/${scanId}`;
                }, 1000);
            }
        })
        .catch(error => {
            console.error("Polling Error:", error);
            // Don't stop polling on single network glitch, but maybe log it
        });
    }, 1000); // Poll every 1000ms (1 second)
}

// Helper to reset UI if scan fails to start
function resetUI() {
    const statusPanel = document.getElementById('status-panel');
    const btnText = document.querySelector('.btn-text');
    
    statusPanel.classList.add('hidden');
    btnText.innerText = "INITIATE_SCAN";
    document.querySelector('.cyber-btn').disabled = false;
}

// Add 'Enter' key support for the input box
document.getElementById('target').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        startScan();
    }
});
                                                
