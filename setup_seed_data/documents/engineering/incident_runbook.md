# Incident Response Runbook

**Effective Date:** January 1, 2024  
**Last Updated:** December 1, 2024  
**Owner:** Platform Engineering

## Overview

This runbook outlines how to respond to production incidents at Acme Corp. Fast, coordinated response minimizes customer impact and helps us learn from failures.

## Severity Levels

| Severity | Description | Response Time | Examples |
|----------|-------------|---------------|----------|
| **SEV1** | Complete outage, all customers affected | 15 minutes | Site down, data loss, security breach |
| **SEV2** | Major feature broken, many customers affected | 30 minutes | Auth failing, payments broken, API errors >10% |
| **SEV3** | Minor feature broken, some customers affected | 2 hours | Single integration down, slow performance |
| **SEV4** | Cosmetic or low-impact issue | Next business day | UI glitch, minor bug |

## Incident Roles

### Incident Commander (IC)
- Coordinates the response
- Makes decisions on mitigation steps
- Communicates status to stakeholders
- Usually the on-call engineer, but can be handed off

### Communications Lead
- Posts updates to #incidents channel
- Updates status page
- Drafts customer communications if needed
- Usually an Engineering Manager or on-call secondary

### Technical Responders
- Investigate root cause
- Implement fixes
- Monitor recovery
- Engineers pulled in as needed based on affected systems

## Response Steps

### 1. Acknowledge (First 5 minutes)
- Acknowledge the alert in PagerDuty
- Join the #incidents Slack channel
- Post initial message: what's broken, who's responding

### 2. Assess (First 15 minutes)
- Determine severity level
- Identify affected systems and customers
- Check recent deployments (last 24 hours)
- Check infrastructure dashboards (Datadog)

### 3. Mitigate (Ongoing)
- **First priority: Stop the bleeding**
- Consider rollback if recent deployment is suspected
- Scale up resources if capacity-related
- Enable feature flags to disable broken functionality
- Communicate every 30 minutes (SEV1/2) or every hour (SEV3)

### 4. Resolve
- Confirm the issue is fully resolved
- Monitor for 30 minutes to ensure stability
- Post final update to #incidents
- Update status page to "Resolved"

### 5. Follow Up (Within 48 hours)
- Create a post-incident review document
- Schedule blameless retrospective
- File tickets for follow-up improvements
- Update runbooks if needed

## Communication Templates

### Initial Incident Post
```
🚨 *INCIDENT DECLARED - [SEV LEVEL]*

*What's happening:* [Brief description]
*Impact:* [Who/what is affected]
*Incident Commander:* @[name]
*Status:* Investigating

Updates every [30 min / 1 hour]
```

### Status Update
```
📍 *UPDATE - [TIME]*

*Status:* [Investigating / Identified / Mitigating / Resolved]
*Actions taken:* [What we've done]
*Next steps:* [What we're doing next]
*ETA:* [If known]
```

### Resolution Post
```
✅ *INCIDENT RESOLVED*

*Duration:* [X hours Y minutes]
*Root cause:* [Brief summary]
*Resolution:* [What fixed it]
*Follow-up:* [Ticket numbers for improvements]

Post-incident review scheduled for [date/time]
```

## Escalation Paths

| System | Primary | Secondary | Escalation |
|--------|---------|-----------|------------|
| API/Backend | On-call engineer | Backend lead | VP Engineering |
| Database | On-call engineer | DBA | VP Engineering |
| Auth/Security | Security on-call | Security lead | CISO |
| Payments | On-call engineer | Payments lead | CFO |
| Mobile | Mobile on-call | Mobile lead | VP Engineering |

## Tools & Links

- **PagerDuty:** pagerduty.com/acme
- **Status Page:** status.acme-corp.com (admin)
- **Datadog:** app.datadoghq.com
- **Runbook Library:** notion.so/acme/runbooks
- **Incident Slack:** #incidents

## Post-Incident Reviews

We conduct blameless post-incident reviews for all SEV1 and SEV2 incidents. Focus areas:
- What happened and timeline
- What went well
- What could be improved
- Action items with owners and due dates

Template: notion.so/acme/post-incident-template
