import re

def load_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

with open('./data/placenames.txt', 'r', encoding='utf-8') as f:
    placenames = [line.strip() for line in f if line.strip()]

common_prefixes = load_list('./data/common-prefixes.txt')
common_suffixes = load_list('./data/common-suffixes.txt')

prefixes = set()
word_starts = set()
word_ends = set()
word_connectors = set()
common_word_starts = set()

for name in placenames:
    # Find sequences of words starting with lowercase letters
    lc = re.findall(r'\b(-?[a-z][a-z\'-]+)+\s?[A-Z]', name)
    if lc:
        lc = lc[0].strip()
        if lc not in word_connectors:
            word_connectors.add(lc)
    # Find sequences of lower case words ending placenames    
    ec = re.findall(r'\b(-?[a-z][a-z\'-]+)+$', name)
    if ec:
        ec = ec[0].strip()
        if ec not in word_ends:
            word_ends.add(ec)
    words = name.split()
    # Prefix: first word if in common_prefixes or is capitalized and not a known ending
    prefix = ""
    rest_words = words
    if words and (words[0] in common_prefixes or (words[0][0].isupper() and words[0].lower() not in [s.lower() for s in common_suffixes])):
        prefix = words[0]
        prefixes.add(prefix)
        rest_words = words[1:]
    # For each word (except prefix), extract start and end
    for word in rest_words:
        # Word start: up to first vowel group or 4 letters
        m = re.match(r"([A-Z][bcdfghjklmnpqrstvwxyz]*[aeiouy]+[a-z]{0,2})", word)
        if m:
            start = m.group(1)
            if len(start) > 1 and start not in word_starts:
                word_starts.add(start)
        # Word end: match known suffix or last 3-5 letters
        matched_suffix = None
        for suf in sorted(common_suffixes, key=len, reverse=True):
            if word.lower().endswith(suf.lower()):
                word_ends.add(suf)
                matched_suffix = suf
                # Extract the word start by removing the suffix
                start_candidate = word[:-len(suf)]
                if len(start_candidate) > 1:
                    common_word_starts.add(start_candidate)
                break
        if not matched_suffix:
            # Take last 3-5 letters as fallback, but only if it contains at least one vowel
            if len(word) > 3:
                end5 = word[-5:]
                if re.search(r'[aeiouy]', end5, re.I):
                    word_ends.add(end5)
            if len(word) > 2:
                end3 = word[-3:]
                if re.search(r'[aeiouy]', end3, re.I):
                    word_ends.add(end3)

# Save to text files
with open('./data/prefixes.txt', 'w', encoding='utf-8') as f:
    for p in sorted(prefixes):
        f.write(p + '\n')

with open('./data/word_starts.txt', 'w', encoding='utf-8') as f:
    for s in sorted(word_starts):
        f.write(s + '\n')

with open('./data/word_ends.txt', 'w', encoding='utf-8') as f:
    for e in sorted(word_ends):
        f.write(e + '\n')

with open('./data/word_connectors.txt', 'w', encoding='utf-8') as f:
    for c in sorted(word_connectors):
        f.write(c + '\n')

with open('./data/common_word_starts.txt', 'w', encoding='utf-8') as f:
    for s in sorted(common_word_starts):
        f.write(s + '\n')

print("Granular parts extracted and saved to text files.")