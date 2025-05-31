import random
import re

def load_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

common_prefixes = load_list('./data/common-prefixes.txt')
common_suffixes = load_list('./data/common-suffixes.txt')
prefixes = load_list('./data/prefixes.txt')
root_bases = load_list('./data/root_bases.txt')
roots = load_list('./data/roots.txt')
suffixes = load_list('./data/suffixes.txt')

def generate_placename():
    use_common_prefix = random.random() < 0.2
    use_prefix = random.random() < 0.4
    use_root_base = random.random() < 0.6
    use_suffix = random.random() < 0.2

    if use_common_prefix:
       prefix = random.choice(common_prefixes)
    elif use_prefix:
        prefix = random.choice(prefixes)
    else:
        prefix = ""

    if use_root_base:
        root_base = random.choice(root_bases)
        root_end = random.choice(common_suffixes)
        root = root_base + root_end
    else:
        root = random.choice(roots)
    
    if use_suffix:
        suffix = random.choice(suffixes)
    else:
        suffix = ""
    
    name = f"{prefix} {root} {suffix}".strip()
    return re.sub(r'\s+', ' ', name)

for _ in range(15):
    new_name = generate_placename()
    print(new_name)

