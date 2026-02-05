<div align="center">

# ⚡ SENTINELX // V2.0
**[ NEXT-GEN WEB SECURITY RECONNAISSANCE TOOL ]**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Org](https://img.shields.io/badge/ORG-HACKOPS-red.svg?style=for-the-badge)](https://github.com/Hackops-Official)

---

> **SentinelX** is a high-performance, mobile-responsive automated scanner designed for security researchers and penetration testers. It bridges the gap between powerful CLI tools and an intuitive, modern cyber-interface.

[**🌐 Live Demo**](#) | [**📜 Documentation**](#) | [**🛠️ Setup Guide**](#)

</div>

---

## 🚀 ABOUT HACKOPS
**HACKOPS** is an elite security-focused collective dedicated to building tools that simplify complex offensive and defensive operations. We believe in high-utility software wrapped in professional, immersive user interfaces. 

* **Vision:** Democratizing advanced security reconnaissance.
* **Mission:** Building the "Swiss Army Knife" for the modern operator.

---

## 🛠️ CORE CAPABILITIES
SentinelX automates the heavy lifting of initial recon. It integrates industry-standard engines into a unified data flow.

| Module | Function | Status |
| :--- | :--- | :--- |
| **Network Mapper** | Port discovery & Service detection | `OPERATIONAL` |
| **Web Auditor** | Nikto-based vulnerability scanning | `OPERATIONAL` |
| **Subdomain Recon** | Automated asset discovery | `STABLE` |
| **Threat Intelligence** | Real-time IP reputation tracking | `BETA` |

---

## 💻 THE INTERFACE
Designed with a "Terminal-First" philosophy, the UI features:
* **Glitch-Effect Typography:** For that authentic operator aesthetic.
* **Real-time Progress:** Live polling from the Flask backend via `main.js`.
* **Mobile Optimized:** Fully responsive for scans on-the-go via Android browsers.

---

## 🛠️ INSTALLATION & DEPLOYMENT

### 1. Prerequisites
Ensure you have the following installed on your system (Linux):
```bash
# Update system
sudo apt update && sudo apt install nmap nikto python3 -y
```
For the Termux
```bash
pkg update && pkg install nmap nikto python3 -y
```
### 2. Clone the Repository
```bash
git clone [https://github.com/YourUsername/Sentinelx.git](https://github.com/YourUsername/Sentinelx.git)
cd Sentinelx
```
### 3. Initialize Environment
Install the requirements 
```bash
pip install -r requirements.txt
```
### 4. Give the Permission 
```bash
chmod +x app.py
```
### 5. To run the tool
```bash
python3 app.py
```
### 6. Open the Browser 
Open the tab in browser 
```http://127.0.0.1:5000```

##🛠️ ARCHITECTURE FLOW
The system operates on a multi-threaded architecture to prevent UI blocking:
```graph LR
    A[Web UI] -- POST --> B[Flask Server]
    B -- Spawn Thread --> C[Scanner Engine]
    C -- Execute --> D[Nmap/Nikto]
    D -- Return Data --> C
    C -- Store Results --> B
    B -- JSON Status --> A
```
## 🤝 CONTRIBUTING
We welcome operators from all over the world.
Fork the Project.
Create your Feature Branch (git checkout -b feature/AmazingFeature).
Commit your Changes (git commit -m 'Add some AmazingFeature').
Push to the Branch (git push origin feature/AmazingFeature).
Open a Pull Request.

<div align="center">
⚠️ LEGAL DISCLAIMER
This tool is for educational and authorized testing purposes only. Usage of SentinelX for attacking targets without prior mutual consent is illegal. HACKOPS is not responsible for any misuse or damage caused by this program.
© 2026 HACKOPS SECURITY SOLUTIONS
</div>
