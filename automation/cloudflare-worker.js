/**
 * Civados Client Repo Generator — Cloudflare Worker
 * ===================================================
 * Receives a webhook from GHL via Make.com,
 * creates a customised private GitHub repo for the new client,
 * and returns the repo URL.
 *
 * Deploy this in: Cloudflare Dashboard → Workers & Pages → Create Worker
 * Environment variables to set:
 *   GITHUB_TOKEN  — your GitHub personal access token
 *   GITHUB_ORG    — your GitHub username (SavechM)
 */

const GITHUB_API = "https://api.github.com";

// ── HELPERS ──────────────────────────────────────────────────────────────────

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .trim()
    .substring(0, 50); // GitHub repo name limit
}

function toBase64(str) {
  return btoa(unescape(encodeURIComponent(str)));
}

function fill(template, client) {
  const map = {
    "[BUSINESS NAME]"           : client.client_name,
    "[YOUR BUSINESS NAME]"      : client.client_name,
    "[BUSINESS TYPE]"           : client.business_type,
    "[YOUR BUSINESS TYPE]"      : client.business_type,
    "[YOUR NAME]"               : client.owner_name,
    "[OWNER NAME]"              : client.owner_name,
    "[LOCATION]"                : client.location,
    "[CITY/REGION]"             : client.location,
    "[SERVICE]"                 : client.services,
    "[SERVICES]"                : client.services,
    "[YOUR GOOGLE REVIEW LINK]" : client.google_review_link || "https://g.page/r/YOUR-LINK/review",
    "[GOOGLE REVIEW LINK]"      : client.google_review_link || "https://g.page/r/YOUR-LINK/review",
    "[YOUR NUMBER]"             : client.phone || "your phone number",
    "[PHONE]"                   : client.phone || "your phone number",
    "[YOUR WEBSITE]"            : client.website || "your website",
  };
  let result = template;
  for (const [key, val] of Object.entries(map)) {
    result = result.replaceAll(key, val);
  }
  return result;
}

// ── GITHUB API ────────────────────────────────────────────────────────────────

async function createRepo(name, description, token, org) {
  const res = await fetch(`${GITHUB_API}/user/repos`, {
    method: "POST",
    headers: {
      Authorization: `token ${token}`,
      Accept: "application/vnd.github.v3+json",
      "Content-Type": "application/json",
      "User-Agent": "Civados-Worker",
    },
    body: JSON.stringify({
      name,
      description,
      private: true,
      auto_init: false,
    }),
  });
  // 422 = already exists, that's fine
  if (res.status !== 201 && res.status !== 422) {
    const err = await res.text();
    throw new Error(`Failed to create repo: ${res.status} — ${err}`);
  }
  return true;
}

