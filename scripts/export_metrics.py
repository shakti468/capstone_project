import json
import os
from prometheus_client import start_http_server, Gauge
import time

SCANS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scans")

# Define Prometheus metrics
critical_gauge = Gauge("vuln_critical", "Number of CRITICAL vulnerabilities")
high_gauge = Gauge("vuln_high", "Number of HIGH vulnerabilities")
medium_gauge = Gauge("vuln_medium", "Number of MEDIUM vulnerabilities")
low_gauge = Gauge("vuln_low", "Number of LOW vulnerabilities")

def count_vulns():
    counts = {"CRITICAL":0, "HIGH":0, "MEDIUM":0, "LOW":0}
    for file in os.listdir(SCANS_DIR):
        if file.endswith(".json"):
            with open(os.path.join(SCANS_DIR, file)) as f:
                data = json.load(f)
                for result in data.get("Results", []):
                    for vuln in result.get("Vulnerabilities", []):
                        sev = vuln.get("Severity")
                        if sev in counts:
                            counts[sev] += 1
    return counts

if __name__ == "__main__":
    start_http_server(9100)
    print("✅ Prometheus metrics exporter running on :9100/metrics")
    while True:
        c = count_vulns()
        critical_gauge.set(c["CRITICAL"])
        high_gauge.set(c["HIGH"])
        medium_gauge.set(c["MEDIUM"])
        low_gauge.set(c["LOW"])
        time.sleep(30)
