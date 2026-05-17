"""
Civados Client Repo Generator
==============================
This script creates a customised private GitHub repository for a new Civados client.

Trigger: Called by Make.com when a new client is tagged in GoHighLevel.

Input (JSON via webhook):
  - client_name        : Full name of the client business
  - business_type      : e.g. "plumbing", "personal training", "accounting"
  - owner_name         : First name of the business owner
  - location           : City/region e.g. "Manchester" or "Sydney, NSW"
  - services           : Comma-separated list e.g. "emergency plumbing, boiler repair"
  - website            : Client website URL (optional)
  - google_review_link : Client's Google review link (optional)
  - phone              : Client phone number (optional)

Output:
  - GitHub repo URL (private)
  - Confirmation of files created
"""

import os
import json
import base64
import requests
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN_HERE")
GITHUB_ORG   = os.environ.get("GITHUB_ORG", "SavechM")   # your GitHub username
GITHUB_API   = "https://api.github.com"
# ────────────────────────────────────────────────────────────────────────────


def slugify(text):
    """Turn 'Bob's Plumbing Manchester' into 'bobs-plumbing-manchester'"""
    import re
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def create_repo(repo_name, description):
    """Create a new PRIVATE GitHub repository."""
    url = f"{GITHUB_API}/user/repos"
    payload = {
        "name": repo_name,
        "description": description,
        "private": True,
        "auto_init": False
    }
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code == 422:
        # Repo already exists — that's fine, continue
        print(f"Repo {repo_name} already exists. Adding files.")
        return True
    r.raise_for_status()
    return True