async function pushFile(repoName, filePath, content, token, org) {
  const url = `${GITHUB_API}/repos/${org}/${repoName}/contents/${filePath}`;
  const headers = {
    Authorization: `token ${token}`,
    Accept: "application/vnd.github.v3+json",
    "Content-Type": "application/json",
    "User-Agent": "Civados-Worker",
  };

  // Check if file already exists (need SHA to update)
  let sha;
  const existing = await fetch(url, { headers });
  if (existing.status === 200) {
    const data = await existing.json();
    sha = data.sha;
  }

  const body = {
    message: `Add ${filePath}`,
    content: toBase64(content),
    branch: "main",
  };
  if (sha) body.sha = sha;

  const res = await fetch(url, {
    method: "PUT",
    headers,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to push ${filePath}: ${res.status} — ${err}`);
  }
  return true;
}

// ── FILE CONTENT GENERATORS ───────────────────────────────────────────────────

function makeReadme(client) {
  const now = new Date().toLocaleDateString("en-GB", { month: "long", year: "numeric" });
  return fill(`# [BUSINESS NAME] — AI & Automation Resource Library

> Your private resource hub, set up and maintained by Civados.

**Business:** [BUSINESS NAME]
**Owner:** [OWNER NAME]
**Location:** [LOCATION]
**Services:** [SERVICES]
**Created:** ${now}

---

## What's In Here

This is your private library of AI tools, prompts, and automation workflows — built specifically for [BUSINESS NAME]. Everything is already customised for your business. Just copy, paste, and use.

| Section | What You'll Find |
|---|---|
| [/prompts](./prompts/) | AI prompts with your business details pre-filled |
| [/workflows](./workflows/) | Step-by-step GHL automation setup guides |
| [/resources](./resources/) | Tools and strategies for [BUSINESS TYPE] businesses |

---

## Quick Start (Do These First)

1. **prompts/lead-followup.md** — Copy SMS 1 and set it up in GHL today
2. **prompts/review-responses.md** — Use these every time you get a Google review
3. **workflows/missed-call-textback.md** — 20 minutes to set up, highest ROI automation

---

## Your Details (Already Pre-filled)

- Business: **[BUSINESS NAME]**
- Location: **[LOCATION]**
- Services: **[SERVICES]**
- Review link: **[YOUR GOOGLE REVIEW LINK]**
- Phone: **[YOUR NUMBER]**

---

*Managed by Civados | Questions? hello@civados.com*
`, client);
}

function makeLeadFollowup(client) {
  return fill(`# Lead Follow-Up Prompts — [BUSINESS NAME]

> Pre-filled for [BUSINESS NAME] in [LOCATION]. Copy and use directly in GHL.

---

## SMS 1 — Immediate (Within 5 Minutes)

\`\`\`
Hi {{contact.first_name}}, it's [OWNER NAME] from [BUSINESS NAME].

Thanks for reaching out about [SERVICES]. I'll be in touch shortly — what's the best time to give you a quick call?
\`\`\`

---

## SMS 2 — Day 2 (No Reply)

\`\`\`
Hey {{contact.first_name}} — just checking my message got through yesterday.

Happy to chat whenever suits. Reply here or call us on [YOUR NUMBER].

— [OWNER NAME], [BUSINESS NAME]
\`\`\`

---

## Email 1 — Day 1 (5 Minutes After SMS 1)

**Subject:** Your enquiry with [BUSINESS NAME]

\`\`\`
Hi {{contact.first_name}},

Thanks for getting in touch with [BUSINESS NAME] in [LOCATION].

We specialise in [SERVICES] and I'd love to help. Can I grab 15 minutes for a quick call?

[ADD YOUR BOOKING LINK HERE]

Speak soon,
[OWNER NAME]
[BUSINESS NAME] | [YOUR NUMBER]
\`\`\`

---

## Email 2 — Day 3 (Value Add, No Reply)

**Subject:** Quick tip on [SERVICES]

\`\`\`
Hi {{contact.first_name}},

One thing most people don't realise about [SERVICES]:

[ADD A GENUINE USEFUL TIP FOR YOUR NICHE HERE]

Happy to chat if useful — no pressure either way.

[OWNER NAME]
[BUSINESS NAME] | [LOCATION] | [YOUR NUMBER]
\`\`\`

---

## Final SMS — Day 7

\`\`\`
Hi {{contact.first_name}}, last message from me.

If you still need help with [SERVICES] in [LOCATION], just reply YES and I'll be in touch.

— [OWNER NAME], [BUSINESS NAME]
\`\`\`
`, client);
}

function makeReviewResponses(client) {
  return fill(`# Google Review Response Templates — [BUSINESS NAME]

> Ready to copy-paste. Add the customer name and one specific detail they mentioned.

---

## 5-Star Review (With Text)

\`\`\`
Thank you so much, [CUSTOMER NAME]! We really appreciate you taking the time to share your experience with [BUSINESS NAME].

[MENTION ONE THING THEY SAID] is something we always strive to get right, so it's great to hear it came through.

We look forward to helping you again — and please don't hesitate to refer us to anyone who needs [SERVICES] in [LOCATION]!

— [OWNER NAME] & the [BUSINESS NAME] team
\`\`\`

---

## 5-Star Review (Stars Only, No Text)

\`\`\`
Thank you for the 5 stars! We really appreciate your support of [BUSINESS NAME] here in [LOCATION]. Looking forward to helping you again soon!
— [OWNER NAME]
\`\`\`

---

## 4-Star Review

\`\`\`
Thank you for the feedback, [CUSTOMER NAME]. We're glad to hear [POSITIVE ELEMENT] worked well for you.

Your point about [THEIR CONCERN] is noted — we're always looking to improve.

We'd love to welcome you back next time you need [SERVICES]. Thanks for supporting a local [LOCATION] business!

— [OWNER NAME], [BUSINESS NAME]
\`\`\`

---

## Negative Review Response

\`\`\`
Thank you for your feedback, [CUSTOMER NAME]. I'm sorry to hear your experience didn't meet expectations.

This isn't the standard we hold ourselves to, and I'd genuinely like to make it right.

Please contact me directly on [YOUR NUMBER] so we can resolve this for you.

— [OWNER NAME], [BUSINESS NAME]
\`\`\`

---

## Your Google Review Link

**[YOUR GOOGLE REVIEW LINK]**

Add this link to: post-job SMS, email signature, invoices, business cards.

---

*Managed by Civados | hello@civados.com*
`, client);
}

function makeMissedCall(client) {
  return fill(`# GHL Workflow: Missed Call Text-Back — [BUSINESS NAME]

> Set up once. Runs forever. Estimated time: 20 minutes.

---

## What It Does

When [BUSINESS NAME] misses a call, GHL sends an automatic SMS within 60 seconds.

**Why:** 78% of customers go with whoever responds first. Most won't leave a voicemail — they'll just call a competitor.

---

## Setup Steps

**1. Create Workflow**
- GHL → Automation → Workflows → New Workflow
- Name: [BUSINESS NAME] — Missed Call Text-Back

**2. Trigger:** Missed Call (inbound only)

**3. Action 1 — Immediate SMS**

\`\`\`
Hi! Sorry I missed your call — it's [OWNER NAME] from [BUSINESS NAME].

What can I help you with? Reply here or call us back on [YOUR NUMBER].
\`\`\`

**4. Action 2 — Internal Notification (same time)**
- Email yourself: "Missed call from {{contact.phone}}. Auto-text sent."

**5. Action 3 — Wait 30 mins, then check**
- If replied → remove from workflow
- If no reply → send Action 4

**6. Action 4 — Second SMS (30 mins)**

\`\`\`
Still here! Happy to help with [SERVICES] in [LOCATION] or get you booked in.

Just reply here or call [YOUR NUMBER]. — [OWNER NAME]
\`\`\`

---

## Checklist Before Publishing

- [ ] Send window set to 8am–8pm [LOCATION] time
- [ ] Stop on reply: ON
- [ ] Stop if appointment booked: ON
- [ ] Tested with your own mobile number

---

*Managed by Civados | hello@civados.com*
`, client);
}

// ── MAIN HANDLER ──────────────────────────────────────────────────────────────

async function handleRequest(request, env) {
  // Only accept POST
  if (request.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  // Optional: simple auth check
  const authHeader = request.headers.get("X-Civados-Key");
  if (env.CIVADOS_SECRET && authHeader !== env.CIVADOS_SECRET) {
    return new Response("Unauthorised", { status: 401 });
  }

  let client;
  try {
    client = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON body" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Validate required fields
  const required = ["client_name", "business_type", "owner_name", "location", "services"];
  for (const field of required) {
    if (!client[field]) {
      return new Response(JSON.stringify({ error: `Missing field: ${field}` }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      });
    }
  }

  const token   = env.GITHUB_TOKEN;
  const org     = env.GITHUB_ORG || "SavechM";
  const slug    = slugify(client.client_name);
  const repoName = `civados-${slug}`;
  const description = `AI prompts and automation resources for ${client.client_name} — managed by Civados`;

  try {
    // 1. Create the repo
    await createRepo(repoName, description, token, org);

    // 2. Push all files
    const files = {
      "README.md"                         : makeReadme(client),
      "prompts/lead-followup.md"          : makeLeadFollowup(client),
      "prompts/review-responses.md"       : makeReviewResponses(client),
      "workflows/missed-call-textback.md" : makeMissedCall(client),
    };

    for (const [path, content] of Object.entries(files)) {
      await pushFile(repoName, path, content, token, org);
    }

    const repoUrl = `https://github.com/${org}/${repoName}`;

    return new Response(
      JSON.stringify({
        success   : true,
        repo_url  : repoUrl,
        repo_name : repoName,
        client    : client.client_name,
        files     : Object.keys(files),
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );

  } catch (err) {
    return new Response(
      JSON.stringify({ success: false, error: err.message }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}

// ── EXPORT ────────────────────────────────────────────────────────────────────

export default {
  async fetch(request, env) {
    return handleRequest(request, env);
  },
};
