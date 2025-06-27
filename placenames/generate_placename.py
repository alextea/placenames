import random
import re

def load_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

common_prefixes = load_list('./data/common_prefixes.txt')
common_suffixes = load_list('./data/common_suffixes.txt')
common_word_starts = load_list('./data/common_word_starts.txt')
prefixes = load_list('./data/prefixes.txt')
word_starts = load_list('./data/word_starts.txt')
word_ends = load_list('./data/word_ends.txt')
word_connectors = load_list('./data/word_connectors.txt')
rude_words = load_list('./data/rude_words.txt')

def generate_placenames(mode='normal', n=1):
    """
    mode: 'normal', 'common', or 'rude'
    n: number of placenames to return
    """
    results = []
    for _ in range(n):
        # Prefix selection
        use_common_prefix = random.random() < 0.4 if mode != 'normal' else random.random() < 0.2
        use_prefix = random.random() < 0.4
        use_connector = random.random() < 0.1
        if mode == 'common' or mode == 'rude':
            prefix = random.choice(common_prefixes) if use_common_prefix and common_prefixes else ""
        else:
            if use_common_prefix and common_prefixes:
                prefix = random.choice(common_prefixes)
            elif use_prefix and prefixes:
                prefix = random.choice(prefixes)
            else:
                prefix = ""

        # Root and ending selection
        if mode == 'common':
            root_start = random.choice(common_word_starts) if common_word_starts else ""
            root_end = random.choice(common_suffixes) if common_suffixes else ""
        elif mode == 'rude':
            root_start = random.choice(rude_words) if rude_words else ""
            root_end = random.choice(common_suffixes).lower() if common_suffixes else ""
        else:
            root_start = random.choice(word_starts) if word_starts else ""
            root_end = random.choice(word_ends) if word_ends else ""
            if root_end and root_end[0].isupper():
                root_end = " " + root_end
        root = root_start + root_end

        # Connector logic
        if use_connector and word_connectors:
            connector = random.choice(word_connectors)
            if mode == 'common':
                end_start = random.choice(common_word_starts) if common_word_starts else ""
                end_end = random.choice(common_suffixes).lower() if common_suffixes else ""
            elif mode == 'rude':
                end_start = random.choice(word_starts) if word_starts else ""
                end_end = random.choice(word_ends).lower() if word_ends else ""
            else:
                end_start = random.choice(word_starts) if word_starts else ""
                end_end = random.choice(word_ends).lower() if word_ends else ""
            end = end_start + end_end
            root = f"{root} {connector} {end}"
            if '-' in root:
                root = root.replace(' ', '')

        # Special handling for rude mode (suffix logic)
        if mode == 'rude' and root_end:
            if root_end and root_end[0].isupper():
                suffix = " " + root_end
                root_end = random.choice(common_suffixes) if common_suffixes else ""
                root_end = root_end + suffix
            root = root_start + root_end

        name = f"{prefix} {root}".strip()
        name = re.sub(r'\s+', ' ', name)
        results.append(name)
    return results if n > 1 else results[0]

if __name__ == "__main__":
    print("\nGenerating 15 random placenames:")
    for name in generate_placenames('normal', 15):
        print(name)
    print("\nGenerating 15 common placenames:")
    for name in generate_placenames('common', 15):
        print(name)
    print("\nGenerating 15 rude placenames:")
    for name in generate_placenames('rude', 15):
        print(name)