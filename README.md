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


  
