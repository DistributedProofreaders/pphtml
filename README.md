# pphtml
HTML tests for Project Gutenberg texts

## Language subtag registry

This project uses IANA's language subtag registry ([IANA page][1]). This
registry may change over time and should be occasionally refreshed.

The raw registry file is available for download at:

<https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry>

### Updating the registry

1. Download a fresh copy of the registry file:

   ```sh
   curl -L -O https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
   ```

2. Regenerate the JSON file from the updated registry file:

   ```sh
   python3 language_registry_to_json.py
   ```

   The script accepts optional arguments if you need non-default paths:

   ```sh
   python3 language_registry_to_json.py \
       --registry language-subtag-registry \
       --output language-subtag-registry.json
   ```

[1]: https://www.iana.org/assignments/language-subtags-tags-extensions/language-subtags-tags-extensions.xhtml#language-subtags
