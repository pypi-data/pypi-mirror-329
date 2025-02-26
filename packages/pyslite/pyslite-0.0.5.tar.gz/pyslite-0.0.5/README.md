# pySlite

[![PyPI package](https://img.shields.io/badge/pip%20install-pyslite-brightgreen)](https://pypi.org/project/pyslite/)
[![version number](https://img.shields.io/pypi/v/pyslite?color=green&label=version)](https://pypi.org/project/pyslite/)
[![Actions Status](https://github.com/oddaspa/pyslite/workflows/Build%20status/badge.svg)](https://github.com/oddaspa/pyslite/actions)
[![PyPI downloads](https://img.shields.io/pypi/dm/pyslite.svg)](https://pypistats.org/packages/pyslite)
[![License](https://img.shields.io/github/license/oddaspa/pyslite)](https://github.com/oddaspa/pyslite/blob/main/LICENSE.txt)

Unofficial Python SDK for Slite API.

## Installation

```sh
$ pip install pyslite
```

## Usage

This SDK provides a simple way to interact with the Slite API. Here's how to use it:

```python
from pyslite.client import Client

# Replace with your actual API key
api_key = "YOUR_SLITE_API_KEY"
client = Client(api_key)

# Get a note by ID
note = client.get_note("your_note_id")
if note:
    print(f"Note Title: {note.title}")
    print(f"Note Content: {note.content}") #Note content is markdown
else:
    print("Failed to retrieve note.")

# Create a new note
response = client.create_note(
    parent_note_id="your_parent_note_id",
    template_id="your_template_id",
    title="My New Note",
    content="# My New Note\nThis is the content of my new note."
)
if response:
    print(f"Note created successfully! Status code: {response.status_code}")
else:
    print("Failed to create note.")

#Fetch all notes recursively under a given note.
all_notes = client.fetch_notes_recursive("your_root_note_id")
if all_notes:
    for note in all_notes:
        print(f"Note Title: {note.title}")
else:
    print("Failed to fetch notes.")
```

Remember to replace "your_note_id", "your_parent_note_id", "your_template_id", and "your_root_note_id" with actual Slite note IDs.

## Features

- Get Note: Retrieves a single note by its ID.
- Create Note: Creates a new note with specified parent, template, title, and markdown content.
- Fetch Notes Recursively: Retrieves a note and all its children recursively.

## Error Handling

The library includes robust error handling. If a request fails, it will print an informative error message to the console and return None.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
