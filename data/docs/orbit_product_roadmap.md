# Orbit — Product Roadmap
**H1 2026 (January – June)**  
**Version:** 1.3  
**Owner:** Product Management  
**Classification:** Confidential — Internal Only  
**Last Updated:** January 15, 2026

---

## About This Document

This document describes Orbit's planned product work for H1 2026. It is updated monthly. Features marked ✅ are shipped. Features marked 🔄 are in progress. Features marked 📋 are planned but not yet started. Features marked ❌ have been cut or deferred.

This roadmap is organized by theme, not by sprint. For sprint-level detail, see the Linear project boards.

---

## Company Context

Orbit is a B2B workforce management platform serving mid-market companies (200–5,000 employees) in the US and Canada. Our core product helps HR and operations teams manage employee scheduling, time tracking, absence management, and labor cost reporting.

As of Q4 2025, Orbit has 412 paying customers, $8.4M ARR, and is growing at 3.1% MoM. Our primary expansion motion is seat expansion within existing accounts. New logo acquisition is driven largely by outbound sales and G2 reviews.

Our top 3 priorities for H1 2026, as set by the executive team in January planning:
1. Reduce churn (current annual churn: 11.2%, target: <8%)
2. Increase expansion revenue (current NRR: 108%, target: 120%)
3. Ship AI-assisted scheduling to unblock enterprise deals (3 enterprise pilots waiting on this feature)

---

## Theme 1: AI-Assisted Scheduling

**Why:** Our top-of-funnel win rate against Deputy and When I Work drops to 38% without AI scheduling. Both competitors shipped AI recommendations in 2025. Three enterprise deals (estimated combined ACV: $420K) are explicitly blocked on this feature.

**What we're building:**
- Demand forecasting engine — predict staffing needs based on historical data, seasonality, and user-defined events
- Auto-schedule generator — produce a draft schedule that satisfies coverage requirements, labor laws, employee preferences, and cost targets
- Shift swap recommendations — when an employee requests a swap, suggest the best available replacement
- Manager override interface — allow managers to adjust AI suggestions with clear visibility into cost and compliance implications

### 1.1 Demand Forecasting MVP
**Status:** 🔄 In Progress  
**Target:** February 28, 2026  
**Owner:** ML Platform team + Product (Kenji Watanabe)  
**Description:** Ingest 12 months of historical shift data and user-defined "demand signals" (upcoming events, holidays, seasonal patterns). Produce a daily staffing headcount recommendation per role per location. Accuracy target: within 10% of actual required headcount 80% of the time.  
**Dependencies:** Data pipeline work from Platform (ETA Feb 10). ML model training requires at least 6 months of historical data per location — customers with less history will see reduced accuracy.

### 1.2 Auto-Schedule Generator
**Status:** 📋 Planned  
**Target:** April 15, 2026  
**Owner:** Scheduling team + ML Platform  
**Description:** Given demand forecast + employee roster + constraints (availability, certifications, max hours, labor law rules by state), generate a draft schedule for a given week. The generated schedule should require fewer than 30 minutes of manager editing on average (measured via time-in-editor telemetry).  
**Risk:** Labor law rules vary significantly by state and province. We will launch with US-only support. Canadian labor law support is deferred to H2.

### 1.3 Shift Swap Recommendations
**Status:** 📋 Planned  
**Target:** May 30, 2026  
**Owner:** Scheduling team  
**Description:** When a swap request is submitted, surface the top 3 recommended replacements ranked by: availability, role match, hours remaining in week, and travel distance to shift location.

### 1.4 Enterprise Pilot Onboarding
**Status:** 🔄 In Progress  
**Target:** March 31, 2026 (pilot start)  
**Owner:** Customer Success + Product  
**Description:** Onboard the 3 enterprise pipeline deals into a closed AI scheduling beta. Gather structured feedback via bi-weekly calls and in-app surveys.

---

## Theme 2: Churn Reduction

**Why:** At 11.2% annual churn, we are losing approximately 46 customers per year. Exit interview data shows top reasons: "product too complex for our admin team" (38%), "missing integrations with our HRIS" (31%), "reporting doesn't show what I need" (21%).

**What we're building:**
- Simplified admin experience for SMB customers
- Native integrations with Workday, BambooHR, and Rippling
- Revamped labor cost reporting

### 2.1 Simplified Scheduling View (SMB Mode)
**Status:** 🔄 In Progress  
**Target:** February 14, 2026  
**Owner:** Core Product (Priya Sharma)  
**Description:** A simplified scheduling interface for customers with <100 employees that hides advanced features (multi-location management, certification tracking, union rules). Toggled per account by customer success during onboarding. Reduces initial time-to-value for SMB customers.

