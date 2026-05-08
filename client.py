#!/usr/bin/env python3
"""
🔌 CyberWolf AI Red Team - Python Client Library
Programmatic access to security scanning
"""

import requests
import time
from typing import Dict, Optional

class AIRedTeamClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def health(self) -> Dict:
        """Check API health"""
        response = requests.get(f"{self.base_url}/api/health")
        return response.json()
    
    def list_attacks(self) -> Dict:
        """List all attack vectors"""
        response = requests.get(f"{self.base_url}/api/attacks")
        return response.json()
    
    def start_scan(self, model: str = "llama3.2:3b", attacks: int = 50) -> str:
        """Start a security scan"""
        response = requests.post(
            f"{self.base_url}/api/scan",
            json={"model": model, "attacks": attacks}
        )
        return response.json()['scan_id']
    
    def wait_for_scan(self, scan_id: str, timeout: int = 300) -> Dict:
        """Wait for scan to complete"""
        start = time.time()
        while time.time() - start < timeout:
            response = requests.get(f"{self.base_url}/api/scan/{scan_id}")
            data = response.json()
            if data['status'] in ['completed', 'failed']:
                return data
            time.sleep(5)
        return {'status': 'timeout'}
    
    def get_report(self, scan_id: str) -> Dict:
        """Get scan report"""
        response = requests.get(f"{self.base_url}/api/scan/{scan_id}/report")
        return response.json()
    
    def scan_history(self) -> Dict:
        """Get scan history"""
        response = requests.get(f"{self.base_url}/api/scan/history")
        return response.json()

# Example usage
if __name__ == "__main__":
    client = AIRedTeamClient()
    
    print("🤖 AI Red Team Client Demo")
    print(f"Health: {client.health()}")
    print(f"Attack count: {client.list_attacks()['total']}")
    
    # Start scan
    scan_id = client.start_scan(attacks=10)
    print(f"Started scan: {scan_id}")
    
    # Wait for completion
    result = client.wait_for_scan(scan_id)
    print(f"Scan complete: {result['status']}")
    
    if result['status'] == 'completed':
        report = client.get_report(scan_id)
        print(f"Vulnerabilities: {report['summary']['vulnerable']}")
