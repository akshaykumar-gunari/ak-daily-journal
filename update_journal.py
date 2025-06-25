import json
import sys

def parse_entries_from_txt(txt_file):
    with open(txt_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    entries = []
    current_entry = {"date": "", "day": "", "learnings": []}

    for line in lines:
        if line.startswith("Date:"):
            if current_entry["date"]:  # Save previous entry before starting a new one
                validate_entry(current_entry)
                entries.append(current_entry)
                current_entry = {"date": "", "day": "", "learnings": []}
            current_entry["date"] = line.replace("Date:", "").strip()
        elif line.startswith("Day:"):
            current_entry["day"] = line.replace("Day:", "").strip()
        elif line.startswith("Learnings:"):
            continue
        else:
            current_entry["learnings"].append(line)

    # Append the last entry
    if current_entry["date"]:
        validate_entry(current_entry)
        entries.append(current_entry)

    return entries

def validate_entry(entry):
    if not entry["date"]:
        raise ValueError("Missing Date in one of the entries.")
    if not entry["day"]:
        raise ValueError(f"Missing Day for date {entry['date']}")
    if not entry["learnings"]:
        raise ValueError(f"Missing Learnings for date {entry['date']}")

def load_json_safe(json_file):
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {json_file} not found. Creating a new one.")
        return {"entries": []}
    except json.JSONDecodeError:
        print(f"File {json_file} is empty or invalid. Initializing as empty.")
        return {"entries": []}

def find_entry_by_date(data, date):
    for i, entry in enumerate(data.get("entries", [])):
        if entry.get("date") == date:
            return i, entry
    return None, None

def append_or_update_entries(json_file, new_entries):
    data = load_json_safe(json_file)
    updated = False

    for new_entry in new_entries:
        index, existing_entry = find_entry_by_date(data, new_entry["date"])
        if existing_entry:
            if existing_entry.get("learnings") != new_entry.get("learnings"):
                print(f"⚡ Updating learnings for {new_entry['date']}.")
                data["entries"][index]["learnings"] = new_entry["learnings"]
                updated = True
            else:
                print(f"✅ Entry for {new_entry['date']} already up-to-date.")
        else:
            print(f"✅ Adding new entry for {new_entry['date']}.")
            data["entries"].append(new_entry)
            updated = True

    if updated:
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=2)
        print(f"💾 Changes saved to {json_file}")
    else:
        print("🚫 No changes needed. All entries are already up-to-date.")

if __name__ == "__main__":
    json_file = 'journal-data.json'
    txt_file = 'data/new_entry.txt'

    try:
        entries = parse_entries_from_txt(txt_file)
        append_or_update_entries(json_file, entries)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

