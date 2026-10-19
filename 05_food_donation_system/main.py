import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
USERS_FILE = DATA / "users.json"
DONATIONS_FILE = DATA / "donations.json"
VALID_ROLES = {"donor", "volunteer", "requester"}
VALID_STATUSES = {"Available", "Claimed", "Picked Up", "Delivered"}


def load_records(path):
    DATA.mkdir(exist_ok=True)
    if not path.exists():
        save_records(path, [])
    try:
        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{path.name} contains invalid JSON; restore/fix it before continuing.") from exc
    if not isinstance(records, list):
        raise RuntimeError(f"{path.name} must contain a JSON list.")
    return records


def save_records(path, records):
    DATA.mkdir(exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, ensure_ascii=False)
    temp_path.replace(path)


def get_user(user_id):
    for user in load_records(USERS_FILE):
        if user.get("user_id") == user_id:
            return user
    raise LookupError(f"User '{user_id}' was not found.")


def register_user(name, role, contact):
    name, role, contact = name.strip(), role.strip().lower(), contact.strip()
    if not name or not contact:
        raise ValueError("Name and contact cannot be empty.")
    if role not in VALID_ROLES:
        raise ValueError("Role must be donor, volunteer, or requester.")
    users = load_records(USERS_FILE)
    prefix = {"donor": "DONOR", "volunteer": "VOL", "requester": "REQ"}[role]
    used = {u.get("user_id") for u in users}
    n = 101
    while f"{prefix}{n}" in used:
        n += 1
    user = {"user_id": f"{prefix}{n}", "name": name, "role": role, "contact": contact}
    users.append(user)
    save_records(USERS_FILE, users)
    return user


def create_donation(donor_id, food_name, quantity, unit, location, available_until, contact):
    donor = get_user(donor_id)
    if donor["role"] != "donor":
        raise PermissionError("Only a registered donor can create a donation.")
    food_name, unit, location, contact = food_name.strip(), unit.strip(), location.strip(), contact.strip()
    if not all([food_name, unit, location, contact]):
        raise ValueError("Food, unit, location, and contact cannot be empty.")
    if isinstance(quantity, bool) or quantity <= 0:
        raise ValueError("Quantity must be a positive whole number.")
    try:
        deadline = datetime.fromisoformat(available_until)
    except ValueError as exc:
        raise ValueError("Invalid date/time. Use YYYY-MM-DD HH:MM.") from exc
    if deadline <= datetime.now():
        raise ValueError("Availability deadline must be in the future.")

    donations = load_records(DONATIONS_FILE)
    used = {d.get("donation_id") for d in donations}
    n = 1
    while f"DON{n:03d}" in used:
        n += 1
    donation = {
        "donation_id": f"DON{n:03d}", "donor_id": donor_id,
        "food_name": food_name, "quantity": quantity, "quantity_unit": unit,
        "location": location, "available_until": deadline.isoformat(timespec="minutes"),
        "contact": contact, "status": "Available", "volunteer_id": None
    }
    donations.append(donation)
    save_records(DONATIONS_FILE, donations)
    return donation


def get_donation(donation_id):
    for donation in load_records(DONATIONS_FILE):
        if donation.get("donation_id") == donation_id:
            return donation
    raise LookupError(f"Donation '{donation_id}' was not found.")


def get_available_donations():
    now = datetime.now()
    return [d for d in load_records(DONATIONS_FILE)
            if d.get("status") == "Available"
            and datetime.fromisoformat(d["available_until"]) > now]


def claim_donation(donation_id, volunteer_id):
    volunteer = get_user(volunteer_id)
    if volunteer["role"] != "volunteer":
        raise PermissionError("Only a volunteer can claim a donation.")
    donations = load_records(DONATIONS_FILE)
    donation = next((d for d in donations if d.get("donation_id") == donation_id), None)
    if donation is None:
        raise LookupError(f"Donation '{donation_id}' was not found.")
    if donation["status"] != "Available":
        raise RuntimeError("This donation is no longer available.")
    if datetime.fromisoformat(donation["available_until"]) <= datetime.now():
        raise RuntimeError("This donation has expired.")
    donation["status"] = "Claimed"
    donation["volunteer_id"] = volunteer_id
    save_records(DONATIONS_FILE, donations)
    return donation


