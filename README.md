# capstone_project

# Container Image Vulnerability Scanner — Step 1

## Project Purpose
Automatically scan container images for known vulnerabilities before deployment. This ensures only secure images go to production.

---

## Step 1 Deliverables
- Git repository skeleton and folder structure
- Trivy vulnerability scanner installed
- Ability to scan sample images and produce JSON output

---

## Repository Structure
```bash
capstone_project/
├─ README.md
├─ .gitignore
├─ scanners/
│ └─ trivy-scripts/
│ └─ scan_image.sh
├─ scans/
├─ samples/
│ └─ sample-images.txt
bash

---

## Prerequisites
- **Docker**: `docker --version`
- **Python 3.8+**: `python --version`
- **Trivy**: `trivy --version`  

---

## Install Trivy
**Linux (apt-based)**
```bash
sudo apt-get update
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install -y trivy
```

## Sample Images
```bash
mkdir -p samples
cat > samples/sample-images.txt <<EOF
alpine:3.18
python:3.11-slim
nginx:stable
EOF
```

## Pull images 
```bash
Get-Content samples\sample-images.txt | ForEach-Object { docker pull $_ }
```  
### Screenshots
<img width="1130" height="457" alt="image" src="https://github.com/user-attachments/assets/bf25a8fa-83cb-4a57-b60a-5a6664ddb733" />

------

## Scan images
```bash
trivy image --format table alpine:3.18
trivy image --format json --output scans/alpine_3.18.json alpine:3.18
```

## Screenshots
<img width="1466" height="397" alt="image" src="https://github.com/user-attachments/assets/3762563e-76e9-4797-b8aa-4557d72a62e8" />



-----

# Step 2 — CI/CD Integration with Vulnerability Scanning

- Purpose
Integrate the vulnerability scanner into a CI/CD pipeline so every new container image is automatically scanned. Builds fail if vulnerabilities exceed severity thresholds (HIGH or CRITICAL), preventing insecure images from being deployed.

## Folder Structure Update
```bash
ci/
 └─ github-actions/
     └─ trivy-scan.yml
```

## GitHub Actions Workflow
```bash
name: Container Vulnerability Scan

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  trivy-scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Docker
        uses: docker/setup-buildx-action@v2

      - name: Build Docker image
        run: |
          docker build -t myapp:test .

      - name: Run Trivy Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:test'
          format: 'table'
          exit-code: '1'
          severity: 'HIGH,CRITICAL'
```

## Running the Workflow
<img width="1503" height="782" alt="image" src="https://github.com/user-attachments/assets/c5a34f32-c749-4c89-a139-75024116cc74" />

-----

# Step 3 — Report Generation & Slack Notifications

- In this step, we extend our vulnerability scanner to generate HTML reports from Trivy scan results and send Slack notifications so the DevOps team gets real-time updates.

## Folder Structure Update
```bash
container-vuln-scanner/
├─ scripts/
│  ├─ generate_report.py    # Generates HTML report from JSON scans
│  └─ notify_slack.py       # Sends report link to Slack channel
├─ scans/                   # Trivy JSON scan results
├─ reports/                 # Generated HTML reports
```

## Open Slack Workspace
-	Go to https://slack.com and log in.

## Choose a Channel
-	Pick the channel where you want to receive vulnerability reports.

## Invite Your Bot to the Channel

Inside the channel, at the bottom chat box (where you normally type messages):
1.	Type the following command (replace YourBotName with the bot name you set when creating it in Slack API):
2.	/invite @YourBotName

### Screenshots:
<img width="1560" height="903" alt="image" src="https://github.com/user-attachments/assets/1266ae46-715a-4539-8661-d7bdd2c15cfb" />


## Setup before running
## Export environment variables 
```bash
 export SLACK_BOT_TOKEN="xoxb-your-token"
	export SLACK_CHANNEL="C05XXXXXXX"   # Replace with your Slack channel ID
```

### Screenshots
<img width="1468" height="75" alt="image" src="https://github.com/user-attachments/assets/f24277a8-f525-4a86-9bdf-c50a71632376" />

## 	Run your report generator and the notifier:
<img width="1453" height="142" alt="image" src="https://github.com/user-attachments/assets/8c7d27b8-c51d-4c53-b64c-31b342898ad9" />

## 📌 Example Slack Message

- In your channel (e.g., #it_vulnerability_reports) you will see:

### Screenshot
<img width="932" height="358" alt="image" src="https://github.com/user-attachments/assets/0f192c5c-6689-463d-bcd4-c12c15ef6f18" />

---------



# 📊 Step 4 — Web Dashboard with Grafana + Prometheus
- In this step, we build a dashboard to visualize vulnerability trends over time.
Each Trivy scan summary is exported as metrics → collected by Prometheus → visualized in Grafana.

## Folder Structure
```bash
container-vuln-scanner/
├─ scripts/
│  └─ export_metrics.py      # Prometheus metrics exporter
├─ scans/                    # JSON scan outputs from Trivy
├─ reports/                  # HTML reports (Step 3)
├─ dashboard/
│  ├─ docker-compose.yml     # Runs Prometheus + Grafana
│  ├─ prometheus.yml         # Prometheus config
│  └─ grafana-provisioning/  # (optional auto-setup)
│     ├─ datasources/
│     │   └─ datasource.yml
│     └─ dashboards/
│         └─ vuln-dashboard.json

```
## Run Prometheus + Grafana
```bash
version: '3.7'

services:
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Run:
```bash
cd dashboard
docker-compose up -d
```
### Prometheus → http://localhost:9090
<img width="966" height="708" alt="image" src="https://github.com/user-attachments/assets/ac40e257-77b8-464e-883f-83e73415f000" />

### Grafana → http://localhost:3000
<img width="1133" height="762" alt="image" src="https://github.com/user-attachments/assets/ef34df00-726e-493d-982e-edde0798248f" />

## Configure Prometheus
```bash
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'vuln_scanner'
    static_configs:
      - targets: ['host.docker.internal:9100']
```

## Export Metrics from Scans
```bash
import json
import os
from prometheus_client import start_http_server, Gauge
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANS_DIR = os.path.join(BASE_DIR, "scans")

# Prometheus metrics
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
    print("✅ Exporter running at :9100/metrics")
    while True:
        c = count_vulns()
        critical_gauge.set(c["CRITICAL"])
        high_gauge.set(c["HIGH"])
        medium_gauge.set(c["MEDIUM"])
        low_gauge.set(c["LOW"])
        time.sleep(30)
```

## Install dependencies:
```bash
pip install prometheus-client
```
## Run:
```bash
python3 scripts/export_metrics.py
```
## Check → http://localhost:9100/metrics
<img width="932" height="982" alt="image" src="https://github.com/user-attachments/assets/44a4b284-ce97-4060-af6d-0a31111393c3" />


------


  
