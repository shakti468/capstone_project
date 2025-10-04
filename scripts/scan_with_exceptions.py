import json
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANS_DIR = os.path.join(BASE_DIR, "scans")
CONFIG_FILE = os.path.join(BASE_DIR, "config", "exceptions.json")

os.makedirs(SCANS_DIR, exist_ok=True)

def load_exceptions():
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE) as f:
        return json.load(f).get("ignore_cves", [])

def run_trivy(image, outfile):
    cmd = [
        "trivy", "image", "--quiet",
        "--format", "json",
        "--output", outfile,
        image
    ]
    subprocess.run(cmd, check=True)

def filter_vulns(scan_file, exceptions):
    with open(scan_file) as f:
        data = json.load(f)

    for result in data.get("Results", []):
        if "Vulnerabilities" in result:
            result["Vulnerabilities"] = [
                v for v in result["Vulnerabilities"]
                if v.get("VulnerabilityID") not in exceptions
            ]

    with open(scan_file, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scan_with_exceptions.py <image>")
        sys.exit(1)

    image = sys.argv[1]
    outfile = os.path.join(SCANS_DIR, f"{image.replace('/', '_').replace(':', '_')}.json")

    exceptions = load_exceptions()
    print(f"🔎 Scanning {image} (ignoring {len(exceptions)} CVEs)")

    run_trivy(image, outfile)
    filter_vulns(outfile, exceptions)

    print(f"✅ Scan complete. Filtered report saved to {outfile}")
