import random
import re

with open('./data/placenames.txt', 'r', encoding='utf-8') as f:
    placenames = [line.strip() for line in f if line.strip()]

# Common prefixes and suffixes in UK placenames
COMMON_PREFIXES = [
    "Upper", "Lower", "East", "West", "North", "South", "Great", "Little",
    "Old", "New", "High", "Nether", "Over", "Under", "Middle"
]
COMMON_SUFFIXES = [
    "ton", "ham", "ford", "worth", "ley", "leigh", "field", "wood", "hill", "brook", "bridge",
    "well", "stone", "mouth", "wick", "wich", "by", "thorpe", "combe", "hurst", "stead", "gate",
    "burn", "dale", "end", "side", "green", "cross", "edge", "bank", "park", "pool", "court",
    "bay", "stow", "holme", "barrow", "dean", "fell", "holt", "manor", "heath", "grove", "mead"
]

# Extract prefixes, suffixes, and roots from the dataset
prefixes = set()
suffixes = set()
roots = set()
root_bases = set()

for name in placenames:
    words = name.split()
    # Check for prefix
    if words and words[0] in COMMON_PREFIXES:
        prefixes.add(words[0])
        root_part = ' '.join(words[1:])
    else:
        root_part = name

    # Check for suffix (match at end of word, ignore case)
    matched_suffix = None
    for suf in sorted(COMMON_SUFFIXES, key=len, reverse=True):
        if re.search(rf'{suf}$', root_part, re.I):
            suffixes.add(suf)
            matched_suffix = suf
            break

    # Extract root (remove prefix and suffix)
    if matched_suffix:
        root = re.sub(rf'{matched_suffix}$', '', root_part, flags=re.I).strip()
        if root and len(root) > 1:
            root_bases.add(root)
    else:
        root = root_part.strip()
        if root and len(root) > 1:
            roots.add(root)

# Add some rare/less common prefixes and suffixes found in the data
for name in placenames:
    words = name.replace('-', ' ').split()
    if words and len(words[0]) > 2 and words[0][0].isupper() and words[0] not in COMMON_PREFIXES:
        prefixes.add(words[0])
    for suf in re.findall(r'[A-Z][a-z]+$', name):
        if suf not in COMMON_SUFFIXES and len(suf) > 2:
            suffixes.add(suf)

prefixes = sorted(prefixes)
root_bases = sorted(root_bases)
roots = sorted(roots)
suffixes = sorted(suffixes)

def generate_placename():
    use_common_prefix = random.random() < 0.2
    use_prefix = random.random() < 0.4
    use_root_base = random.random() < 0.6
    use_suffix = random.random() < 0.2

    if use_common_prefix:
       prefix = random.choice(COMMON_PREFIXES)
    elif use_prefix:
        prefix = random.choice(prefixes)
    else:
        prefix = ""

    if use_root_base:
        root_base = random.choice(root_bases)
        root_end = random.choice(COMMON_SUFFIXES)
        root = root_base + root_end
    else:
        root = random.choice(roots)
    
    if use_suffix:
        suffix = random.choice(suffixes)
    else:
        suffix = ""
    
    name = f"{prefix} {root} {suffix}".strip()
    return re.sub(r'\s+', ' ', name)

print("Sample generated placenames:\n")
original_names_set = set(placenames)

for _ in range(15):
    new_name = generate_placename()
    if new_name in original_names_set:
        print(f"{new_name} (exists)")
    else:
        print(new_name)

