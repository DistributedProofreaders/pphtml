#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
language_registry_to_json.py

Reads the IANA language subtag registry file and extracts language subtag
information, writing it to a JSON file.

The output JSON maps lowercase subtag strings to lists of description strings,
for example:
    {
        "en": ["English"],
        "fr": ["French"],
        "zh": ["Chinese"],
        ...
    }

(To shrink the file, the JSON is compacted and not human-readable like above.)

Usage:
    python language_registry_to_json.py
    python language_registry_to_json.py --registry language-subtag-registry
    python language_registry_to_json.py --registry language-subtag-registry --output language-subtag-registry.json
"""

import argparse
import json
import os
import sys


def parse_registry(registry_path):
    """
    Parse the IANA language subtag registry file.
    Returns a dict mapping lowercase subtag -> list of description strings.
    Only records with Type: language are included.
    """
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        sys.exit(f"error: cannot open registry file {registry_path}: {e}")

    lang_map = {}
    for record in content.split("%%"):
        record = record.strip()
        if not record:
            continue
        record_type = ""
        subtag = ""
        descriptions = []

        for line in record.split("\n"):
            if ": " in line:
                key, _, value = line.partition(": ")
                key = key.strip()
                value = value.strip()
                if key == "Type":
                    record_type = value
                elif key == "Subtag":
                    subtag = value
                elif key == "Description":
                    descriptions.append(value)

        if record_type == "language" and subtag:
            lang_map[subtag.lower()] = descriptions

    return lang_map


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    default_registry = os.path.join(script_dir, "language-subtag-registry")
    default_output = os.path.join(script_dir, "language-subtag-registry.json")

    parser = argparse.ArgumentParser(
        description="Convert IANA language subtag registry to JSON"
    )
    parser.add_argument(
        "--registry",
        default=default_registry,
        help="path to language-subtag-registry file (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        default=default_output,
        help="path to output JSON file (default: %(default)s)",
    )
    args = parser.parse_args()

    lang_map = parse_registry(args.registry)
    print(f"extracted {len(lang_map)} language subtags")

    with open(args.output, "w", encoding="utf-8") as f:
        # We can't force to ASCII - some language names contain non-ASCII.
        # Change the separators to shrink file (~8% at time of writing).
        json.dump(lang_map, f, ensure_ascii=False, separators=(',', ':'))
        f.write("\n")

    print(f"wrote {args.output}")


if __name__ == "__main__":
    sys.exit(main())
