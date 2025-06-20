import subprocess
import sys
import re
import os

if len(sys.argv) < 2:
    print("Usage: python script.py input.csv")
    sys.exit(1)

input_file = sys.argv[1]
temp1 = "./data/temp1.csv"
temp2 = "./data/temp2.csv"
output_file = "./data/placenames.txt"

# Use csvsql to filter by descnm and ctry23nm
print("Filtering data for descnm = 'LOC' and ctry23nm = 'England'...")
query = 'select place23nm from IPN_GB_2024 where descnm = "LOC" and ctry23nm = "England"'
subprocess.run([
    "csvsql", "--query", query, "--encoding", "ISO-8859-1", input_file
], stdout=open(temp1, "w"))

# Find quoted strings and reformat them
print("Reformatting quoted strings...")
pattern = re.compile(r'^"([^,]+),\s?([^"]+)"$')
with open(temp1, "r", encoding="utf-8") as fin, open(temp2, "w", encoding="utf-8") as fout:
    next(fin)  # Skip the header line
    for line in fin:
        line = line.rstrip("\n")
        m = pattern.match(line)
        if m:
            fout.write(f"{m.group(2)} {m.group(1)}\n")
        else:
            fout.write(line + "\n")

# Remove any words in parentheses (and flipped parentheses)
print("Removing words in parentheses...")
pattern_parentheses = re.compile(r'^([^()]*)[()][^()]+[()]([^()]*)$')
with open(temp2, "r", encoding="utf-8") as fin, open(temp1, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.rstrip("\n")
        m = pattern_parentheses.match(line)
        if m:
            fout.write(m.group(1) + m.group(2) + "\n")
        else:
            fout.write(line + "\n")

# Remove any words after slashes
print("Removing words after slashes...")
pattern_slash = re.compile(r'^(.*?)(?:\s*\/.*)?$')
with open(temp1, "r", encoding="utf-8") as fin, open(temp2, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.rstrip("\n")
        m = pattern_slash.match(line)
        if m:
            fout.write(m.group(1) + "\n")
        else:
            fout.write(line + "\n")

# Strip whitespace and remove empty lines
print("Stripping whitespace and removing empty lines...")
with open(temp2, "r", encoding="utf-8") as fin, open(temp1, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.strip()
        line = re.sub(r'\s{2,}', ' ', line)  # Replace multiple spaces with a single space
        if line:
            fout.write(line + "\n")

# sort, remove duplicates (encoding IS-8859-1)
subprocess.run([
    "sort", temp1
], stdout=open(temp2, "w"))

subprocess.run([
    "uniq", temp2
], stdout=open(temp1, "w"))

with open(temp1, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
  for line in fin:
    fout.write(line)

# Clean up temp files
os.remove(temp1)
os.remove(temp2)

print(f"Done. Output saved to {output_file}")