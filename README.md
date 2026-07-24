# NYC Event Organizers Site

A simple static website for the ongoing NYC Event Organizers community.

## How to View Locally

Open `index.html` in a browser, or run a small local server:

```sh
python3 -m http.server 8000
```

Then visit:

```text
http://localhost:8000/
```

The RSVP and ticket buttons point to:

```text
https://pools.events/event/7WG2AdGP/august-2026-event-organizer-meetup/
```

Durable Pools pages:

```text
Upcoming events profile: https://pools.events/o/nyc-event-organizers/
Splash / all-links page: https://pools.events/os/nyc-event-organizers/
Old Notion community page: https://organizers.notion.site/?source=copy_link
```

Current event details:

- August 2026 Event Organizer Meetup
- Tuesday, August 18 at 7:00pm
- Prime Produce, 424 W 54th St, New York, NY
- Free–$5 tickets

## Main Files

- `index.html` is the page content.
- `styles.css` controls the visual design and mobile layout.
- `nyc_event_organizers_*.png` are the image assets used by the site.
- `make_event_organizer_print_sheet.py` is the script that generated the flyer/QR print assets.
- `docs/notion-cms.md` explains how the Notion page could become a lightweight CMS later.
- `docs/pools-activity-webhook.md` explains how to safely use the Pools activity webhook without exposing private data.
- `.env.example` shows the private webhook setting name without committing the real URL.
