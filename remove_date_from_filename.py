# This script changes the filename from "YYYYMMDD - filename.md" to "filename.md"
# It also updates the links in all other files to point to the new filename


# Make a dictionary to map old filenames to new filenames
# Check for duplicates in the new filenames

import os
import re
import json


def get_tg_filename(tags_to_refs, matched_text):
    has_period = "." in matched_text
    # Remove [text in brackets] from the matched text
    matched_text = re.sub(r'\[.*?\]', '', matched_text)
    matched_text = matched_text.replace(".", "").strip()
    for tag in tags_to_refs.keys():
        if matched_text in tag:
            return f"[[{tag}]]" if not has_period else f"[[{tag}]]."
    
    # If no match found, return the original text in wiki link format
    input(f"matched_text: {matched_text} not found in tags_to_refs")
    return f"[[{matched_text}]]"

old_to_new = {}
volumes = ["Old Testament", "New Testament", "Book of Mormon", "Doctrine and Covenants", "Pearl of Great Price"]
all_files_sciptures = []

parent_directory = os.path.dirname(os.path.abspath(__file__))

for volume in volumes:
    all_files_sciptures += [f"{volume}\\{f}" for f in os.listdir(f"{parent_directory}\\{volume}")]


# Open tags_to_refs.json and get the list of tags
with open("tags_to_refs.json", "r", encoding="utf-8") as f:
    tags_to_refs = json.load(f)



test_files = ["Old Testament\\Genesis 1.1.md", "Old Testament\\Genesis 1.3.md", "Book of Mormon\\1 Nephi 1.1.md",
"New Testament\\1 Timothy 2.2.md"]

done = 1
total = len(all_files_sciptures)
# Update the links in all other files to point to the new filename
for file in all_files_sciptures:
    print(f"{done}/{total} - {file}")

    with open(file, "r", encoding="utf-8") as f:
        file_contents = f.read()
    # Replace churchofjesuschrist.org links with wiki links
    file_contents = re.sub(
        r'\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(https://www\.churchofjesuschrist\.org/study/scriptures/tg/[^)]*?\)', 
        lambda match: get_tg_filename(tags_to_refs, match.group(1)), 
        file_contents
    )
    done += 1
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_contents)