### 2.2 Workday Integration
**Status:** 🔄 In Progress  
**Target:** March 15, 2026  
**Owner:** Integrations team  
**Description:** Bi-directional sync of employee records between Workday and Orbit. Employee adds, terminations, and role changes in Workday reflect in Orbit within 15 minutes. Time and attendance data from Orbit exports to Workday Payroll.  
**Note:** Workday's integration API requires a paid partnership agreement. Legal is finalizing this — not a technical blocker.

### 2.3 BambooHR Integration
**Status:** 📋 Planned  
**Target:** April 30, 2026  
**Owner:** Integrations team  
**Description:** One-way employee sync from BambooHR to Orbit. BambooHR is used by 23% of our current customer base (per CRM data). This is the most-requested integration by ARR impact.

### 2.4 Rippling Integration
**Status:** ❌ Deferred to H2  
**Reason:** Rippling's API has significant rate limiting that makes real-time sync impractical. We are in discussions with their partnerships team about a higher-tier API agreement. Deferring until resolved.

### 2.5 Labor Cost Reporting Overhaul
**Status:** 📋 Planned  
**Target:** May 15, 2026  
**Owner:** Data & Reporting team (Fatima Al-Rashid)  
**Description:** Rebuild the labor cost report from scratch. Current report is widely cited in churn interviews as inadequate. New report will include: cost by department, role, and location; overtime cost breakdown; budget vs. actual comparison; and 4-week trend lines. Export to CSV and PDF.

---

## Theme 3: Platform & Reliability

**Why:** Tech debt and reliability issues are costing us engineering velocity and creating occasional customer-facing incidents. Three specific areas need investment before we can safely scale to enterprise.

### 3.1 Audit Log Overhaul
**Status:** 🔄 In Progress  
**Target:** February 28, 2026  
**Owner:** Platform team  
**Description:** Rebuild audit logging to be tamper-evident (hash-chained entries) and queryable via the admin UI. Current logs are append-only flat files — not sufficient for enterprise compliance requirements. New system will log: who took what action, on what object, at what time, from what IP address.

### 3.2 SSO / SAML 2.0 Support
**Status:** ✅ Shipped  
**Shipped:** January 8, 2026  
**Description:** Enterprise customers can now configure SSO via SAML 2.0 or OIDC. Tested with Okta, Azure AD, and Google Workspace. Required by 7 enterprise pipeline deals. Shipped 2 weeks ahead of schedule.

### 3.3 API Rate Limiting
**Status:** ✅ Shipped  
**Shipped:** January 22, 2026  
**Description:** Per-customer API rate limits (default: 1,000 requests/minute) to prevent one customer's API usage from impacting platform performance for others. Configurable per customer tier.

### 3.4 Mobile App Performance
**Status:** 📋 Planned  
**Target:** June 15, 2026  
**Owner:** Mobile team (Carlos Mendez)  
**Description:** Address reported performance issues in the mobile app on Android (Pixel 6, Samsung Galaxy S22) — specifically slow schedule load time (p99: 8.2 seconds, target: <2 seconds). Root cause identified as over-fetching on the schedule endpoint. Requires API changes + mobile cache layer.

---

## Deferred / Cut Features

The following features were in consideration for H1 but have been explicitly deferred to H2 or beyond:

| Feature | Reason for Deferral |
|---|---|
| Rippling integration | API rate limit issue, pending partnership negotiation |
| Canadian labor law support for AI scheduling | Complexity and legal review time; H2 priority |
| Shift marketplace (employee-initiated open shift pickup) | Deprioritized vs. churn reduction work; revisit in Q3 |
| Payroll module | Out of scope for H1; major initiative requiring dedicated team |
| White-label / reseller support | Small TAM, high complexity; revisit if channel partnership materializes |

---

## Success Metrics for H1 2026

| Metric | Current | H1 Target |
|---|---|---|
| Annual churn rate | 11.2% | <9% (improvement visible in cohort data) |
| Net Revenue Retention | 108% | >112% |
| AI scheduling feature adoption | N/A (not shipped) | >35% of eligible customers using within 60 days of launch |
| Enterprise deals closed (AI scheduling unblock) | 0 | 2 of 3 pipeline deals closed |
| CSAT score | 7.1/10 | >7.8/10 |
| P1 incidents | 3 in H2 2025 | 0 in H1 2026 |

---

*Orbit Product Roadmap H1 2026 — Confidential — Internal Use Only*  
*Questions: product@orbit.com or #product-roadmap in Slack*
