# Why Blocking AI Crawlers Is Killing Your Visibility (And What to Do Instead)

**Category:** GEO & AEO Strategy  
**Reading time:** 8 minutes  
**Skill level:** Beginner — no technical knowledge required

---

There's a well-intentioned but damaging trend spreading through small business websites right now.

Owners and web developers — spooked by news stories about AI companies scraping content — are blocking AI crawlers. They're adding rules to their `robots.txt`, flipping switches in their CDN settings, and congratulating themselves on protecting their content.

They're also quietly disappearing from the places where their future customers are increasingly looking for recommendations.

This guide explains why **blocking AI crawlers is one of the most counterproductive things a small business can do in 2025**, what the actual risk model looks like, and how to set up a smart AI crawl policy that protects you while maximising your visibility in AI-generated search results.

---

## The New Search Landscape: GEO and AEO

Before getting into crawlers, it helps to understand what's changed.

When someone used to search for a service, they'd type a query into Google and scan a list of blue links. They'd click through, compare a few sites, and make a decision. Your job was to rank on page one.

That model is changing fast.

Increasingly, people ask AI tools directly: *"What's the best accountant in Bristol?"* or *"Can you recommend a marketing agency that specialises in restaurants?"* They get a direct answer — a specific recommendation — without clicking through to ten different websites.

This is called **Generative Engine Optimisation (GEO)** — the practice of optimising your online presence so that AI systems include you in their answers. A related discipline is **Answer Engine Optimisation (AEO)** — structuring your content so AI tools can easily extract and cite it.

The businesses winning these AI-generated recommendations share one thing in common: **AI crawlers can reach their content**.

---

## What AI Crawlers Actually Do

AI crawlers — bots like GPTBot (OpenAI), ClaudeBot (Anthropic), PerplexityBot, and BingBot (used for Copilot) — index your website content to train models and power real-time search features.

When they can crawl your site, a few things happen:

- Your business description, services, location, and expertise get incorporated into the model's understanding of what you do
- When a user asks a relevant question, the AI has your content to draw from when forming its answer
- Your brand name, URL, and service area become part of the citation trail

When they can't crawl your site — because you've blocked them — none of that happens. You're invisible to the AI. A competitor who hasn't blocked crawlers gets recommended instead.

It's the equivalent of telling Google not to index your site and then wondering why you don't rank.

---

## The Legitimate Concern — and Why It Doesn't Apply to Most Small Businesses

The fear driving the crawler-blocking trend is understandable: large publishers and content creators don't want their work used to train AI models without compensation or credit.

That's a real and reasonable concern — for publishers producing large volumes of original written content at commercial scale: news outlets, academic publishers, creative writing platforms.

For a **local service business** — a plumber, a marketing agency, a physiotherapy clinic, an accountant — the calculus is entirely different.

Your website exists to generate leads and establish trust. It contains your services, your location, your contact details, your testimonials, your expertise. That is exactly the information you want AI systems to have.

When a potential client in your city asks an AI assistant *"who does commercial cleaning in [your city]?"* — you want the AI to have read your site. You want it to know your name, your service area, your specialisms. You want to be in the answer.

Blocking GPTBot and PerplexityBot doesn't protect your content. It just removes you from the conversation.

---

## The Bots Worth Blocking vs. The Bots Worth Allowing

Not all AI crawlers deserve equal treatment. Here's the framework:

### Allow These (Critical for GEO/AEO Visibility)

| Bot | Used By |
|---|---|
| GPTBot, OAI-SearchBot | ChatGPT, OpenAI |
| ClaudeBot, Claude-User | Claude (Anthropic) |
| PerplexityBot, Perplexity-User | Perplexity AI |
| BingBot | Bing, Microsoft Copilot |
| Applebot | Apple Intelligence, Siri |
| DuckAssistBot | DuckDuckGo AI |
| MistralAI-User | Mistral AI |
| AmazonBot | Alexa, Amazon AI |

These are the AI systems your potential customers are actually using. Blocking any of them reduces your chances of appearing in AI-generated recommendations.

