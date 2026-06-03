# Helix AI — New Employee Onboarding Guide
**Your First 30 Days**  
**People Operations Team**  
**Last Updated: February 2026**

---

Welcome to Helix. We're glad you're here.

This guide covers everything you need to get set up, productive, and connected in your first 30 days. Read it front to back on day one — it'll save you a lot of "wait, where does that live?" questions later.

If something's wrong, outdated, or unclear, open a PR against the onboarding repo (github.com/helix-internal/onboarding-docs). We update this guide continuously.

---

## Before Day 1

HR will send you a welcome email 5 business days before your start date with:
- Your @helix.ai Google account credentials (temporary password, must change on first login)
- Instructions for shipping your company laptop (MacBook Pro M4 Pro, 36GB RAM — yes, the good one)
- Your offer letter and benefits enrollment link (benefits must be elected within 30 days of start date)

Your laptop ships pre-configured with Jamf MDM, CrowdStrike EDR, Tailscale VPN, and 1Password. Do not wipe it or disable any of these tools.

---

## Day 1: Getting Set Up

### Morning: IT & Access

Your first stop is the #it-helpdesk Slack channel. Post your name and start date and the IT team will provision your accounts. Standard provisioning takes about 2 hours. You'll receive access to:

- Google Workspace (email, calendar, drive, meet)
- Slack (helix-internal.slack.com)
- GitHub (github.com/helix-internal org — accept the email invite)
- Notion (wiki, docs, meeting notes)
- Linear (project management)
- Figma (design team gets Pro, engineering gets viewer)
- AWS console (read-only by default; request additional access through IT)

If you need access to something not on this list, request it through the IT service desk in Jira (project: IT-ACCESS). Most requests are fulfilled within 1 business day.

### Set Up 1Password
1Password Teams is mandatory for all credentials. Your invitation arrives in your Helix email. Set up your master password and store it somewhere safe — we cannot recover it for you. Install the browser extension and desktop app. Migrate any work credentials you're storing elsewhere into 1Password.

### Set Up Tailscale VPN
Install Tailscale from the App Store or tailscale.com/download. Sign in with your @helix.ai Google account. VPN connects automatically when you're on a network other than the Helix office. You'll need VPN active to access internal tools like the staging environment, internal dashboards, and the database console.

### Set Up YubiKey
Your YubiKey ships with your laptop. Register it as your MFA method for Google Workspace, GitHub, and AWS. Instructions are in the IT setup guide pinned in #it-helpdesk. SMS MFA is not permitted.

---

## Your First Week

### Meet Your Manager (Day 1)
Your manager will schedule a 45-minute welcome call on day 1. Come prepared with: your high-level goals for the first 30 days as you understand them, any questions about your role, and any tools or access you think you'll need.

### Team Introduction (Week 1)
Your manager will introduce you in the team Slack channel and arrange 1:1s with your immediate teammates. These are 25-minute casual calls — no agenda required. The goal is to understand what everyone is working on and how you'll collaborate.

### Company All-Hands (Every Other Monday, 10 AM PT)
All-Hands is mandatory for all employees. It's 45 minutes: company updates from the CEO, team highlights, new hire introductions, and open Q&A. Calendar invite will appear in your Google Calendar automatically.

### Read These Documents (Week 1)
Find these in Notion under Company > Core Documents:
- **Helix Product Vision** — where we're going and why
- **Engineering Principles** — how we make technical decisions
- **Communication Norms** — async-first, when to use Slack vs email vs a meeting
- **Incident Runbook** — what to do if something breaks
- **Architecture Overview** — how the product is built (engineering new hires only)

### Complete Security Training (Within 30 Days)
You'll receive a KnowBe4 training invitation in your email. Complete it within 30 days of your start date. It takes about 90 minutes and covers phishing, data handling, and device security. Non-completion is escalated to your manager after the deadline.

---

## How We Work

### Communication
Helix is async-first. Default to writing things down over calling a meeting. When you do need a meeting, include an agenda.

- **Slack** — Day-to-day communication, quick questions, team banter. Not for decisions or anything that needs to be findable later.
- **Notion** — Documentation, meeting notes, RFCs, project plans. If it matters, it lives in Notion.
- **Linear** — Engineering tasks, bugs, and sprint tracking. All engineering work gets a ticket.
- **Email** — External communication and formal HR/finance matters. We do not use email internally for project communication.
- **Google Meet** — Meetings. Record important ones and drop the link in Notion.

