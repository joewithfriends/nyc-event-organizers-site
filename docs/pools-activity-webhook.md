# Pools Activity Webhook

The Pools activity webhook can help power future community-site features from activity like follows, checkout questions, RSVPs, and other organizer signals.

Plain-English version: a webhook is an automated notification pipe. When something happens in Pools, data can be sent to another tool. It is not a public page people visit; it is more like a private delivery address for event data.

## Secret Handling

Do not commit the live Zapier webhook URL to this public GitHub repo.

Store it as an environment variable instead:

```text
POOLS_ACTIVITY_WEBHOOK_URL
```

That keeps the URL out of the code while still letting a server, deployment tool, or automation use it.

## Recommended Data Flow

The current site is static HTML, so it cannot securely receive private webhook activity by itself.

Use this flow instead:

1. Pools sends activity to the Zapier webhook.
2. Zapier filters out private or sensitive fields.
3. Zapier writes safe, public-ready summaries into a source the site can read later.
4. The website displays only approved aggregate or editorial content.

Good destinations for step 3:

- Notion database for non-technical editing and approval.
- Airtable for structured records and filtering.
- A checked-in JSON file if updates are manual and infrequent.
- A small backend/database later if the site becomes more dynamic.

## What Could Appear on the Site

Safe public examples:

- Number of organizers who RSVP'd.
- Recent organizer puzzle themes.
- Common checkout question themes.
- Recent community milestones.
- Venue or organizer needs, after moderation.

Avoid publishing:

- Emails, phone numbers, Instagram handles, names, or payment details without explicit consent.
- Raw checkout answers.
- Anything from a private group chat.
- Exact individual follow or RSVP activity unless the person opted in.

## Suggested Notion CMS Shape

If Notion becomes the moderation layer, create a database called `Community Activity` with:

- `Title`
- `Type`: RSVP, Follow, Checkout Question, Puzzle, Venue Lead, Resource
- `Source`
- `Summary`
- `Public?`
- `Date`
- `Related Event`

Zapier can create draft rows. A human can mark `Public?` when something is ready for the website.

## Future Implementation

When the site moves beyond static HTML, add a build step or small server route that reads only approved records from Notion/Airtable and renders them into the site.

Do not call the Zapier webhook directly from browser JavaScript. That would expose the webhook URL to every site visitor.
