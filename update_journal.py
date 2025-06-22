import json
import sys

def read_new_entry_txt(txt_file):
    with open(txt_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    
    entry = {"date": "", "day": "", "learnings": []}
    
    for line in lines:
        if line.startswith("Date:"):
            entry["date"] = line.replace("Date:", "").strip()
        elif line.startswith("Day:"):
            entry["day"] = line.replace("Day:", "").strip()
        elif line.startswith("Learnings:"):
            continue
        else:
            entry["learnings"].append(line)
    
    # Validate required fields
    if not entry["date"]:
        raise ValueError("Date is missing in the TXT file.")
    if not entry["day"]:
        raise ValueError("Day is missing in the TXT file.")
    if not entry["learnings"]:
        raise ValueError("Learnings are missing in the TXT file.")
    
    return entry

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

def append_or_update_entry(json_file, new_entry):
    data = load_json_safe(json_file)
    
    index, existing_entry = find_entry_by_date(data, new_entry["date"])
    
    if existing_entry:
        if existing_entry.get("learnings") != new_entry.get("learnings"):
            print(f"⚡ Updating learnings for date {new_entry['date']}.")
            data["entries"][index]["learnings"] = new_entry["learnings"]
        else:
            print(f"✅ Entry for {new_entry['date']} already up-to-date. No changes made.")
            return
    else:
        print(f"✅ Adding new entry for {new_entry['date']}.")
        data.setdefault("entries", []).append(new_entry)

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=2)
    
    print(f"💾 Changes saved to {json_file}")

if __name__ == "__main__":
    json_file = 'journal-data.json'
    txt_file = 'data/new_entry.txt'
    
    try:
        new_entry = read_new_entry_txt(txt_file)
        append_or_update_entry(json_file, new_entry)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)