# Food Donation Management System

A console-based Python backend prototype demonstrating OOP, JSON persistence, validation, exception handling, user roles, and donation status progression.

## Run

Requires Python 3.10+ and no third-party packages.

```bash
python main.py
```

## Demo workflow

1. Register a donor and note the generated ID (for example `DONOR101`).
2. Register a volunteer and note the generated ID (for example `VOL101`).
3. Create a donation. Enter availability as `YYYY-MM-DD HH:MM` and choose a future date/time.
4. View available donations and note the donation ID (for example `DON001`).
5. Claim it using the volunteer ID.
6. Mark it picked up, then delivered, using the same volunteer ID.
7. Exit and restart to verify data persistence.

## Data

User and donation records are saved in `data/users.json` and `data/donations.json`. These are local prototype files, not a production database.

## Limitations

This is a local console prototype, not a deployed HTTP API. It does not implement password authentication, multi-user concurrency, notifications, or production security. User IDs are identifiers, not proof of identity.
