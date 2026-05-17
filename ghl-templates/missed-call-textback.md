# GHL Template: Missed Call Text-Back

> One of the highest-ROI automations you can set up. When you miss a call, GHL automatically sends an SMS within 60 seconds. Studies show 78% of customers buy from whoever responds first.

---

## What This Does

When your business misses an inbound call, this workflow instantly:

1. Sends an SMS to the caller within 60 seconds
2. Starts a simple 2-message follow-up if they don't reply
3. Notifies you (the owner/team) so you can call back manually

**Impact:** Businesses using missed call text-back typically recover 20-30% of missed calls that would otherwise be lost.

---

## Prerequisites

- GoHighLevel account with LC Phone or Twilio connected
- Missed call trigger enabled (it's built into GHL)
- Your business phone number forwarded through GHL or set as your GHL number

---

## Workflow Setup

### Step 1 — Create the Workflow

1. Go to **Automation → Workflows → + New Workflow**
2. Name it: `Missed Call Text-Back`
3. Status: Draft while building

---

### Step 2 — Set the Trigger

**Trigger:** Missed Call

- This is a native GHL trigger — no extra setup needed
- Filter: Only trigger for inbound calls (not outbound)

---

### Step 3 — Build the Sequence

#### **Action 1 — Immediate: Send SMS to Caller**
- Delay: 0 (immediate — speed is critical here)
- Type: SMS
- Message:

```
Hi, it's [YOUR NAME] from [BUSINESS NAME]. Sorry I missed your call! 

What can I help you with? Reply here and I'll get back to you straight away.
```

> Keep this short. One question. The goal is to start a conversation, not sell anything.

---

#### **Action 2 — Immediate: Internal Notification to Owner**
- Delay: 0 (simultaneous with Action 1)
- Type: Internal notification / email to owner
- Message:

```
Missed call from {{contact.phone}} ({{contact.first_name}} {{contact.last_name}})

Auto-text sent. Follow up manually if no reply within 15 minutes.
```

---

#### **Action 3 — Wait: Check for Reply**
- Delay: 30 minutes
- Type: If/Else Branch
- Condition: Contact has replied to SMS

  - **YES:** Remove from workflow → Add tag `missed-call-responded` → (optional) move to booking workflow
  - **NO:** Continue to Action 4

---

#### **Action 4 — 30 Minutes: Second SMS (If No Reply)**
- Delay: 30 minutes from Action 1
- Type: SMS
- Message:

```
Still here if you need anything, {{contact.first_name}}! 

Happy to answer questions or get you booked in. Just reply here or call us back on [YOUR NUMBER].
```

---

#### **Action 5 — End: Tag + Notify**
- Add tag: `missed-call-no-response`
- Send internal notification: "No response to missed call text-back for {{contact.phone}} — manual follow-up recommended."

---

### Step 4 — Test It

1. Call your GHL number from a different phone
2. Don't answer
3. Confirm the text-back arrives within 60 seconds
4. Reply to the SMS and confirm the workflow stops
5. Publish

---

## Settings to Check

| Setting | Value |
|---|---|
| Only trigger during business hours | Optional — many businesses send 24/7 and it works fine |
| Stop on reply | YES |
| Stop if appointment booked | YES |
| Only trigger for new contacts | Optional |

---

## Customise for Your Business

**Service business (plumber, electrician, cleaner):**
```
Hi! Sorry I missed you — [BUSINESS NAME] here. What can I help with? Reply or call [NUMBER] and we'll get you sorted.
```

**Health / Wellness:**
```
Hi {{contact.first_name}}, thanks for calling [BUSINESS NAME]. I'm sorry I missed you! 

What were you looking to book? Reply here and I'll help you get started.
```

**Professional services (accountant, lawyer, consultant):**
```
Hello, this is [NAME] from [FIRM]. Apologies for missing your call. 

Please reply here with a brief description of what you need and I'll respond shortly.
```

---

## Why This Works

- **Speed:** 78% of customers go with whoever responds first
- **SMS open rate:** 98% within 3 minutes
- **No voicemail:** Most people under 45 won't leave one — they'll just call a competitor
- **Low effort:** Once set up, it runs forever with zero maintenance

---

*More templates at [github.com/civados](https://github.com/civados) | [civados.com](https://civados.com)*
