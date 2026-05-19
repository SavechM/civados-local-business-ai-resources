# Google Workspace Setup for a Lean Service Business (The Right Way)

**Category:** Business Infrastructure & Email Security  
**Reading time:** 10 minutes  
**Skill level:** Beginner — no technical knowledge required

---

Most small service businesses set up email once and never think about it again. They use a free Gmail account, or the basic email that came with their hosting package, and assume that's good enough.

It isn't — and the gap between "good enough" and "done properly" has real consequences: emails landing in spam, accounts getting compromised, no clear separation between personal and business communications, and zero audit trail when something goes wrong.

**Google Workspace** — Google's paid business email and productivity suite — solves all of this. But the way most people set it up leaves half the value on the table.

This guide covers the account structure, DNS authentication records, and security controls that a lean service business actually needs. Not theoretical best practices — the specific setup that works.

---

## Why Google Workspace and Not Free Gmail

The short version: free Gmail is a personal product. Google Workspace is a business product. The difference matters more than the price.

With Google Workspace you get:
- **Email on your own domain** — `you@yourbusiness.com` instead of `yourbusiness@gmail.com`. This alone has a significant impact on how professional you appear to clients and, critically, how mail servers treat your emails
- **Admin controls** — you manage all accounts centrally, can reset passwords, suspend compromised accounts, and audit activity
- **SPF, DKIM, and DMARC support** — email authentication records that dramatically improve deliverability and protect your domain from being spoofed in phishing attacks
- **Shared drives and collaborative access** — files owned by the business, not by an individual's personal account
- **2FA enforcement** — you can require two-factor authentication across all accounts, not just hope people enable it themselves

For a service business sending proposals, invoices, and client communications, email deliverability and professionalism are not optional concerns. They directly affect whether you get paid and whether clients trust you.

---

## The Account Structure That Actually Works

Most small businesses make one of two mistakes: they create one shared inbox that everyone logs into, or they create a separate Google Workspace account for every person and end up with no coherent structure.

The better approach is a **named account system** with defined purposes. Here's the structure that works for a lean service business of one to five people:

### Account 1: Superadmin (ops@)
`ops@yourbusiness.com`

This account has full administrative control over the workspace. It is used **only** for admin tasks — creating accounts, changing settings, recovering access. It is never used for day-to-day email, never connected to any third-party tool, and never shared.

Think of it as the master key. You use it rarely, keep it locked up, and treat it with extra care. Enable two-factor authentication with an authenticator app (not SMS) and store the password somewhere secure and separate from everything else.

### Account 2: Owner / Daily Driver
`yourname@yourbusiness.com`

This is your personal business inbox. Client correspondence, proposals, relationship-building — anything tied to you as an individual lives here. Keep it clean and purpose-specific.

### Account 3: Operations & Integrations
`ops-auto@yourbusiness.com` or `civilitas@yourbusiness.com`

Every third-party tool your business uses — your CRM, automation platform, API integrations, AI tools — authenticates with this account. This separation is critical for two reasons:

First, it creates a clean audit trail. When you check which apps have access to your business data, it's all in one place rather than scattered across personal accounts.

Second, if a tool is compromised or behaves unexpectedly, you can revoke access from one account without disrupting your personal email or your client-facing communications.

### Account 4: Social & Public Presence
`social@yourbusiness.com`

All social media platforms — LinkedIn, Instagram, Facebook, X — are registered to this account. If a social platform gets compromised (it happens), the blast radius is contained. Your business email, your CRM, your client communications are all on separate accounts that are unaffected.

### Account 5: Support / Collaborative Inbox
Set up as a **Google Group with Collaborative Inbox** rather than a standard account.

`hello@yourbusiness.com` or `support@yourbusiness.com`

A Google Group inbox allows multiple people to access the same inbox without sharing a password — you add members individually, each with their own login. This is how you scale support or handle enquiries without creating security vulnerabilities. Add aliases like `contact@`, `info@`, and `noreply@` to the same group.

---

## The DNS Records That Most People Skip

This is where most Google Workspace setups are incomplete — and where email deliverability actually gets won or lost.

When you send an email, the receiving mail server checks several records to decide whether to trust it. Without these records properly configured, your emails are significantly more likely to land in spam, or to be outright rejected.

