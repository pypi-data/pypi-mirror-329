# autocorrect.py
import os
import re
import unicodedata
import regex
import jellyfish
import pkg_resources

# Words to exclude from correction and target words.
words_exclude = {"ផ្ទះ", "ផ្លូវ"}
targets = {"ផ្ទះ", "ផ្លូវ", "ភូមិ"}

def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text)

def load_resource_text(resource_path: str) -> str:
    """Load a text resource from the package."""
    # resource_path example: "data/district.txt" or "data/phum/example.txt"
    return pkg_resources.resource_string(__name__, resource_path).decode("utf-8")

def load_autocorrect_dict_from_resource(resource_path: str) -> set:
    """
    Load words from a single file resource.
    """
    text = load_resource_text(resource_path)
    return {normalize_text(line.strip()) for line in text.splitlines() if line.strip()}

def load_autocorrect_dicts_from_resource(folder_resource: str) -> set:
    """
    Load words from all .txt files in a folder inside the package.
    """
    words = set()
    # List all files in the given resource folder.
    # Note: resource_listdir works with pkg_resources if files are included.
    for filename in pkg_resources.resource_listdir(__name__, folder_resource):
        if filename.endswith(".txt"):
            resource_path = os.path.join(folder_resource, filename)
            text = load_resource_text(resource_path)
            words |= {normalize_text(line.strip()) for line in text.splitlines() if line.strip()}
    return words

# Automatically load dictionaries when the package is imported.
phum_dict = load_autocorrect_dicts_from_resource("data/phum")
khum_dict = load_autocorrect_dicts_from_resource("data/khum")
district_dict = load_autocorrect_dict_from_resource("data/district.txt")
province_dict = load_autocorrect_dict_from_resource("data/province.txt")

# print(f"Phum Dict Loaded ({len(phum_dict)} words)")
# print(f"Khum Dict Loaded ({len(khum_dict)} words)")
# print(f"District Dict Loaded ({len(district_dict)} words)")
# print(f"Province Dict Loaded ({len(province_dict)} words)")

def autocorrect_word(
    word: str, word_set: set, max_ratio: float = 0.4, max_typo_distance: int = None
) -> list:
    """
        Damerau-Levenshtein distance counts how many small changes
        (add, remove, change, or swap letters) are needed to fix a word.
    Example:
    -To change "cat" to "cart", you need 1 edit (insert "r").
    -To change "form" to "from", you need 1 edit (swap "o" and "r").
    -To change "hello" to "halo", you need 2 edits (remove "l" and change "e" to "a").
    """
    word = normalize_text(word)
    if word in word_set:
        return [word]
    max_typo_distance = (
        max(3, int(len(word) * 0.4)) if max_typo_distance is None else max_typo_distance
    )
    best_candidate, best_ratio = None, float("inf")
    for correct in word_set:
        d = jellyfish.damerau_levenshtein_distance(word, correct)
        ratio = d / max(len(word), len(correct))
        if d <= max_typo_distance or ratio <= max_ratio:
            if ratio < best_ratio:
                best_ratio, best_candidate = ratio, correct
    # If word contains numbers but candidate doesn't, skip correction.
    if any("០" <= ch <= "៩" for ch in word) and not (
        best_candidate and any("០" <= ch <= "៩" for ch in best_candidate)
    ):
        return [word]
    return [word] if best_candidate is None or best_ratio > 0.20 else [best_candidate]

def is_number(word: str) -> bool:
    return re.sub(r"[\u200B-\u200D\uFEFF]", "", word).strip().isdigit()

def merge_tokens(part: str) -> str:
    tokens, merged, i = part.split(), [], 0
    while i < len(tokens):
        if tokens[i] in targets and i + 1 < len(tokens) and re.search(r"[A-Za-z0-9]", tokens[i + 1]):
            merged.append(tokens[i] + tokens[i + 1])
            i += 2
        else:
            merged.append(tokens[i])
            i += 1
    return " ".join(merged)

