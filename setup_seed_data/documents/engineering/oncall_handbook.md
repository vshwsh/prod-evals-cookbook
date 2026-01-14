# On-Call Handbook

**Effective Date:** January 1, 2024  
**Last Updated:** November 1, 2024  
**Owner:** Platform Engineering

## Overview

On-call rotation ensures 24/7 coverage for production issues. This handbook covers expectations, schedules, and how to handle your on-call shift.

## On-Call Expectations

When you're on-call, you are the **first responder** for production issues. This means:

- **Response time:** Acknowledge alerts within 15 minutes
- **Availability:** Be reachable and able to work within 30 minutes
- **Sobriety:** No alcohol or substances that impair judgment
- **Connectivity:** Have reliable internet and phone access
- **Laptop ready:** Keep your work laptop charged and accessible

## Rotation Schedule

| Team | Rotation Length | Primary Coverage |
|------|----------------|------------------|
| Platform | 1 week | 24/7 |
| Backend | 1 week | 24/7 |
| Mobile | 1 week | 8am-10pm PT (pager to platform overnight) |
| Data | 1 week | 6am-10pm PT |

Rotations start on **Monday at 10:00 AM Pacific** and end the following Monday.

## Compensation

- **On-call stipend:** $500/week for 24/7 rotations, $300/week for limited hours
- **Incident pay:** Additional $100 per SEV1/SEV2 incident responded to
- **Comp time:** Take a day off after particularly intense on-call weeks (manager discretion)

## Handoff Process

### Outgoing On-Call (Monday morning)
1. Post a summary in #oncall-handoff:
   - Active incidents or ongoing issues
   - Known upcoming risks (deploys, maintenance windows)
   - Anything weird you noticed during the week
2. Update the on-call doc with any new runbooks or learnings

### Incoming On-Call
1. Review the handoff summary
2. Check PagerDuty for any open or recent incidents
3. Review the on-call calendar for scheduled maintenance
4. Confirm your PagerDuty contact info is current

## What To Do When Paged

### Step 1: Acknowledge
- Acknowledge the alert in PagerDuty within 15 minutes
- This stops escalation and shows you're responding

### Step 2: Assess
- Is this a real issue or a false alarm?
- What's the severity? (See incident runbook for definitions)
- Who else needs to be involved?

### Step 3: Respond
- For SEV1/SEV2: Post in #incidents and follow the incident runbook
- For SEV3/SEV4: Investigate and resolve, or create a ticket for business hours
- For false alarms: Silence and create a ticket to fix the alert

### Step 4: Document
- Log what happened and what you did
- If it was a real incident, ensure follow-ups are created

## Common Scenarios

### "I'm getting too many alerts"
- If alerts are noisy, your job includes improving them
- Create tickets to fix flaky alerts
- Adjust thresholds if they're too sensitive
- Don't just silence without follow-up

### "I don't know how to fix this"
- **Escalate.** It's better to wake someone up than to let an issue persist
- Check the runbook library first
- Reach out to the relevant team's channel
- Use the escalation paths in the incident runbook

### "I have a conflict during my on-call week"
- Find a swap with another team member
- Post in #oncall-swaps at least 48 hours in advance
- Update PagerDuty with the new schedule
- Inform your manager

## Tools

- **PagerDuty:** Alerting and scheduling - pagerduty.com/acme
- **Datadog:** Metrics and dashboards - app.datadoghq.com
- **Slack:** #incidents for live response, #oncall for discussion
- **Runbooks:** notion.so/acme/runbooks

## Mental Health

On-call can be stressful. Please:
- Take breaks between shifts
- Talk to your manager if on-call is affecting your wellbeing
- Use comp time after hard weeks
- Remember: it's okay to escalate and ask for help

## Questions

Reach out in #oncall or to the Platform team lead.