Log into your DNS provider (Cloudflare, if you're set up well) and add the following:

### MX Records — Where Your Email Goes

These tell the internet that email for your domain should be delivered to Google's servers. You need five of them:

| Priority | Mail Server |
|---|---|
| 1 | ASPMX.L.GOOGLE.COM |
| 5 | ALT1.ASPMX.L.GOOGLE.COM |
| 5 | ALT2.ASPMX.L.GOOGLE.COM |
| 10 | ALT3.ASPMX.L.GOOGLE.COM |
| 10 | ALT4.ASPMX.L.GOOGLE.COM |

Add only these five. Remove any others — legacy or hosting-provided MX records that linger can cause delivery issues.

### SPF Record — Who Is Allowed to Send Email As You

SPF (Sender Policy Framework) tells receiving servers which mail servers are authorised to send email from your domain. If someone tries to spoof your domain in a phishing email, a properly configured SPF record helps get that email rejected.

Add a TXT record on your root domain (`@`):

```
v=spf1 include:_spf.google.com ~all
```

This says: only Google's servers are authorised to send email from this domain.

### DKIM Record — Cryptographic Email Signing

DKIM (DomainKeys Identified Mail) adds a cryptographic signature to every outgoing email. The receiving server checks the signature against a public key published in your DNS. If they match, the email is confirmed as genuinely from you.

Generate this inside Google Workspace Admin Console: **Apps → Google Workspace → Gmail → Authenticate email → Generate new record**. Copy the Name and Value and add them as a TXT record in your DNS.

### DMARC Record — Policy and Reporting

DMARC (Domain-based Message Authentication Reporting and Conformance) ties SPF and DKIM together and tells receiving servers what to do when an email fails those checks.

Add a TXT record on `_dmarc.yourdomain.com`:

```
v=DMARC1; p=quarantine; rua=mailto:[your-reporting-address]
```

Start with `p=quarantine` — this sends failing emails to spam rather than rejecting them outright, giving you a safety margin while you verify everything is working. Once you've confirmed legitimate emails are passing, upgrade to `p=reject`.

For the `rua` address, use a free DMARC reporting service like Postmark's DMARC tool. It processes the XML reports Google and other servers send you and presents them in a readable format. This is how you monitor whether anyone is spoofing your domain.

**After setting up all three records**, test them using [mail-tester.com](https://mail-tester.com) — send a test email and it gives you a deliverability score with specific pass/fail results for each record.

---

## Security Controls You Actually Need to Enable

### Enforce Two-Factor Authentication Across All Accounts

In Google Workspace Admin Console: **Security → 2-Step Verification → Enforcement → On for all users**.

This means every account in your workspace must have 2FA enabled — it's not optional. Use an authenticator app (Google Authenticator, Authy) rather than SMS codes, which can be intercepted via SIM-swapping attacks.

### Lock Down the Superadmin Account

The ops/superadmin account deserves extra steps:
- Never use it for day-to-day email
- Never connect it to third-party apps or integrations
- Log in only when you need to make admin changes, then log out
- Store the password separately from your other passwords
- Set a recovery email and phone and keep them current

If this account is compromised, an attacker has full control of your entire Google Workspace. Treat it accordingly.

### Quarterly Connected Apps Review

Third-party apps that connect to your Google Workspace accumulate over time. Tools you tried and stopped using. Integrations from old projects. Each connected app is a potential attack surface.

Every quarter: **Security → Access and data control → API controls → Manage third-party app access**. Review every connected app. Revoke anything you no longer use.

---

## A Note on Shared Drives vs. Personal Drive

One structural decision that pays dividends later: store all business files in **Shared Drives**, not in individual accounts' personal Google Drive.

Files in a personal Drive are owned by that account. If you close the account, lose access, or have an employee leave, the files become inaccessible or lost.

Files in a Shared Drive are owned by the workspace — they persist regardless of what happens to individual accounts. Create a Shared Drive for your business from day one and keep all client files, templates, and internal documents there.

---

## What "Done Properly" Looks Like

When Google Workspace is set up correctly for a service business, here's the end state:

- Five (or fewer) accounts with clear, non-overlapping purposes
- MX, SPF, DKIM, and DMARC records all configured and verified passing
- 2FA enforced at the organisation level
- Superadmin account locked down and used only for admin tasks
- All third-party tools connected through the operations account
- Social platforms on their own isolated account
- Client support handled through a Google Group Collaborative Inbox
- All business files in Shared Drives, not personal accounts

This takes an afternoon to set up properly. Once it's done, you have a business email infrastructure that's more secure, more deliverable, and more scalable than the vast majority of small businesses — including most of your direct competitors.

---

## Need It Done for You?

Google Workspace setup — including DNS configuration, SPF/DKIM/DMARC verification, account structure, and security hardening — is part of the core infrastructure package at **Civados**.

We set it up once, document it properly, and make sure it's running correctly before we hand it over. No guesswork, no half-configured records quietly failing in the background.

[Get in touch with Civados](https://civados.com) if you'd rather have it done right than figure it out yourself.

---

*Civados helps local service businesses build AI-ready digital infrastructure — websites, email, automation, and security — without the complexity.*