def autocorrect_word_in_part(word, dictionary):
    word = normalize_text(word)
    if is_number(word) or word in words_exclude:
        return word

    # If the word already starts with a correct target, return it unchanged.
    # This prevents already correct tokens like "ផ្លូវក្រុម៨" from being modified.
    for t in {"ផ្ទះ", "ផ្លូវ", "ភូមិ"}:
        if word.startswith(t):
            return word

    # Correct known incorrect prefixes.
    if word.startswith("ផ្លុវ"):
        return "ផ្លូវ" + word[len("ផ្លុវ"):]
    if word.startswith("ផ្លុរ"):
        return "ផ្លូវ" + word[len("ផ្លុរ"):]
    if word.startswith("ផ្លូរ"):
        return "ផ្លូវ" + word[len("ផ្លូរ"):]
    if word.startswith("ផ្លូ"):
        return regex.sub(r"^ផ្លូ(?:\X*?)(?=[A-Za-z0-9\u17E0-\u17E9/])", "ផ្លូវ", word)
    if word.startswith("ផ្ល"):
        m = re.search(r"[0-9\u17E0-\u17E9/]", word)
        if m:
            return "ផ្លូវ" + word[m.start():]
        return "ផ្លូវ"

    # Fallback: if none of the above match, try to correct by matching target clusters.
    for t in {"ផ្ទះ", "ផ្លូវ", "ភូមិ"}:
        if word.startswith(t):
            rem = word[len(t):]
            return t if t == "ភូមិ" and not rem.strip() else t + (autocorrect_word(rem, dictionary)[0] if t == "ភូមិ" else rem)

    clusters = regex.findall(r"\X", word)
    best_target, best_n, best_distance = None, 0, float("inf")
    for t in {"ផ្ទះ", "ផ្លូវ", "ភូមិ"}:
        t_clusters = regex.findall(r"\X", t)
        if len(clusters) < len(t_clusters):
            continue
        d = jellyfish.damerau_levenshtein_distance("".join(clusters[:len(t_clusters)]), t)
        if d < best_distance:
            best_distance, best_target, best_n = d, t, len(t_clusters)
    if best_target and best_distance <= 2:
        rem = "".join(clusters[best_n:])
        if best_target == "ភូមិ":
            res = autocorrect_word(rem, dictionary)
            return best_target if not rem.strip() else best_target + (res[0] if res else rem)
        if best_target == "ផ្ទះ" and rem.startswith("ទ"):
            rem = rem[1:]
        return best_target + rem

    return word if word in dictionary else (autocorrect_word(word, dictionary)[0] or word)

def autocorrect_address_1(part, dictionary=phum_dict):
    # Merge tokens and autocorrect each word.
    return " ".join(
        autocorrect_word_in_part(w, dictionary) for w in merge_tokens(part).split()
    )

def autocorrect_address_2(address_2_text, khum_dictionary=khum_dict, district_dictionary=district_dict, province_dictionary=province_dict):
    parts = address_2_text.split()
    if len(parts) >= 2 and is_number(parts[1]):
        commune = parts[0] + parts[1]
        district = parts[2] if len(parts) > 2 else ""
        province = " ".join(parts[3:]) if len(parts) > 3 else ""
    else:
        if len(parts) >= 4:
            commune = parts[0]
            district = parts[1]
            province = " ".join(parts[2:])
        elif len(parts) == 3:
            commune, district, province = parts
        else:
            commune = parts[0] if parts else ""
            district = province = ""
    corrected_commune = autocorrect_word(commune, khum_dictionary, max_ratio=0.6)[0]
    corrected_district = autocorrect_word(district, district_dictionary, max_ratio=0.6)[0] if district else ""
    corrected_province = autocorrect_word(province, province_dictionary, max_ratio=0.6)[0] if province else ""
    return " ".join(filter(None, [corrected_commune, corrected_district, corrected_province]))


# ==========================Autocorrect Province, District, Khum, Phum separately==========================

def autocorrect_province(province_text: str) -> str:
    return autocorrect_word(province_text, province_dict, max_ratio=0.6)[0]

def autocorrect_district(district_text: str) -> str:
    return autocorrect_word(district_text, district_dict, max_ratio=0.6)[0]

def autocorrect_khum(khum_text: str) -> str:
    return autocorrect_word(khum_text, khum_dict, max_ratio=0.6)[0]

def autocorrect_phum(phum_text: str) -> str:
    phum_text = normalize_text(phum_text)  # Normalize Unicode characters
    
    # Case 1: If it already starts with "ភូមិ", autocorrect the remaining part
    if phum_text.startswith("ភូមិ"):
        rem = phum_text[len("ភូមិ"):]  # Get the part after "ភូមི"
        if not rem.strip():
            return "ភូមិ"  # Return just "ភូមិ" if nothing follows
        else:
            corrected_rem = autocorrect_word(rem, phum_dict, max_ratio=0.6)[0]
            return "ភូមិ" + corrected_rem
    
    # Case 2: Check if it starts with a variant of "ភូមិ" (e.g., "ភុមិ")
    clusters = regex.findall(r"\X", phum_text)  # Split into Unicode grapheme clusters
    t_clusters = regex.findall(r"\X", "ភូមិ")  # Clusters for "ភូមិ"
    if len(clusters) >= len(t_clusters):
        prefix = "".join(clusters[:len(t_clusters)])  # Take the first part of the input
        d = jellyfish.damerau_levenshtein_distance(prefix, "ភូមិ")  # Compare with "ភូមិ"
        if d <= 2:  # Allow small typos (distance ≤ 2)
            rem = "".join(clusters[len(t_clusters):])  # Get the remaining part
            corrected_rem = autocorrect_word(rem, phum_dict, max_ratio=0.6)[0] if rem.strip() else ""
            return "ភូមិ" + corrected_rem
    
    # Case 3: Fallback to dictionary-based correction
    return autocorrect_word(phum_text, phum_dict, max_ratio=0.6)[0]
