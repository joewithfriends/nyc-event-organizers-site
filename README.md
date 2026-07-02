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

Current event details:

- August 2026 Event Organizer Meetup
- Tuesday, August 25 at 7:00pm
- New York, NY
- Free tickets

## Main Files

- `index.html` is the page content.
- `styles.css` controls the visual design and mobile layout.
- `nyc_event_organizers_*.png` are the image assets used by the site.
- `make_event_organizer_print_sheet.py` is the script that generated the flyer/QR print assets.
