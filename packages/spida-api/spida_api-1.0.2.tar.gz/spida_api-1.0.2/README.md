# SPIDA FORMS - API Library + Webhook & Form Manager

## Overview
This project provides a **Webhook & Form Manager** for interacting with **SPIDA Studio** forms. The application allows users to:
- **Manage Webhooks**: Register and unregister webhooks for form updates.
- **Edit Forms**: Fetch and update SPIDA forms.
- **View Webhook Events**: Monitor real-time webhook event logs.

This document provides instructions on how to set up and use the system.

---

## API Library

> Add to requirements.in
```text
spida-api
```

```python
# Read SPIDA API values from .env
SPIDA_SERVER = os.getenv("SPIDA_SERVER")
SPIDA_API_KEY = os.getenv("SPIDA_API_KEY")
SPIDA_USERNAME = os.getenv('SPIDA_USERNAME')
SPIDA_PASSWORD = os.getenv('SPIDA_PASSWORD')
SPIDA_COMPANY_ID = os.getenv('SPIDA_COMPANY_ID')

spida_api = SpidaAPI(SPIDA_USERNAME, SPIDA_PASSWORD, SPIDA_SERVER)
spida_api.switch_company(SPIDA_COMPANY_ID)
```

## SPIDA Documentation
- SPIDA Webhook API Docs: [SPIDA Webhook API](https://github.com/spidasoftware/schema/blob/master/doc/apis/webhookAPI.md)
- **Production SPIDA**: [techserv.spidastudio.com](https://techserv.spidastudio.com)
- **Test SPIDA**: [test-techserv.spidastudio.com](https://test-techserv.spidastudio.com)

### Form Templates
| Form Name | Template URL |
|-----------|-------------|
| **Oncor Work Order Form (JUMR)** | [Edit Template 849](https://techserv.spidastudio.com/projectmanager/formTemplate/edit/849) |
| **Oncor JUFR Work Order Form** | [Edit Template 951317](https://techserv.spidastudio.com/projectmanager/formTemplate/edit/951317) |

---

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- **Node.js** (for local testing, if required)
- **Python & Flask** (for backend services)

### Environment Variables (`.env`)
Create a `.env` file in the project root and add the following credentials:
```ini
# Admin user for both (Ask Keagan/Logan)
SPIDA_USERNAME=
SPIDA_PASSWORD=
# Oncor
SPIDA_COMPANY_ID=145

# PROD
# SPIDA_SERVER=techserv.spidastudio.com
# SPIDA_API_KEY=

# TEST
SPIDA_SERVER=test-techserv.spidastudio.com
SPIDA_API_KEY=
```

### Running the Server
```bash
# Clone the repository
git clone https://github.com/TechServ-Consulting-Training-Ltd/spida_api
cd spida_api

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python server.py
```

### Running the Web App
The frontend runs directly in the browser using Babel. To start:
```bash
# Ensure you are in the project root
python -m http.server 8000
```
Then, open `http://localhost:8000` in your browser.

---

## Features & Usage

### **Manage Webhooks**
- View all registered webhooks.
- Register a new webhook by providing a **URL, channel, and event regex**.
- Unregister existing webhooks.

**Example UI for Production:**
<img width="1638" alt="Webhook   Form Manager" src="https://github.com/user-attachments/assets/cd2ab855-9d23-40e1-968d-8a842c5d6a8e" />

**Example Cloudwatch logs for Production:**
<img width="1435" alt="Pasted Graphic 19" src="https://github.com/user-attachments/assets/b2409019-016b-4719-81c1-4f0080a71f62" />

**To test webhook registrations:**
1. Navigate to the test SPIDA manager:
   [Test Project Manager](https://test-techserv.spidastudio.com/projectmanager/manager/detail/project?loadedTagIds=[%22524%22])
   **SPIDA UI:**
   ![unknown](https://github.com/user-attachments/assets/9a9efd0d-152a-43c6-a45d-e2dadaf40ff6)
3. Modify a form and submit changes.
4. View logs to verify webhook events.

### **Webhook Expiration**
We have a scheduler that hits a Lambda every 4 hours that refreshes all of our
webhooks for another 24 hours.
- Code for Lambda: https://github.com/TechServ-Consulting-Training-Ltd/oncor/blob/staging/src/webhook_lambda_handler.py?#L32
- Lambda function in AWS: https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/spida_webhook?subtab=triggers&tab=configure
- Event definition: https://us-east-1.console.aws.amazon.com/events/home?region=us-east-1#/eventbus/default/rules/spida_daily_webhook_cron_job
- Lambda Logs: https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fspida_webhook

### **Edit Forms**
- Retrieve a form by entering its **Form ID**.
- Update form field values and submit changes.
- View API responses directly in the UI.

### **View Webhook Events**
- Monitor incoming webhook events in real-time.
- Uses WebSockets for dynamic updates.

---

## Using Ngrok for Webhook Debugging
To test webhooks locally, use **ngrok** to expose your local server.
```bash
ngrok http 5003
```
Then register `https://your-ngrok-url/webhooks` as a webhook URL in the SPIDA UI.

---

## Example Webhook Payload
```json
{
  "channel": "Form",
  "eventName": "update:TEST_02_14_2025:Oncor Work Order Form",
  "hookId": "257b38c2-2d3b-4d14-b660-22feb8b2417a",
  "payload": {
    "form": {
      "fields": {
        "Email Subject Field": "Oncor Action Required: Need WR Approval in WMIS (WR Number shown below)",
        "Oncor Work Order Name": "3334452",
        "Oncor Work Order Number": "3334452"
      },
      "projectLevelRequiredFor": "PROJECT",
      "template": "849",
      "title": "Oncor Work Order Form"
    },
    "parentId": 15672587,
    "parentName": "TEST_02_14_2025",
    "projectId": 15672587,
    "projectName": "TEST_02_14_2025",
    "user": "kmcnew@techservltd.net"
  },
  "timestamp": 1739905831161
}
```
