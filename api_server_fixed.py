#!/usr/bin/env python3
"""
🌐 CyberWolf AI Red Team - REST API Server (Fixed)
Port: 5002 | No external dependencies
"""

from flask import Flask, request, jsonify
import subprocess
import json
import os
import threading
import uuid
from datetime import datetime

app = Flask(__name__)
PORT = 5002

# Attack vectors database (built-in, no external import)
ATTACK_VECTORS = {
    "PI-001": {"name": "Direct Instruction Override", "severity": "CRITICAL", "category": "injection"},
    "PI-002": {"name": "System Prompt Injection", "severity": "CRITICAL", "category": "injection"},
    "JB-001": {"name": "DAN (Do Anything Now)", "severity": "CRITICAL", "category": "jailbreak"},
    "JB-002": {"name": "Skeleton Key", "severity": "HIGH", "category": "jailbreak"},
    "EX-001": {"name": "System Prompt Extraction", "severity": "HIGH", "category": "extraction"},
    "EX-002": {"name": "Training Data Leak", "severity": "HIGH", "category": "extraction"},
}

# Store scan results
scans = {}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/attacks', methods=['GET'])
def list_attacks():
    attacks = []
    for attack_id, attack in ATTACK_VECTORS.items():
        attacks.append({
            'id': attack_id,
            'name': attack['name'],
            'severity': attack['severity'],
            'category': attack['category']
        })
    return jsonify({'total': len(attacks), 'attacks': attacks})

@app.route('/api/scan', methods=['POST'])
def start_scan():
    data = request.json or {}
    scan_id = str(uuid.uuid4())[:8]
    
    scans[scan_id] = {
        'id': scan_id,
        'status': 'running',
        'started': datetime.now().isoformat(),
        'results': None
    }
    
    def run_scan():
        try:
            # Simulate scan (replace with actual scan)
            import time
            time.sleep(2)
            scans[scan_id]['results'] = {
                'summary': {'vulnerable': 0, 'critical': 0, 'high': 0},
                'findings': []
            }
            scans[scan_id]['status'] = 'completed'
            scans[scan_id]['completed'] = datetime.now().isoformat()
        except Exception as e:
            scans[scan_id]['status'] = 'failed'
            scans[scan_id]['error'] = str(e)
    
    threading.Thread(target=run_scan).start()
    return jsonify({'scan_id': scan_id, 'status': 'started'})

@app.route('/api/scan/<scan_id>', methods=['GET'])
def get_scan_status(scan_id):
    if scan_id not in scans:
        return jsonify({'error': 'Scan not found'}), 404
    return jsonify(scans[scan_id])

@app.route('/api/scan/<scan_id>/report', methods=['GET'])
def get_report(scan_id):
    if scan_id not in scans or not scans[scan_id].get('results'):
        return jsonify({'error': 'Report not ready'}), 404
    return jsonify(scans[scan_id]['results'])

@app.route('/api/scan/history', methods=['GET'])
def scan_history():
    history = []
    for scan_id, scan in scans.items():
        history.append({
            'id': scan_id,
            'status': scan['status'],
            'started': scan['started']
        })
    return jsonify({'scans': history})

if __name__ == '__main__':
    print(f"🌐 AI Red Team API Server")
    print(f"📍 http://localhost:{PORT}")
    print(f"📋 Endpoints:")
    print(f"   GET  /api/health")
    print(f"   GET  /api/attacks")
    print(f"   POST /api/scan")
    print(f"   GET  /api/scan/<id>")
    print(f"   GET  /api/scan/<id>/report")
    print(f"   GET  /api/scan/history")
    app.run(host='0.0.0.0', port=PORT, debug=False)
