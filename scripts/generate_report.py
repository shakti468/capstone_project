import json
import os
from datetime import datetime

# Get absolute path to project root (one level up from scripts/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANS_DIR = os.path.join(BASE_DIR, "scans")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

report_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
report_file = os.path.join(REPORTS_DIR, f"vuln_report_{report_time}.html")

html_content = f"""
<html>
<head><title>Container Vulnerability Report</title></head>
<body>
<h2>Container Vulnerability Report - {report_time}</h2>
"""

for filename in os.listdir(SCANS_DIR):
    if filename.endswith(".json"):
        path = os.path.join(SCANS_DIR, filename)
        with open(path) as f:
            data = json.load(f)
            html_content += f"<h3>Image: {filename}</h3><ul>"
            for result in data.get("Results", []):
                for vuln in result.get("Vulnerabilities", []):
                    html_content += (
                        f"<li>[{vuln.get('Severity')}] {vuln.get('VulnerabilityID')} "
                        f"- {vuln.get('PkgName')} ({vuln.get('InstalledVersion')})</li>"
                    )
            html_content += "</ul>"

html_content += "</body></html>"

with open(report_file, "w") as f:
    f.write(html_content)

print(f"✅ Report generated: {report_file}")
