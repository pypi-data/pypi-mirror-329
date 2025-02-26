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
from utils.note import Note

class Client():

    def __init__(self, API_KEY):
        self.api_key = API_KEY
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-slite-api-key': API_KEY
        }
        self.base_url = "https://api.slite.com/v1/"
    
    
    def get_note(self, noteId):
        url = self.base_url + f"notes/{noteId}?format=md"
        response = requests.get(url, headers=self.headers)
        if response.ok:
            note = Note(**response.json())
        else:
            note = None
        return note
    
    def create_note(
        self,
        parentNoteId: str,
        templateId: str,
        title:str,
        content: str
    ):
      url = self.base_url + f"notes/"
      response = requests.post(
          url,
          json={
              "title": title,
              "parentNoteId": parentNoteId,
              "templateId": templateId,
              "content": content
          },
          headers=self.headers
      )
      return response