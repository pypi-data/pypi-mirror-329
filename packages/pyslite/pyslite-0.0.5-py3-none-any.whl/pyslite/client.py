"""
Copyright 2024 Odd Gunnar Aspaas

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import requests
from requests import Response
from .utils.note import Note
from .utils.notes_response import NotesResponse  # Import NotesResponse
from typing import Optional, List


class Client:
    """
    A client for interacting with the Slite API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the Slite API client.

        Args:
            api_key: Your Slite API key.
        """
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-slite-api-key": self.api_key,
        }
        self.base_url = "https://api.slite.com/v1/"

    def get_note(self, note_id: str) -> Optional[Note]:
        """
        Retrieves a note from Slite by its ID.

        Args:
            note_id: The ID of the note to retrieve.

        Returns:
            A Note object if the note is found, None otherwise.

        Raises:
            requests.exceptions.RequestException: If there's an error during the HTTP request.
        """
        url = self.base_url + f"notes/{note_id}?format=md"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return Note(**response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error fetching note: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing JSON response when fetching note: {e}")
            return None

    def create_note(
        self, parent_note_id: str, template_id: str, title: str, content: str
    ) -> Optional[Response]:
        """
        Creates a new note in Slite.

        Args:
            parent_note_id: The ID of the parent note.
            template_id: The ID of the template to use.
            title: The title of the new note.
            content: The content of the new note.

        Returns:
            The response object from the Slite API, or None if failed.
        Raises:
            requests.exceptions.RequestException: If there's an error during the HTTP request.
        """

        url = self.base_url + "notes/"
        payload = {
            "title": title,
            "parentNoteId": parent_note_id,
            "templateId": template_id,
            "markdown": content,
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error creating note: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing JSON response when creating note: {e}")
            return None

    def fetch_notes_recursive(self, note_id: str) -> List[Note]:
        """
        Recursively fetches all child notes of a given note.

        Args:
            note_id: The ID of the parent note.

        Returns:
            A list of Note objects, including the parent note and all its descendants.

        Raises:
            requests.exceptions.RequestException: If there's an error during the HTTP request.
            ValueError: If there's an error parsing the JSON response.
        """
        url = self.base_url + f"notes/{note_id}/children"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            response_data = NotesResponse(**response.json())

            all_notes: List[Note] = []
            # Add parent note.
            parent_note = self.get_note(note_id)
            if parent_note:
                all_notes.append(parent_note)
            # Recursivly loop through children.
            if response_data.total > 0:
                for child in response_data.notes:
                    child_id = child.id
                    child_notes = self.fetch_notes_recursive(child_id)
                    all_notes.extend(child_notes)
            return all_notes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching children of note {note_id}: {e}")
            return []
        except ValueError as e:
            print(f"Error parsing JSON response when fetching children of note {note_id}: {e}")
            return []

