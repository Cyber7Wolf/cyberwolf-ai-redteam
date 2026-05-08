#!/usr/bin/env python3
"""
🌐 CyberWolf AI Red Team - Web Dashboard
View assessment results, compare models, track trends
"""

from flask import Flask, render_template_string, jsonify, send_file
import json
import os
import glob
from datetime import datetime

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Red Team Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0a0e27;
            color: #00ff88;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 30px;
            border-bottom: 2px solid #00ff88;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(0,0,0,0.6);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .stat-value { font-size: 2.5em; font-weight: bold; }
        .reports-list {
            background: rgba(0,0,0,0.6);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        .report-item {
            padding: 10px;
            border-bottom: 1px solid #333;
            cursor: pointer;
        }
        .report-item:hover { background: rgba(0,255,136,0.1); }
        .chart-container { margin: 20px 0; }
        button {
            background: #00ff88;
            color: #0a0e27;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🤖 AI Red Team Dashboard</h1>
        <p>LLM Security Assessment Platform</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card"><div class="stat-value" id="totalReports">0</div><div>Total Reports</div></div>
        <div class="stat-card"><div class="stat-value" id="avgRisk">0</div><div>Avg Risk Score</div></div>
        <div class="stat-card"><div class="stat-value" id="totalVulns">0</div><div>Total Vulns Found</div></div>
        <div class="stat-card"><div class="stat-value" id="lastScan">-</div><div>Last Scan</div></div>
    </div>
    
    <div class="chart-container">
        <div id="trendChart"></div>
    </div>
    
    <div class="reports-list">
        <h2>📊 Recent Reports</h2>
        <div id="reportsList"></div>
    </div>
</div>

<script>
    function loadData() {
        fetch('/api/stats')
            .then(res => res.json())
            .then(data => {
                document.getElementById('totalReports').textContent = data.total_reports;
                document.getElementById('avgRisk').textContent = data.avg_risk;
                document.getElementById('totalVulns').textContent = data.total_vulnerabilities;
                document.getElementById('lastScan').textContent = data.last_scan;
                
                // Render reports list
                const reportsDiv = document.getElementById('reportsList');
                reportsDiv.innerHTML = '';
                data.reports.forEach(report => {
                    const div = document.createElement('div');
                    div.className = 'report-item';
                    div.innerHTML = `${report.name} - Risk: ${report.risk_score} - ${report.date}`;
                    div.onclick = () => window.open(`/view/${report.name}`, '_blank');
                    reportsDiv.appendChild(div);
                });
                
                // Render chart
                Plotly.newPlot('trendChart', data.chart.data, data.chart.layout);
            });
    }
    
    loadData();
    setInterval(loadData, 30000);
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/stats')
def api_stats():
    reports = []
    for f in glob.glob('redteam_report_*.json'):
        try:
            with open(f, 'r') as file:
                data = json.load(file)
                reports.append({
                    'name': f,
                    'risk_score': data.get('summary', {}).get('risk_score', 0),
                    'date': f.split('_')[2].split('.')[0]
                })
        except:
            pass
    
    reports.sort(key=lambda x: x['date'], reverse=True)
    
    total_reports = len(reports)
    avg_risk = sum(r['risk_score'] for r in reports) // total_reports if total_reports > 0 else 0
    total_vulns = 0
    
    chart_data = {
        'data': [{
            'x': [r['date'][:8] for r in reports[:10]],
            'y': [r['risk_score'] for r in reports[:10]],
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Risk Score',
            'line': {'color': '#00ff88'}
        }],
        'layout': {
            'title': 'Risk Score Trend',
            'plot_bgcolor': '#0a0e27',
            'paper_bgcolor': '#0a0e27',
            'font': {'color': '#00ff88'}
        }
    }
    
    return jsonify({
        'total_reports': total_reports,
        'avg_risk': avg_risk,
        'total_vulnerabilities': total_vulns,
        'last_scan': reports[0]['date'] if reports else 'None',
        'reports': reports[:20],
        'chart': chart_data
    })

@app.route('/view/<filename>')
def view_report(filename):
    return send_file(filename, mimetype='text/html')

if __name__ == '__main__':
    print("🌐 Dashboard running at http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
