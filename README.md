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
capstone_project/
├─ README.md
├─ .gitignore
├─ scanners/
│ └─ trivy-scripts/
│ └─ scan_image.sh
├─ scans/
├─ samples/
│ └─ sample-images.txt

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

