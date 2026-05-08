# 🤖 CyberWolf AI Red Team - LLM Security Testing Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 🎯 What is CyberWolf AI Red Team?

**AI-powered security testing framework for Large Language Models** that automatically detects vulnerabilities using 100+ attack vectors.

### Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **100+ Attack Vectors** | Prompt injection, jailbreaks, data extraction |
| 📊 **Professional Reports** | HTML, PDF, JSON formats |
| 🌐 **REST API** | Programmatic access |
| 🔄 **CI/CD Ready** | GitHub Actions integration |
| 🐳 **Docker Support** | Easy deployment |
| 📧 **Email Reports** | Send to stakeholders |

---

## 🚀 Quick Start

### Local Installation

```bash
git clone https://github.com/Cyber7Wolf/cyberwolf-ai-redteam.git
cd cyberwolf-ai-redteam
pip install -r requirements.txt
ollama serve &
python3 redteam_ultimate.py

docker-compose up -d

# Start API server
python3 api_server_fixed.py

# Run a scan
curl -X POST http://localhost:5002/api/scan

from client_fixed import AIRedTeamClient

client = AIRedTeamClient()
scan_id = client.start_scan()
result = client.get_report(scan_id)
print(f"Vulnerabilities: {result['summary']['vulnerable']}")
