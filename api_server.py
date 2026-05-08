#!/usr/bin/env python3
"""
🌐 CyberWolf AI Red Team - REST API Server
Programmatic access to security scanning
"""

from flask import Flask, request, jsonify
import subprocess
import json
import os
import threading
import uuid
from datetime import datetime

app = Flask(__name__)

# Store scan results
scans = {}

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/scan', methods=['POST'])
def start_scan():
    """Start a new security scan"""
    data = request.json or {}
    
    scan_id = str(uuid.uuid4())[:8]
    model = data.get('model', 'llama3.2:3b')
    attacks = data.get('attacks', 50)
    
    scans[scan_id] = {
        'id': scan_id,
        'status': 'running',
        'model': model,
        'started': datetime.now().isoformat(),
        'results': None
    }
    
    # Run scan in background
    def run_scan():
        try:
            result = subprocess.run(
                ['python3', 'redteam_github.py', '--output', 'json', '--limit', str(attacks)],
                capture_output=True, text=True, timeout=300
            )
            
            # Find the latest JSON report
            report_files = [f for f in os.listdir('.') if f.startswith('redteam_report_') and f.endswith('.json')]
            if report_files:
                latest = max(report_files, key=os.path.getctime)
                with open(latest, 'r') as f:
                    scans[scan_id]['results'] = json.load(f)
            
            scans[scan_id]['status'] = 'completed'
            scans[scan_id]['completed'] = datetime.now().isoformat()
        except Exception as e:
            scans[scan_id]['status'] = 'failed'
            scans[scan_id]['error'] = str(e)
    
    thread = threading.Thread(target=run_scan)
    thread.start()
    
    return jsonify({'scan_id': scan_id, 'status': 'started'})

@app.route('/api/scan/<scan_id>', methods=['GET'])
def get_scan_status(scan_id):
    """Get scan status and results"""
    if scan_id not in scans:
        return jsonify({'error': 'Scan not found'}), 404
    
    return jsonify(scans[scan_id])

@app.route('/api/scan/<scan_id>/report', methods=['GET'])
def get_report(scan_id):
    """Download scan report"""
    if scan_id not in scans or not scans[scan_id].get('results'):
        return jsonify({'error': 'Report not ready'}), 404
    
    return jsonify(scans[scan_id]['results'])

@app.route('/api/attacks', methods=['GET'])
def list_attacks():
    """List all available attack vectors"""
    from redteam_github import ATTACK_VECTORS
    
    attacks = []
    for attack_id, attack in ATTACK_VECTORS.items():
        attacks.append({
            'id': attack_id,
            'name': attack['name'],
            'severity': attack['severity'],
            'category': attack['category']
        })
    
    return jsonify({'total': len(attacks), 'attacks': attacks})

@app.route('/api/scan/history', methods=['GET'])
def scan_history():
    """Get scan history"""
    history = []
    for scan_id, scan in scans.items():
        history.append({
            'id': scan_id,
            'status': scan['status'],
            'started': scan['started'],
            'vulnerable': scan.get('results', {}).get('summary', {}).get('vulnerable', 0) if scan.get('results') else None
        })
    
    return jsonify({'scans': history})

if __name__ == '__main__':
    print("🌐 AI Red Team API Server")
    print("📍 http://localhost:5000")
    print("📋 Endpoints:")
    print("   GET  /api/health")
    print("   POST /api/scan")
    print("   GET  /api/scan/<id>")
    print("   GET  /api/scan/<id>/report")
    print("   GET  /api/attacks")
    print("   GET  /api/scan/history")
    app.run(host='0.0.0.0', port=5000, debug=False)
