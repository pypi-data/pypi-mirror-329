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
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests import Response
from .utils.note import Note
from .utils.notes_response import NotesResponse
from typing import Optional, List
import time


class Client:
    """
    A client for interacting with the Slite API.
    """

    def __init__(self, api_key: str, max_retries: int = 3, backoff_factor: float = 1.0):
        """Initializes the Slite API client.

        Args:
            api_key: Your Slite API key.
            max_retries: Maximum number of retries for failed requests.
            backoff_factor: Multiplier for exponential backoff (seconds).
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
        self.session = requests.Session()
        retries = Retry(
            
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504]  # Retry on these status codes
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))


    def _request(self, method: str, url: str, **kwargs) -> Optional[Response]:
        """Makes a request to the Slite API with retry logic."""
        try:
            response = self.session.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return None


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
        response = self._request("GET", url)
        if response:
            try:
                return Note(**response.json())
            except ValueError as e:
                print(f"Error parsing JSON response: {e}")
                return None
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
        return self._request("POST", url, json=payload)


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
        response = self._request("GET", url)
        if response:
            try:
                response_data = NotesResponse(**response.json())
                all_notes = []
                if response_data.total > 0:
                    all_notes.append(self.get_note(note_id)) #add parent note.
                    for child in response_data.notes:
                        child_notes = self.fetch_notes_recursive(child.id)
                        all_notes.extend(child_notes)
                return all_notes
            except ValueError as e:
                print(f"Error parsing JSON response: {e}")
                return []
        return []

