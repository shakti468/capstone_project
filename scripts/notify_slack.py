import os
import glob
import requests

# Slack bot token
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#it_vulnerability_reports")

if not SLACK_BOT_TOKEN:
    raise ValueError("❌ SLACK_BOT_TOKEN not set. Run: export SLACK_BOT_TOKEN=xoxb-XXXX")

# Project root (one level up from scripts/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Find the latest report
list_of_reports = glob.glob(os.path.join(REPORTS_DIR, "vuln_report_*.html"))
if not list_of_reports:
    raise FileNotFoundError("❌ No reports found in reports/ folder. Run generate_report.py first.")

latest_report = max(list_of_reports, key=os.path.getctime)

print(f"📤 Sending Slack message with report link: {latest_report}")

# Slack chat.postMessage API
url = "https://slack.com/api/chat.postMessage"

message_text = f"📊 A new container vulnerability report is available:\n`{latest_report}`\nPlease open it locally or from repo artifacts."

response = requests.post(
    url,
    headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}",
             "Content-Type": "application/json"},
    json={
        "channel": SLACK_CHANNEL,
        "text": message_text
    }
)

resp_json = response.json()
if response.status_code != 200 or not resp_json.get("ok"):
    print("❌ Failed to send Slack message:", resp_json)
else:
    print("✅ Slack message sent successfully!")
