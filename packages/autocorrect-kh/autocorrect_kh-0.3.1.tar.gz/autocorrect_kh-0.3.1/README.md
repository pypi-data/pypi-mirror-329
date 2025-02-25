# Autocorrect for Khmer National ID Addresses (`autocorrect_kh`)

This Python script (`autocorrect.py`) provides an autocorrection tool for Khmer addresses on Cambodian National ID cards. It processes addresses in two parts—`address_1` (house, road, village) and `address_2` (commune, district, province)—using dictionary-based correction and custom rules tailored to Khmer script.

![Khmer Address Correction Example](sample.png)

## Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Key Functions](#key-functions)

## Features
- Khmer Address Correction: Fixes typos and misspellings in Khmer addresses.
- Two-Part Processing: Splits addresses into `address_1` (ផ្ទះ, ផ្លូវ, ភូមិ) and `address_2` (ឃុំ, district, province).
- Dictionary Support: Loads correction dictionaries from text files or folders.
- Custom Logic: Handles unique Khmer terms like ផ្ទះ (house) and ផ្លូវ (road) with specific rules.
- Unicode Normalization: Ensures consistent Khmer text processing.

## Requirements
- Python 3.x
- Required packages:
    - `jellyfish` (for Damerau-Levenshtein distance)
    - `regex` (for advanced pattern matching)
    - `unicodedata` (included in Python standard library)
    - `pkg_resources` (included with `setuptools`)


## Installation

Install the library via `pip`:

```bash
pip install autocorrect_kh
```

Or Install from source

```bash
git clone https://github.com/monykappa/autocorrect-kh.git
```

## Usage
### Autocorrect for `address_1` and `address_2`
```bash
from autocorrect_kh import autocorrect_address_1, autocorrect_address_2

address_1 = "ផ្ទ៤១បេ ផ្លុវ៤៤៤ ភុមិ២"
address_2 = "សង្កាត់ទលទពូងទី ២ ខណ្ឌចំករមន ភ្នំពញ"


address_1_text = autocorrect_address_1(address_1) # Output: ផ្ទះ៤១បេ ផ្លូវ៤៤៤ ភូមិ២
address_2_text = autocorrect_address_2(address_2) # Output: សង្កាត់ទួលទំពូងទី២ ខណ្ឌចំការមន ភ្នំពេញ

print("Autocorrected Address:", address_1_text + " " + address_2_text)
```

### Autocorrect Address Separately
```bash
from autocorrect_kh import autocorrect_province, autocorrect_district, autocorrect_khum, autocorrect_phum

phum_text = "កូមិត្រពាងថ្លង២"
khum_text = "សង្កាក់ច្បាអំពៅ២"
district_text = "ខណ្ឌចំករមន"
province_text = "កំពង់ចម"

autocorrect_phum = autocorrect_phum(phum_text)
autocorrect_khum = autocorrect_khum(khum_text)
autocorrect_district = autocorrect_district(district_text)
autocorrect_province = autocorrect_province(province_text)

print(f"Original phum {phum_text} -> autocorrected phum {autocorrect_phum}") # Output: ភូមិត្រពាំងថ្លឹង២
print(f"Original khum {khum_text} -> autocorrected khum {autocorrect_khum}") # Output:​​ ​សង្កាត់ច្បារអំពៅ២
print(f"Original district {district_text} -> autocorrected district {autocorrect_district}") # Output:​ ខណ្ឌចំការមន
print(f"Original province {province_text} -> autocorrected province {autocorrect_province}") # Output: កំពង់ចាម
```

# How It Works
## Address Breakdown
Khmer National ID addresses are split into:

1. `address_1:` Contains ផ្ទះ (house), ផ្លូវ (road), and ភូមិ (village/phum).
2. `address_2`: Contains ឃុំ/សង្កាត់ (commune/khum), district, and province.

## Correction Flow
### Address 1: House, Road, Village
- ផ្ទះ (House) and ផ្លូវ (Road):
    - Corrected using hardcoded rules (not from dictionaries) due to their unique patterns, often followed by numbers or identifiers.
    - Examples:
        - `ផ្ទ១១៣` → `ផ្ទះ១១៣` 
        - `ផ្លូរបេតុង` → `ផ្លូវបេតុង` 