def update_status(donation_id, new_status, volunteer_id):
    allowed_next = {"Claimed": "Picked Up", "Picked Up": "Delivered"}
    donations = load_records(DONATIONS_FILE)
    donation = next((d for d in donations if d.get("donation_id") == donation_id), None)
    if donation is None:
        raise LookupError(f"Donation '{donation_id}' was not found.")
    volunteer = get_user(volunteer_id)
    if volunteer["role"] != "volunteer":
        raise PermissionError("Only a volunteer can update status.")
    if donation.get("volunteer_id") != volunteer_id:
        raise PermissionError("Only the assigned volunteer can update this donation.")
    if allowed_next.get(donation["status"]) != new_status:
        raise RuntimeError(f"Invalid status transition: {donation['status']} -> {new_status}.")
    donation["status"] = new_status
    save_records(DONATIONS_FILE, donations)
    return donation


def print_donation(d):
    print("-" * 42)
    for label, key in [("Donation ID", "donation_id"), ("Food", "food_name"),
                       ("Quantity", "quantity"), ("Unit", "quantity_unit"),
                       ("Location", "location"), ("Available until", "available_until"),
                       ("Status", "status"), ("Donor ID", "donor_id"),
                       ("Volunteer ID", "volunteer_id")]:
        print(f"{label:16}: {d.get(key) or 'Not assigned'}")
    print("-" * 42)


def ask(label):
    value = input(label).strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    return value


def main():
    print("=== Food Donation Management System ===")
    while True:
        print("\n1 Register user  2 Create donation  3 Available donations")
        print("4 View donation  5 Claim donation  6 Mark picked up")
        print("7 Mark delivered  8 View users  9 Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                user = register_user(ask("Name: "), ask("Role (donor/volunteer/requester): "), ask("Contact: "))
                print(f"Registered successfully. User ID: {user['user_id']}")
            elif choice == "2":
                donor_id = ask("Donor ID: ").upper()
                food = ask("Food name: ")
                quantity = int(ask("Quantity (whole number): "))
                unit = ask("Quantity unit (e.g. meals): ")
                location = ask("Location: ")
                deadline_text = ask("Available until (YYYY-MM-DD HH:MM): ")
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d %H:%M").isoformat(timespec="minutes")
                contact = ask("Contact: ")
                donation = create_donation(donor_id, food, quantity, unit, location, deadline, contact)
                print(f"Donation created. ID: {donation['donation_id']} | Status: {donation['status']}")
            elif choice == "3":
                donations = get_available_donations()
                if not donations:
                    print("No available donations.")
                for donation in donations:
                    print_donation(donation)
            elif choice == "4":
                print_donation(get_donation(ask("Donation ID: ").upper()))
            elif choice == "5":
                donation = claim_donation(ask("Donation ID: ").upper(), ask("Volunteer ID: ").upper())
                print(f"Donation {donation['donation_id']} claimed by {donation['volunteer_id']}.")
            elif choice in {"6", "7"}:
                donation_id = ask("Donation ID: ").upper()
                volunteer_id = ask("Assigned volunteer ID: ").upper()
                status = "Picked Up" if choice == "6" else "Delivered"
                donation = update_status(donation_id, status, volunteer_id)
                print(f"Donation status updated to {donation['status']}.")
            elif choice == "8":
                users = load_records(USERS_FILE)
                if not users:
                    print("No users registered.")
                for user in users:
                    print(f"{user['user_id']} | {user['name']} | {user['role']} | {user['contact']}")
            elif choice == "9":
                print("Goodbye.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 9.")
        except (ValueError, LookupError, PermissionError, RuntimeError, OSError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
