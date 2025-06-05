import random
import re

def load_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

common_prefixes = load_list('./data/common-prefixes.txt')
common_suffixes = load_list('./data/common-suffixes.txt')
common_word_starts = load_list('./data/common_word_starts.txt')
prefixes = load_list('./data/prefixes.txt')
word_starts = load_list('./data/word_starts.txt')
word_ends = load_list('./data/word_ends.txt')
word_connectors = load_list('./data/word_connectors.txt')

def generate_placename():
    # Choose prefix
    use_common_prefix = random.random() < 0.2
    use_prefix = random.random() < 0.4
    use_connector = random.random() < 0.1

    if use_common_prefix and common_prefixes:
        prefix = random.choice(common_prefixes)
    elif use_prefix and prefixes:
        prefix = random.choice(prefixes)
    else:
        prefix = ""

    # Compose root from granular parts
    root_start = random.choice(word_starts) if word_starts else ""
    root_end = random.choice(word_ends) if word_ends else ""
    if root_end[0].isupper(): root_end = " "+root_end
    root = root_start + root_end

    if use_connector and word_connectors:
        connector = random.choice(word_connectors)
        # Randomly insert connector between start and end
        end_start = random.choice(word_starts) if word_starts else ""
        end_end = random.choice(word_ends).lower() if word_ends else ""
        end = end_start + end_end
        root = f"{root} {connector} {end}"

    # Optionally add a space if prefix is present and root doesn't start with a space
    name = f"{prefix} {root}".strip()
    # Clean up double spaces
    name = re.sub(r'\s+', ' ', name)
    return name

def generate_common_placenames():
    # Only use common prefixes, common word starts, and common suffixes
    use_common_prefix = random.random() < 0.4
    use_connector = random.random() < 0.1
    prefix = random.choice(common_prefixes) if use_common_prefix and common_prefixes else ""

    # Use starts and ends that are common (from your extracted files)
    root_start = random.choice(common_word_starts) if common_word_starts else ""
    root_end = random.choice(common_suffixes) if common_suffixes else ""
    root = root_start + root_end

    if use_connector and word_connectors:
        connector = random.choice(word_connectors)
        # Randomly insert connector between start and end
        end_start = random.choice(common_word_starts) if common_word_starts else ""
        end_end = random.choice(common_suffixes).lower() if common_suffixes else ""
        end = end_start + end_end
        root = f"{root} {connector} {end}"

    name = f"{prefix} {root}".strip()
    name = re.sub(r'\s+', ' ', name)
    return name

def generate_rude_placename():
    # Load rude words from file
    rude_words = load_list('./data/rude_words.txt')

    use_common_prefix = random.random() < 0.3
    use_rude_start = random.random() < 0.2  # 20% chance to use rude as start or end

    prefix = random.choice(common_prefixes) if use_common_prefix and common_prefixes else ""

    if use_rude_start and rude_words:
        root_start = random.choice(rude_words)
        root_end = random.choice(common_suffixes) if common_suffixes else ""
    else:
        root_start = random.choice(common_word_starts) if common_word_starts else ""
        root_end = random.choice(rude_words) if rude_words else ""

    if root_end[0].isupper():
        suffix = " "+root_end
        root_end = random.choice(common_suffixes) if common_suffixes else ""
        root_end = root_end+suffix
    root = root_start + root_end

    name = f"{prefix} {root}".strip()
    name = re.sub(r'\s+', ' ', name)
    return name

# Example usage:
# for _ in range(15):
#     print(generate_placename())
for _ in range(15):
    print(generate_common_placenames())
# for _ in range(15):
#     print(generate_rude_placename())