- ភូមិ (Village/Phum):
    - First checks and corrects the prefix ភូមិ (e.g., `ភុមិ` → `ភូមិ`).
    - Then corrects the village name after ភូមិ using the phum_dict (loaded from data/phum/).
    - Note: The phum dictionary excludes the word ភូមិ because it’s inconsistently present on ID cards.
    - Example:
        - Input: `ភុមិស្វយព្រៃ`
        - Step 1: `ភុមិ` → `ភូមិ`
        - Step 2: `ស្វយព្រៃ` → `ស្វាយព្រៃ` (using phum_dict)
        - Output: `ភូមិស្វាយព្រៃ`
### Address 2: Commune, District, Province
- Corrected directly using automatically loaded dictionaries from:
    - `data/khum/` for khum
    - `data/district.txt` for district
    - `data/province.txt` for province
- No prefix-specific rules; full names are matched and corrected.
- Example:
    - Input: `សង្កាត់បឹងត្រុបែក ខណ្ឌចំករមន ភ្នំពញ`
    - Output: `សង្កាត់បឹងត្របែក ខណ្ឌចំការមន ភ្នំពេញ` (corrected using dictionaries)
### Separate Autocorrect Functions (v0.3.0)
The `autocorrect_kh` package now includes dedicated functions to autocorrect individual components of Khmer addresses. This allows you to correct specific parts of an address—such as village (phum), commune (khum), district, or province—independently, offering greater flexibility alongside the combined address correction features.

- `autocorrect_phum(phum_text)`:
    Corrects village names, handling the prefix ភូមិ (phum) separately. It ensures the prefix is standardized (e.g., correcting ភុមិ to ភូមិ) and then corrects the village name using the phum_dict dictionary.
- Example:
    - Input: `កូមិត្រពាងថ្លង២`
    - Output: `ភូមិត្រពាំងថ្លឹង២`
- `autocorrect_khum(khum_text)`:
    Corrects commune (khum) names using the `khum_dict` dictionary.
- Example:
    - Input: `សង្កាក់ច្បាអំពៅ២`
    - Output: `សង្កាត់ច្បារអំពៅ២`
- `autocorrect_district(district_text)`:
    Corrects district names using the district_dict dictionary.
- Example:
    - Input: `ខណ្ឌចំករមន`
    - Output: `ខណ្ឌចំការមន`
- `autocorrect_province(province_text)`:
    Corrects province names using the province_dict dictionary.
- Example:
    - Input: `កំពង់ចម`
    - Output: `កំពង់ចាម`
These functions provide consistent and accurate corrections for individual address components, whether used on their own or as part of a broader address correction workflow.
# Key Functions
### Load Dictionary
- `normalize_text(text)`: Normalizes Khmer Unicode to NFC for consistent processing.
- `load_resource_text(resource_path)`: Loads raw text from a package resource file.
- `load_autocorrect_dict_from_resource(resource_path)`: Loads a dictionary from a single text file (e.g., `district.txt`).
- `load_autocorrect_dicts_from_resource(folder_resource)`: Loads dictionaries from a folder (e.g., `data/phum/`).
### Autocorrect Specifically for `address_1` and `address_2`
- `autocorrect_address_1(part, dictionary=phum_dict)`: Corrects `address_1` with custom rules.
- `autocorrect_address_2(address_2_text, khum_dictionary=khum_dict, district_dictionary=district_dict, province_dictionary=province_dict)`: Corrects `address_2` (commune, district, province) using dictionaries.
### Autocorrect Phum, Khum, District, and Province Separately
- `autocorrect_phum(phum_text)`: Corrects village names (e.g., `កូមិត្រពាងថ្លង២` → `ភូមិត្រពាំងថ្លឹង២`).
- `autocorrect_khum(khum_text)`: Corrects commune names using `khum_dict`.
- `autocorrect_district(district_text)`: Corrects district names using `district_dict`.
- `autocorrect_province(province_text)`: Corrects province names using `province_dict`.