def push_file(repo_name, file_path, content, commit_message):
    """Push a single file to a GitHub repo via the Contents API."""
    url = f"{GITHUB_API}/repos/{GITHUB_ORG}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    payload = {
        "message": commit_message,
        "content": encoded,
        "branch": "main"
    }

    # Check if file exists (to get SHA for update)
    existing = requests.get(url, headers=headers)
    if existing.status_code == 200:
        payload["sha"] = existing.json()["sha"]

    r = requests.put(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json().get("content", {}).get("html_url", "")


def customise(template, client):
    """Replace all placeholder tokens with real client data."""
    replacements = {
        "[BUSINESS NAME]"      : client["client_name"],
        "[YOUR BUSINESS NAME]" : client["client_name"],
        "[BUSINESS TYPE]"      : client["business_type"],
        "[YOUR BUSINESS TYPE]" : client["business_type"],
        "[YOUR NAME]"          : client["owner_name"],
        "[OWNER NAME]"         : client["owner_name"],
        "[LOCATION]"           : client["location"],
        "[CITY/REGION]"        : client["location"],
        "[SERVICE]"            : client["services"],
        "[SERVICES]"           : client["services"],
        "[YOUR GOOGLE REVIEW LINK]" : client.get("google_review_link", "https://g.page/r/YOUR-LINK/review"),
        "[GOOGLE REVIEW LINK]" : client.get("google_review_link", "https://g.page/r/YOUR-LINK/review"),
        "[YOUR NUMBER]"        : client.get("phone", "your phone number"),
        "[PHONE]"              : client.get("phone", "your phone number"),
        "[YOUR WEBSITE]"       : client.get("website", "your website"),
        "civados.com"          : client.get("website", "civados.com"),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


# ── FILE TEMPLATES ───────────────────────────────────────────────────────────

def readme(client):
    return customise(f"""# [BUSINESS NAME] — AI & Automation Resource Library

> Your private resource hub, set up and maintained by [Civados](https://civados.com).

**Business:** [BUSINESS NAME]
**Owner:** [OWNER NAME]
**Location:** [LOCATION]
**Services:** [SERVICES]
**Created:** {datetime.now().strftime("%B %Y")}

---

## What's In Here

This is your private library of AI tools, prompts, and automation workflows — built specifically for [BUSINESS NAME].

Everything is already customised for your business. Just copy, paste, and use.

| Section | What You'll Find |
|---|---|
| [/prompts](./prompts/) | AI prompts with your business details pre-filled |
| [/workflows](./workflows/) | Step-by-step automation setup guides for your business |
| [/resources](./resources/) | Tools and strategies relevant to [BUSINESS TYPE] |

---

## Quick Start

**Most useful things to use first:**

1. `prompts/lead-followup.md` — Copy the first SMS prompt and set it up in GHL today
2. `prompts/review-responses.md` — Use these every time you get a Google review
3. `workflows/missed-call-textback.md` — 20 minutes to set up, pays for itself immediately

---

## Your Business Details (Pre-filled)

All prompts in this library already include:
- Your business name: **[BUSINESS NAME]**
- Your location: **[LOCATION]**
- Your services: **[SERVICES]**
- Your Google review link: **[YOUR GOOGLE REVIEW LINK]**
- Your phone: **[YOUR NUMBER]**

You just need to add the customer's name and any job-specific details.

---

*Managed by [Civados](https://civados.com) | Questions? Email us at hello@civados.com*
""", client)


def lead_followup(client):
    return customise(f"""# Lead Follow-Up Prompts — [BUSINESS NAME]

> Pre-filled for [BUSINESS NAME] in [LOCATION]. Copy and use directly.

---

## SMS 1 — Immediate (Send within 5 minutes)

Paste this into GHL as your first automated SMS:

```
Hi {{{{contact.first_name}}}}, it's [OWNER NAME] from [BUSINESS NAME] in [LOCATION].

Thanks for reaching out about [SERVICES]. I'll be in touch shortly — is there a best time to give you a quick call?
```

---

## SMS 2 — Day 2 Follow-Up (No Reply)

```
Hey {{{{contact.first_name}}}} — just checking my message got through yesterday.

Happy to jump on a quick call whenever suits. Reply here or call us on [YOUR NUMBER].
```

---

## Email 1 — Day 1 (Sent 5 minutes after SMS 1)

**Subject options:**
- Your enquiry with [BUSINESS NAME]
- Re: [SERVICES] in [LOCATION]
- [OWNER NAME] from [BUSINESS NAME] here

**Body:**
```
Hi {{{{contact.first_name}}}},

Thanks for getting in touch with [BUSINESS NAME].

We specialise in [SERVICES] for [LOCATION] residents and businesses, and I'd love to help you out.

Can I grab 15 minutes for a quick call to understand what you're looking for?

[ADD YOUR CALENDLY OR BOOKING LINK HERE]

Speak soon,
[OWNER NAME]
[BUSINESS NAME]
[YOUR NUMBER]
```

---

## Email 2 — Day 3 (Value Add, No Reply)

**Subject:** Quick tip on [SERVICES]

```
Hi {{{{contact.first_name}}}},

I know you're busy, so I'll keep this short.

One thing most people don't realise about [SERVICES]: [ADD A GENUINELY USEFUL TIP FOR YOUR NICHE HERE].

If you'd like to chat about how this applies to your situation, I'm happy to jump on a quick call.

[OWNER NAME]
[BUSINESS NAME] | [LOCATION]
[YOUR NUMBER]
```

---

## Final SMS — Day 7

```
Hi {{{{contact.first_name}}}}, last message from me — I don't want to crowd your phone.

If you still need help with [SERVICES] in [LOCATION], just reply YES and I'll be in touch. No pressure either way.

— [OWNER NAME], [BUSINESS NAME]
```

---

*Resource library by [Civados](https://civados.com)*
""", client)


def review_responses(client):
    return customise(f"""# Google Review Response Templates — [BUSINESS NAME]

> Ready to copy-paste. Personalise the [CUSTOMER NAME] and any specific details.

---

## 5-Star Response (With Text)

```
Thank you so much, [CUSTOMER NAME]! We really appreciate you taking the time to share your experience with [BUSINESS NAME].

[ADD ONE SPECIFIC THING THEY MENTIONED] is something we always strive to get right, so it's great to hear that came through.

We look forward to helping you again — and please don't hesitate to refer us to anyone who needs [SERVICES] in [LOCATION]!

— [OWNER NAME] & the [BUSINESS NAME] team
```

---

## 5-Star Response (Stars Only, No Text)

```
Thank you for the 5 stars! We really appreciate your support of [BUSINESS NAME] here in [LOCATION]. Looking forward to helping you again soon! 🙏
```

---

## 4-Star Response

```
Thank you for your feedback, [CUSTOMER NAME], and for taking the time to leave a review.

We're glad to hear [POSITIVE ELEMENT] worked well for you. Your point about [THEIR CONCERN] is noted — we're always looking to improve and this helps.

We'd love to welcome you back next time you need [SERVICES]. Thanks again for supporting a local [LOCATION] business!

— [OWNER NAME], [BUSINESS NAME]
```

---

## Negative Review Response (Legitimate Complaint)

```
Thank you for your feedback, [CUSTOMER NAME]. I'm sorry to hear your experience with [BUSINESS NAME] didn't meet expectations.

This isn't the standard we hold ourselves to, and I'd genuinely like to understand what happened and make it right.

Please contact me directly on [YOUR NUMBER] or at [ADD EMAIL] so we can resolve this for you.

— [OWNER NAME], [BUSINESS NAME]
```

---

## Fake or Suspicious Review

```
Thank you for your message. We take all feedback seriously, however we're unable to locate any record of a booking or service under this name with [BUSINESS NAME].

If there's been any confusion, we'd welcome the chance to clarify — please reach out to us directly on [YOUR NUMBER].

— [BUSINESS NAME] Team
```

---

## Your Google Review Link

Send customers directly here to leave a review:

**[YOUR GOOGLE REVIEW LINK]**

Add this to:
- Post-job SMS
- Email signature
- Invoices
- Business cards

---

*Resource library by [Civados](https://civados.com)*
""", client)


def missed_call_workflow(client):
    return customise(f"""# GHL Workflow: Missed Call Text-Back — [BUSINESS NAME]

> Set this up once. It runs forever. Estimated setup time: 20 minutes.

---

## What It Does

When [BUSINESS NAME] misses an inbound call, GHL automatically sends a text to the caller within 60 seconds.

**Why it matters:** 78% of customers go with whoever responds first. Most won't leave a voicemail — they'll just call a competitor.

---

## Setup Steps

### 1. Create the Workflow

- GHL → Automation → Workflows → New Workflow
- Name: `[BUSINESS NAME] — Missed Call Text-Back`
- Status: Draft

### 2. Set the Trigger

- Trigger type: **Missed Call**
- Filter: Inbound calls only

### 3. Action 1 — Immediate SMS (0 minute delay)

Copy this message exactly:

```
Hi! Sorry I missed your call — it's [OWNER NAME] from [BUSINESS NAME].

What can I help you with? Reply here and I'll get back to you straight away, or call us back on [YOUR NUMBER].
```

### 4. Action 2 — Internal Notification (0 minute delay)

- Type: Email notification to owner
- Message: "Missed call from {{contact.phone}}. Auto-text sent. Follow up if no reply in 15 mins."
- Send to: [ADD YOUR EMAIL]

### 5. Action 3 — Wait & Check (30 minute delay)

- Type: If/Else
- Condition: Contact has replied to SMS
- YES → Remove from workflow, add tag `missed-call-responded`
- NO → Continue

### 6. Action 4 — Second SMS (30 minutes, no reply)

```
Still here if you need anything! Happy to answer questions about [SERVICES] in [LOCATION] or get you booked in.

Just reply here or call [YOUR NUMBER]. — [OWNER NAME]
```

### 7. Activate

- Save → Test with your own mobile → Publish

---

## Settings Checklist

- [ ] Send window: 8am–8pm [LOCATION] time
- [ ] Stop on reply: ON
- [ ] Stop if appointment booked: ON
- [ ] Test before publishing: DONE

---

*Resource library by [Civados](https://civados.com)*
""", client)


# ── MAIN ─────────────────────────────────────────────────────────────────────

def create_client_repo(client_data: dict) -> dict:
    """
    Main function. Call this with client details to create their private repo.

    Returns: dict with repo_url and list of files created.
    """
    name_slug   = slugify(client_data["client_name"])
    repo_name   = f"civados-{name_slug}"
    description = f"AI prompts and automation resources for {client_data['client_name']} — managed by Civados"

    print(f"\n🚀 Creating repo: {repo_name}")
    create_repo(repo_name, description)

    files = {
        "README.md"                         : readme(client_data),
        "prompts/lead-followup.md"          : lead_followup(client_data),
        "prompts/review-responses.md"       : review_responses(client_data),
        "workflows/missed-call-textback.md" : missed_call_workflow(client_data),
    }

    created = []
    for path, content in files.items():
        print(f"  ✓ Pushing {path}")
        push_file(repo_name, path, content, f"Add {path}")
        created.append(path)

    repo_url = f"https://github.com/{GITHUB_ORG}/{repo_name}"
    print(f"\n✅ Done! Repo live at: {repo_url}\n")

    return {
        "repo_url"      : repo_url,
        "repo_name"     : repo_name,
        "files_created" : created,
        "client"        : client_data["client_name"]
    }


# ── WEBHOOK SERVER (for Make.com to call) ────────────────────────────────────

def run_server():
    """Simple HTTP server to receive webhooks from Make.com / GHL."""
    from http.server import HTTPServer, BaseHTTPRequestHandler

    class WebhookHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body   = self.rfile.read(length)
            try:
                client_data = json.loads(body)
                result      = create_client_repo(client_data)
                response    = json.dumps(result).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(response)
            except Exception as e:
                error = json.dumps({"error": str(e)}).encode()
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(error)

        def log_message(self, format, *args):
            pass  # Suppress default logging

    port = int(os.environ.get("PORT", 8080))
    print(f"Civados Repo Generator running on port {port}")
    HTTPServer(("0.0.0.0", port), WebhookHandler).serve_forever()


# ── RUN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "server":
        run_server()
    else:
        # Test run with example client
        test_client = {
            "client_name"        : "Johnson's Plumbing",
            "business_type"      : "plumbing",
            "owner_name"         : "Dave Johnson",
            "location"           : "Manchester",
            "services"           : "emergency plumbing, boiler repair, bathroom fitting",
            "website"            : "https://johnsonsplumbing.co.uk",
            "google_review_link" : "https://g.page/r/EXAMPLE/review",
            "phone"              : "0161 123 4567"
        }
        result = create_client_repo(test_client)
        print(json.dumps(result, indent=2))