### Block These (No Business Value)

Some crawlers scrape content without providing any visibility benefit in return — often from companies with no meaningful user base, or from regions you don't serve. Bytespider (ByteDance/TikTok), PetalBot (Huawei), and various obscure scraping bots fall into this category. Blocking them costs you nothing in visibility terms.

The distinction is simple: **if a significant number of real people use that AI tool to get recommendations, you want that tool to have crawled your site**.

---

## How to Set Up a Smart AI Crawl Policy

The best tool for managing AI crawler access is **Cloudflare's AI Crawl Control** — available on the free plan.

### Step 1: Turn Off the Blunt Instrument

In Cloudflare, go to **Security → Bots**. You may see a setting called **Block AI Bots** — turn this OFF if it's enabled. This setting blocks everything indiscriminately, including the major crawlers you want.

Instead, you'll use AI Crawl Control for precise, per-bot management.

### Step 2: Use AI Crawl Control

Go to **Security → AI Crawl Control** (or search for it in the dashboard). Here you'll see a list of known AI crawlers with individual allow/block toggles.

Set the major AI crawlers listed above to **Allow**. Set scrapers with no visibility value to **Block**.

This gives you the best of both worlds: visibility in AI search results from the platforms that matter, without feeding low-value scrapers that offer nothing in return.

### Step 3: Create a robots.txt That Signals Openness

Your `robots.txt` file is one of the first things AI crawlers check. A well-configured file signals that you're AI-ready and cooperative.

For a small business that wants maximum AI visibility:

```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: *
Allow: /
```

Explicitly allowing the major AI crawlers — rather than just relying on the wildcard `*` — sends a clearer signal and ensures compatibility even if a crawler defaults to conservative behaviour.

### Step 4: Create an llms.txt File

An emerging standard for AI-ready websites is the `llms.txt` file — placed at `yourdomain.com/llms.txt`. It works similarly to `robots.txt` but is specifically designed to help AI systems understand your site's content structure.

A basic `llms.txt` for a small service business looks like this:

```
# Civados

> Civados helps local service businesses build AI-ready digital infrastructure — websites, automation, and security.

## Services
- [AI Automation for Local Business](/services/ai-automation)
- [Website & Security Setup](/services/infrastructure)
- [Google Workspace Configuration](/services/google-workspace)

## About
- [About Civados](/about)
- [Contact](/contact)
```

This file gives AI systems a clean, structured summary of who you are and what you do — significantly increasing the likelihood of accurate, favourable representation in AI-generated answers.

---

## The Entity Signal Connection

Allowing AI crawlers isn't just about direct AI recommendations. It connects to the broader concept of **entity building** — the practice of creating consistent, cross-platform signals that help both Google and AI systems understand your business is real, established, and relevant.

Every time a legitimate AI crawler indexes your site and finds consistent information — your business name, location, services, contact details — it reinforces your entity. That has downstream effects on traditional search rankings as well as AI visibility.

Businesses that block AI crawlers are not only absent from AI recommendations. They're also weakening their entity signals at exactly the moment those signals are becoming more important.

---

## The Competitive Advantage Window Is Open Now

Most small businesses haven't thought carefully about AI crawler policy. They've either blocked everything out of fear or done nothing at all.

That creates a short window where deliberate action gives a meaningful advantage. The businesses that configure intelligent AI crawl policies now — allowing the right bots, creating `llms.txt` files, structuring content for AI readability — will have stronger AI visibility when the market fully shifts to AI-mediated search.

That window won't be open forever. The businesses who move early will be the hardest to displace.

---

## Need This Set Up Properly?

AI crawl policy, `robots.txt` configuration, and `llms.txt` creation are part of the **AI-ready infrastructure** setup Civados builds for local service businesses. Combined with entity building, structured data, and security hardening, it's a complete foundation for visibility in both traditional and AI-powered search.

If you want this done correctly from day one, [talk to Civados](https://civados.com).

---

*Civados helps local service businesses build AI-ready digital infrastructure — websites, email, automation, and security — without the complexity.*
