import re

with open('./data/placenames.txt', 'r', encoding='utf-8') as f:
    placenames = [line.strip() for line in f if line.strip()]

# Load common prefixes and suffixes from text files
def load_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
    
common_prefixes = load_list('./data/common-prefixes.txt')
common_suffixes = load_list('./data/common-suffixes.txt')

prefixes = set()
suffixes = set()
roots = set()
root_bases = set()

for name in placenames:
    words = name.split()
    if words and words[0] in common_prefixes:
        prefixes.add(words[0])
        root_part = ' '.join(words[1:])
    else:
        root_part = name

    matched_suffix = None
    for suf in sorted(common_suffixes, key=len, reverse=True):
        if re.search(rf'{suf}$', root_part, re.I):
            suffixes.add(suf)
            matched_suffix = suf
            break

    if matched_suffix:
        root = re.sub(rf'{matched_suffix}$', '', root_part, flags=re.I).strip()
        if root and len(root) > 1:
            root_bases.add(root)
    else:
        root = root_part.strip()
        if root and len(root) > 1:
            roots.add(root)

# Add rare/less common prefixes and suffixes
for name in placenames:
    words = name.replace('-', ' ').split()
    if words and len(words[0]) > 2 and words[0][0].isupper() and words[0] not in common_prefixes:
        prefixes.add(words[0])
    for suf in re.findall(r'[A-Z][a-z]+$', name):
        if suf not in common_suffixes and len(suf) > 2:
            suffixes.add(suf)

# Save to text files
with open('./data/prefixes.txt', 'w', encoding='utf-8') as f:
    for p in sorted(prefixes):
        f.write(p + '\n')

with open('./data/root_bases.txt', 'w', encoding='utf-8') as f:
    for r in sorted(root_bases):
        f.write(r + '\n')

with open('./data/roots.txt', 'w', encoding='utf-8') as f:
    for r in sorted(roots):
        f.write(r + '\n')

with open('./data/suffixes.txt', 'w', encoding='utf-8') as f:
    for s in sorted(suffixes):
        f.write(s + '\n')

print("Parts extracted and saved to text files.")