# Deploy on Cloudflare Workers — Setup Guide

> No server. No monthly fee. Already in your Cloudflare account. Takes about 10 minutes.

---

## Step 1 — Create the Worker

1. Log into [dash.cloudflare.com](https://dash.cloudflare.com)
2. In the left sidebar click **Workers & Pages**
3. Click **Create** → **Create Worker**
4. Give it a name: `civados-repo-generator`
5. Click **Deploy** (ignore the default code for now)

---

## Step 2 — Paste the Code

1. On the next screen click **Edit Code**
2. **Select all** the existing code in the editor and **delete it**
3. Copy the entire contents of `cloudflare-worker.js` (from this repo)
4. Paste it into the editor
5. Click **Deploy** (top right)

You'll get a URL that looks like:
`https://civados-repo-generator.YOUR-SUBDOMAIN.workers.dev`

**Copy this URL — you'll need it for GHL and Make.com.**

---

## Step 3 — Add Your Environment Variables

This is where you give the Worker your GitHub token (securely — it never appears in the code).

1. Go back to your Worker's overview page
2. Click **Settings** → **Variables and Secrets**
3. Click **Add variable** for each of these:

| Variable Name | Value | Type |
|---|---|---|
| `GITHUB_TOKEN` | Your GitHub token (`ghp_...`) | Secret |
| `GITHUB_ORG` | `SavechM` | Text |
| `CIVADOS_SECRET` | Make up a password e.g. `civ-2026-secure` | Secret |

> The `CIVADOS_SECRET` is optional but recommended — it stops anyone else from calling your Worker.

4. Click **Save and Deploy**

---

## Step 4 — Test It

Open a terminal (or use an online tool like [reqbin.com](https://reqbin.com)) and send a test request:

**Test JSON to send:**
```json
{
  "client_name": "Test Plumbing Co",
  "business_type": "plumbing",
  "owner_name": "John",
  "location": "Manchester",
  "services": "emergency plumbing, boiler repair",
  "phone": "0161 000 0000",
  "google_review_link": "https://g.page/r/TEST/review",
  "website": "https://testplumbing.co.uk"
}
```

**Send it to:** `https://civados-repo-generator.YOUR-SUBDOMAIN.workers.dev`

**Expected response:**
```json
{
  "success": true,
  "repo_url": "https://github.com/SavechM/civados-test-plumbing-co",
  "repo_name": "civados-test-plumbing-co",
  "client": "Test Plumbing Co",
  "files": ["README.md", "prompts/lead-followup.md", "prompts/review-responses.md", "workflows/missed-call-textback.md"]
}
```

Check your GitHub — the private repo should appear within a few seconds.

---

## Step 5 — Wire Up GHL + Make.com

### In GoHighLevel

**First — add these custom fields to contacts:**
- Settings → Custom Fields → Contacts → Add:
  - `business_type` (Text)
  - `services` (Text)
  - `google_review_link` (Text)
  - `github_repo_url` (Text) ← this gets auto-filled by the automation

**Then — create the workflow:**
1. Automation → Workflows → New Workflow
2. Name: `New Client — Repo Generator`
3. **Trigger:** Contact Tag Added → Tag: `civados-client`
4. **Action:** Webhook
   - URL: your Cloudflare Worker URL
   - Method: POST
   - Header: `X-Civados-Key` = your CIVADOS_SECRET value
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
5. **Action 2:** Update Contact Field
   - Field: `github_repo_url`
   - Value: (the repo_url from the webhook response)

### In Make.com (Optional — if you want to store the response back in GHL)

GHL's native webhook action doesn't always capture the response cleanly. Make.com handles this better:

1. Create a new scenario
2. **Module 1:** Webhooks → Custom Webhook (get a Make.com URL)
   - Use THIS URL as your GHL webhook destination instead
3. **Module 2:** HTTP → Make a Request
   - URL: your Cloudflare Worker URL
   - Method: POST
   - Add header: `X-Civados-Key` = your secret
   - Body: pass through from Module 1
4. **Module 3:** GoHighLevel → Update Contact
   - Contact ID: from Module 1 data
   - `github_repo_url`: `{{2.repo_url}}` (from the HTTP response)

---

## What Happens End-to-End

```
You tag a contact "civados-client" in GHL
            ↓
GHL sends their details to Make.com webhook
            ↓
Make.com calls your Cloudflare Worker
            ↓
Worker creates private GitHub repo in ~5 seconds
            ↓
Worker returns the repo URL
            ↓
Make.com writes the URL back to the GHL contact
            ↓
You share the repo link with the client at onboarding
```

**Your time per client: 0 minutes.**

---

## Troubleshooting

| Problem | Check |
|---|---|
| Worker returns 401 | Your `X-Civados-Key` header doesn't match `CIVADOS_SECRET` |
| Worker returns 500 | Check `GITHUB_TOKEN` is set and not expired |
| Repo not appearing | GitHub username in `GITHUB_ORG` must match exactly |
| GHL fields empty | Make sure contact has company_name and city filled in |
| Make.com not triggering | Check the webhook URL in GHL matches Make.com's URL |

---

## Cost

| Service | Cost |
|---|---|
| Cloudflare Workers | **Free** (100,000 requests/day) |
| GitHub private repos | **Free** (unlimited on free plan) |
| Make.com | **Free** tier (1,000 operations/month — enough for ~100 clients) |

Total: **£0/month** until you're onboarding hundreds of clients.

---

*Built by Civados | hello@civados.com*
