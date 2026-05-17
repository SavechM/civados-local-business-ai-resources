# Civados Client Repo Automation — Setup Guide

> When you tag a new client in GoHighLevel, this system automatically creates a private GitHub resource library customised for their business. No manual work required.

---

## How It Works (Plain English)

```
New client tagged in GHL
        ↓
GHL fires a webhook (sends client details to Make.com)
        ↓
Make.com calls your Repo Generator script
        ↓
Script creates a private GitHub repo customised for the client
        ↓
Repo URL gets stored back in GHL on the client's contact
        ↓
You (or your team) share the repo link with the client at onboarding
```

Total time once set up: **0 minutes per client.** It runs automatically.

---

## What You Need

- [ ] GoHighLevel account (you have this)
- [ ] GitHub account — SavechM (you have this)
- [ ] Make.com account (free tier works to start) — make.com
- [ ] A server to run the Python script (options below)
- [ ] Your GitHub token (you already created this)

---

## Part 1 — Deploy the Script

The script (`create_client_repo.py`) needs to run somewhere on the internet so Make.com can call it.

**Easiest option — Railway (free tier, no coding):**

1. Go to [railway.app](https://railway.app) and sign up with your GitHub account
2. Click **New Project → Deploy from GitHub**
3. Select your `civados-local-business-ai-resources` repo
4. Railway will detect the Python file automatically
5. Go to **Variables** and add:
   - `GITHUB_TOKEN` = your GitHub token
   - `GITHUB_ORG` = SavechM
6. Go to **Settings → Networking → Generate Domain**
7. Copy the URL — it'll look like: `https://civados-abc123.up.railway.app`

That's your webhook URL. Keep it handy.

**Alternative — Run it on your own server (if you have one):**
```bash
pip install requests
GITHUB_TOKEN=your_token GITHUB_ORG=SavechM python create_client_repo.py server
```

---

## Part 2 — Set Up the GHL Trigger

In GoHighLevel:

1. Go to **Automation → Workflows → New Workflow**
2. Name it: `New Client — Repo Generator`
3. **Trigger:** Contact Tag Added
   - Tag: `civados-client` (or whatever tag you use for new paying clients)
4. **Action:** Webhook
   - URL: `https://your-railway-url.up.railway.app` (from Part 1)
   - Method: POST
   - Body (JSON):
   ```json
   {
     "client_name": "{{contact.company_name}}",
     "business_type": "{{contact.customField.business_type}}",
     "owner_name": "{{contact.first_name}}",
     "location": "{{contact.city}}",
     "services": "{{contact.customField.services}}",
     "website": "{{contact.website}}",
     "phone": "{{contact.phone}}",
     "google_review_link": "{{contact.customField.google_review_link}}"
   }
   ```
5. **Action 2:** Update Contact
   - Custom field: `github_repo_url`
   - Value: (this gets populated by the webhook response — see Make.com step)

---

## Part 3 — Wire It in Make.com

If you want Make.com to handle the middle step (catching the response and writing back to GHL):

1. Go to [make.com](https://make.com) → **Create a new scenario**
2. **Module 1:** Webhooks → Custom Webhook
   - Click **Add** → Copy the webhook URL Make.com gives you
   - Use THIS URL in your GHL workflow instead of the Railway URL
3. **Module 2:** HTTP → Make a Request
   - URL: your Railway script URL
   - Method: POST
   - Body: pass through the data from Module 1
4. **Module 3:** GoHighLevel → Update Contact
   - Contact ID: from the webhook data
   - Custom field `github_repo_url`: from the HTTP response

Save and activate.

---

## Part 4 — Create the GHL Custom Fields

In GoHighLevel, add these custom fields to contacts:

| Field Name | Type | Used For |
|---|---|---|
| `business_type` | Text | Type of business (plumber, gym, etc.) |
| `services` | Text | Main services offered |
| `google_review_link` | Text | Their Google review URL |
| `github_repo_url` | Text | Auto-populated — their resource repo link |

Go to: **Settings → Custom Fields → Add Field**

---

## Part 5 — Test It

1. Create a test contact in GHL with all fields filled in
2. Add the trigger tag manually
3. Watch Railway logs — you should see the script run
4. Check GitHub — a new private repo should appear under SavechM
5. Check the GHL contact — `github_repo_url` field should be populated

---

## What the Client Gets

A private GitHub repo at:
`https://github.com/SavechM/civados-[their-business-name]`

Contents:
- `README.md` — their personalised resource hub overview
- `prompts/lead-followup.md` — follow-up prompts with their details pre-filled
- `prompts/review-responses.md` — review templates for their business
- `workflows/missed-call-textback.md` — GHL setup guide for their business

All placeholder text replaced with their actual business name, location, services, phone number, and Google review link.

---

## Monetisation Ideas

This system adds real perceived value to your Civados packages:

- **Starter package:** Include the repo as a "done-for-you resource library" (costs you 0 minutes)
- **Premium package:** Ongoing updates — add new prompts and workflows each month
- **Agency white-label:** Rebrand this system and offer it to other agencies as a client onboarding add-on

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Repo not created | Check GITHUB_TOKEN is set correctly in Railway variables |
| Wrong client name in files | Check GHL field mapping in the webhook body |
| Workflow not triggering | Make sure the tag name matches exactly (case sensitive) |
| Make.com not receiving data | Check the webhook URL in GHL matches Make.com's webhook URL |

---

*Built by [Civados](https://civados.com) | Questions: hello@civados.com*
