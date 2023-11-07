import re

def parse_bib_entry(entry):
    """Parses a single BibTeX entry and returns a dictionary of fields."""
    # Split the entry into lines and remove ',' from the end
    lines = entry.strip().split(",\n")
    # The first line contains the entry type and citation key
    first_line = lines.pop(0)
    entry_type = first_line.split("{")[0].strip().replace('@', '')
    citation_key = re.findall(r'\{(.*?)\,', first_line)[0]
    fields = {'ENTRYTYPE': entry_type, 'CITATIONKEY': citation_key}
    # Process remaining lines
    for line in lines:
        # Match only lines with '=' and ignore lines with strings inside strings
        if "=" in line and not re.search(r'\".*\".*\"', line):
            # Extract field name and value
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('{}"')
            fields[key] = value
    return fields

def bib_to_markdown_table(bib_text):
    """Converts BibTeX entries to a Markdown table."""
    # Split the bib file into individual entries
    entries = re.split(r'\n@', bib_text)
    # Parse each entry
    parsed_entries = [parse_bib_entry(entry) if entry.strip() else None for entry in entries]
    parsed_entries = [entry for entry in parsed_entries if entry]  # Remove None entries
    
    # Define the header of the Markdown table
    headers = ["Author", "Title", "Journal", "Year"]
    md_table = "| " + " | ".join(headers) + " |\n"
    md_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    
    # Add each entry to the Markdown table
    for entry in parsed_entries:
        row = []
        for header in headers:
            key = header.upper()
            if key in entry:
                row.append(entry[key])
            else:
                row.append('')
        md_table += "| " + " | ".join(row) + " |\n"
    
    return md_table

# Sample .bib content
bib_content = """
@article{smith2019,
    author = {John Smith and Jane Doe},
    title = {Great findings},
    journal = {Journal of Important Studies},
    year = {2019},
}

@article{doe2020,
    author = {Jane Doe},
    title = {Follow-up study},
    journal = {Journal of Follow-up Studies},
    year = {2020},
}
"""

print(bib_to_markdown_table(bib_content))