Slack response time expectations: within 4 hours during your working hours. You are not expected to respond outside your working hours — set your Slack status and notification schedule accordingly.

### Working Hours and Flexibility
Helix does not track hours. We track output. Your working hours are flexible with two constraints: you must be available for team meetings (check your calendar before booking a vacation day), and you must be reachable during a 4-hour overlap window with your team (for most US-based employees this is 10 AM–2 PM PT).

### Time Off
Helix has unlimited PTO. This is not a trap — leadership actively encourages people to take at least 15 days per year. To take time off: add it to your Google Calendar, notify your manager in Slack, and ensure your work is covered. No approval required for up to 5 consecutive days; manager approval needed for longer.

### Performance
Performance reviews are quarterly (March, June, September, December). You'll set goals at the start of each quarter in Notion using the Helix Goals template. Your manager reviews progress mid-quarter and gives written feedback at quarter-end. Compensation reviews happen annually in January.

---

## Engineering-Specific Setup (Engineering New Hires Only)

### Local Development
Clone the main repositories from github.com/helix-internal. Setup instructions for each repo live in the root CONTRIBUTING.md. The main product stack is:
- Backend: Python 3.12, FastAPI, PostgreSQL 16
- Frontend: React 19, TypeScript, Tailwind CSS
- Infrastructure: Terraform, AWS, EKS (Kubernetes 1.29)
- CI/CD: GitHub Actions + ArgoCD

Do not commit directly to main. All work goes through pull requests with at least one reviewer. Use conventional commits format for commit messages.

### Your First PR
Your first week goal is to ship a real PR — even a small one. Bug fix, documentation improvement, test coverage, refactor. Something real. This gets you familiar with the review process and signals to the team that you're operational.

### On-Call Rotation
Engineers join the on-call rotation after 90 days. On-call is one week per rotation (approximately every 8 weeks depending on team size). You'll be on secondary on-call for your first rotation (shadowing the primary), and primary thereafter. PagerDuty will notify you when you're on-call.

---

## Benefits Summary

Full details are in the benefits enrollment portal (link in your welcome email). Key items:

- **Health insurance** — Medical (Blue Shield, Anthem, or Kaiser depending on location), dental, and vision. Helix covers 100% of employee premiums and 75% of dependent premiums.
- **401(k)** — 4% company match, vests immediately. Administered by Fidelity. Enroll at fidelity.com/atwork.
- **Equity** — Your offer letter includes your stock option grant. Options vest over 4 years with a 1-year cliff. Exercise window is 10 years from grant date (not 90 days — we believe in employee-friendly equity).
- **Home office stipend** — $1,500 on hire for home office setup, $500/year thereafter. Submit receipts through Expensify.
- **Learning budget** — $2,000/year for courses, books, conferences. Manager approval required for amounts over $500. Submit through Expensify.
- **Mental health** — Unlimited sessions with licensed therapists via Spring Health, covered 100%.

Benefits questions: benefits@helix.ai or the #people-ops Slack channel.

---

## Who To Know

**People Operations:** people@helix.ai, #people-ops — onboarding, benefits, HR questions  
**IT Helpdesk:** #it-helpdesk — access, devices, software  
**Security Team:** security@helix.ai, #security-alerts — anything security-related  
**Finance:** finance@helix.ai — expenses, reimbursements, invoices  
**Legal:** legal@helix.ai — contracts, NDAs, compliance questions  

Your manager is your first stop for anything role-related. They'll direct you from there.

---

## 30-Day Checklist

- [ ] All accounts provisioned and logged into
- [ ] YubiKey registered on all accounts
- [ ] 1Password set up with all credentials migrated
- [ ] Tailscale VPN active
- [ ] Security training completed (KnowBe4)
- [ ] 1:1s completed with all immediate teammates
- [ ] Core documents read (Notion > Company > Core Documents)
- [ ] First PR merged (engineering only)
- [ ] Benefits enrolled (deadline: 30 days from start)
- [ ] 401(k) enrollment started (Fidelity)
- [ ] Home office stipend submitted (if applicable)
- [ ] 30-day check-in with manager completed

---

*Last updated by People Ops, February 2026. Questions? Drop them in #people-ops.*
