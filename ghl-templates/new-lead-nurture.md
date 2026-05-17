# GHL Template: New Lead 7-Day Nurture Sequence

> A fully documented GoHighLevel workflow for automatically following up with new inbound leads over 7 days. No coding required.

---

## What This Does

When a new lead comes in (from your website, Facebook ad, Google ad, or any form), this workflow automatically sends a sequence of messages over 7 days to:

1. Confirm their enquiry instantly
2. Build rapport and trust
3. Encourage them to book a call or appointment
4. Handle objections before they arise
5. Leave the door open if they're not ready yet

**Conversion benchmark:** A well-built nurture sequence typically converts 20-40% of leads who didn't respond to the first message.

---

## Prerequisites

- Active GoHighLevel account
- At least one lead source connected (web form, Facebook, Google, etc.)
- Twilio (SMS) or LC Phone connected for SMS sending
- Email sender domain verified

---

## Workflow Setup

### Step 1 — Create the Workflow

1. Go to **Automation → Workflows → + New Workflow**
2. Name it: `New Lead — 7 Day Nurture`
3. Set status to **Draft** while building

---

### Step 2 — Set the Trigger

**Trigger:** Contact Tag Added

- Tag: `new-lead`
- OR use: Form Submitted / Survey Submitted / Funnel Page Visited (whichever applies to your lead source)

**Filter:** Source = [your lead source name]

> Tip: Create a trigger for each lead source separately if they need different messaging.

---

### Step 3 — Build the Sequence

#### **Action 1 — Immediate: Send SMS**
- Delay: 0 minutes (immediate)
- Type: SMS
- Message:

```
Hi {{contact.first_name}}, it's [YOUR NAME] from [BUSINESS NAME]. 

Thanks for reaching out about [SERVICE]. I'll be in touch shortly — is there a best time to give you a quick call?
```

---

#### **Action 2 — Immediate + 5 minutes: Send Email**
- Delay: 5 minutes
- Type: Email
- Subject: `Your enquiry with [BUSINESS NAME]`
- Body:

```
Hi {{contact.first_name}},

Thanks for getting in touch. I've received your enquiry about [SERVICE] and wanted to reach out personally.

[1-2 sentences about what you do and the result you help people get]

I'd love to set up a quick 15-minute call to understand what you're looking for. 

[CALENDLY LINK or CALL US AT: PHONE NUMBER]

Speak soon,
[YOUR NAME]
[BUSINESS NAME]
```

---

#### **Action 3 — Day 1: If/Else Branch**

Check: Has contact replied to SMS or email?

- **YES path:** Add tag `lead-engaged` → Remove from this workflow → Move to Booked Call workflow
- **NO path:** Continue to next step

---

#### **Action 4 — Day 2: Send SMS**
- Delay: 1 day after Action 1
- Type: SMS
- Message:

```
Hey {{contact.first_name}} — just checking my message got through yesterday. Happy to jump on a quick call whenever suits. 

Reply here or grab a time: [LINK]
```

---

#### **Action 5 — Day 3: Send Email (Value Add)**
- Delay: 2 days after Action 1
- Type: Email
- Subject: `Quick tip for [RELEVANT TOPIC]`
- Body: [Use the Day 3 Value Add prompt from the lead-followup.md prompts file]

---

#### **Action 6 — Day 5: Send SMS**
- Delay: 4 days after Action 1
- Type: SMS
- Message:

```
Hi {{contact.first_name}}, I know life gets busy. If you're still thinking about [SERVICE], I'm here whenever you're ready. 

No pressure — just reply YES if you'd like me to reach out, or NO to be removed. 🙂
```

---

#### **Action 7 — Day 7: Final Email**
- Delay: 6 days after Action 1
- Type: Email
- Subject: `Last one from me, {{contact.first_name}}`
- Body:

```
Hi {{contact.first_name}},

I don't want to crowd your inbox, so this will be my last message for now.

If the timing wasn't right, no worries at all. If you ever want to revisit [SERVICE], I'm here.

You can always reach us at [PHONE/EMAIL] or book a time here: [LINK]

Wishing you well,
[YOUR NAME]
[BUSINESS NAME]
```

---

#### **Action 8 — Day 7 End: Add Tag**
- Tag: `nurture-complete-no-response`
- This puts them into a separate list for a re-engagement campaign in 30-60 days

---

### Step 4 — Activate & Test

1. Save the workflow
2. Create a test contact with your own mobile and email
3. Manually add the trigger tag to the test contact
4. Confirm all messages arrive correctly and at the right times
5. Set workflow status to **Published**

---

## Key Settings to Check

| Setting | Recommended Value |
|---|---|
| Send window (SMS) | 8am–8pm local time |
| Send window (Email) | 7am–7pm local time |
| Stop on reply | YES — always |
| Stop on appointment booked | YES |
| Unsubscribe handling | Follow GHL default |

---

## What to Track

- **Open rate (email):** Target 35%+
- **Reply rate (SMS):** Target 15%+
- **Conversion rate (lead to booked call):** Target 20-35%
- **Opt-out rate:** Should be under 3%

---

## Common Mistakes

- Sending too many messages too fast (looks desperate)
- Not stopping the sequence when someone replies
- Generic messages with no personalisation
- Not testing before going live
- Forgetting to set send windows (sending at 3am)

---

*More templates at [github.com/civados](https://github.com/civados) | Full setup help at [civados.com](https://civados.com)*
