# Notion CMS Notes

The old Notion page is useful as content guidance today and could become a simple backend CMS later.

Plain-English version: a CMS is the place where non-technical people edit website content. If Notion becomes the CMS, someone could update event resources, community links, venue notes, or organizer puzzles in Notion, and the website could pull those updates automatically.

## Source Page

```text
https://organizers.notion.site/?source=copy_link
```

## Content Worth Using

- Community chat links: WhatsApp and Instagram.
- Mailing list / organizer index framing.
- RSVP and past meetup archive structure.
- Media, venue list, transcripts, and notes.
- Organizer puzzle themes: event formats, managing a team, building community, and policy / space.

## Recommended CMS Path

Keep the current website static for now. It is simple, fast, and easy for a collaborator to edit.

If the Notion page becomes the source of truth, the next clean step is to move repeated content into structured Notion databases:

- `Events`: title, date, time, location, ticket URL, poster image, status.
- `Community Links`: label, URL, short description, priority.
- `Resources`: title, category, URL, summary.
- `Organizer Puzzles`: theme, description, related notes.

Then the site can be upgraded to a small build step that reads Notion and generates static HTML from those databases.

## Why Not Wire Live Notion Immediately

Live Notion fetching would add API credentials, deployment environment variables, caching, error handling, and a build/deploy step. That is worth doing once the Notion structure is stable, but it is heavier than this first static site needs.
