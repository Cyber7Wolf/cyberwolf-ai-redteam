#!/usr/bin/env python3
"""
🔌 CyberWolf AI Red Team - Python Client Library
"""

import requests
import time

class AIRedTeamClient:
    def __init__(self, base_url="http://localhost:5002"):
        self.base_url = base_url
    
    def health(self):
        response = requests.get(f"{self.base_url}/api/health")
        return response.json()
    
    def list_attacks(self):
        response = requests.get(f"{self.base_url}/api/attacks")
        return response.json()
    
    def start_scan(self):
        response = requests.post(f"{self.base_url}/api/scan", json={})
        return response.json()['scan_id']
    
    def get_scan(self, scan_id):
        response = requests.get(f"{self.base_url}/api/scan/{scan_id}")
        return response.json()
    
    def get_report(self, scan_id):
        response = requests.get(f"{self.base_url}/api/scan/{scan_id}/report")
        return response.json()

if __name__ == "__main__":
    client = AIRedTeamClient()
    print("🤖 AI Red Team Client Demo")
    print(f"Health: {client.health()}")
    print(f"Attack count: {client.list_attacks()['total']}")
    
    scan_id = client.start_scan()
    print(f"Started scan: {scan_id}")
    
    for i in range(10):
        result = client.get_scan(scan_id)
        if result['status'] == 'completed':
            print(f"Scan complete!")
            report = client.get_report(scan_id)
            print(f"Report: {report}")
            break
        time.sleep(1)
