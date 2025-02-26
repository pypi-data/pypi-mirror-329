import requests 
import atexit
from typing import Optional
BASE_URL = "https://api.simplex.sh"

import json

class Simplex:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session_id = None
        atexit.register(self.close_session)

    def close_session(self):
        if not self.session_id:
            return
        response = requests.post(
            f"{BASE_URL}/close_session",
            headers={
                'x-api-key': self.api_key
            },
            data={'session_id': self.session_id}
        )
        self.session_id = None
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the close_session action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to close session: {response.json()['error']}")

    def create_session(self, show_in_console: Optional[bool] = True, proxies: Optional[bool] = True):
        response = requests.post(
            f"{BASE_URL}/create_session",
            headers={
                'x-api-key': self.api_key
            },
            data={'proxies': proxies}
        )
        # Check for non-200 status code
        if response.status_code != 200:
            raise ValueError(f"Create session request failed with status code {response.status_code}: {response.text}")
            
        response_json = response.json()
        if 'session_id' not in response_json:
            raise ValueError(f"It looks like the session wasn't created successfully. Did you set your api_key when creating the Simplex class?")
        self.session_id = response_json['session_id']
        livestream_url = response_json['livestream_url']

        if show_in_console:
            print(f"Livestream URL: {livestream_url}")

        return livestream_url

    def goto(self, url: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action goto with url='{url}'")
        
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        data = {'url': url}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/goto",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the goto action failed to return a response. Did you set your api_key when creating the Simplex class?")
    
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to goto url: {response.json()['error']}")

    def click(self, element_description: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action click with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/click",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the click action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return response.json()["element_clicked"]
        else:
            raise ValueError(f"Failed to click element: {response.json()['error']}")

    def type(self, text: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action type with text='{text}'")

        data = {'text': text}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/type",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to type text: {response.json()['error']}")

    def press_enter(self, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError("Must call create_session before calling action press_enter")

        data = {}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/press_enter",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the press_enter action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to press enter: {response.json()['error']}")
        
    def press_tab(self, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError("Must call create_session before calling action press_tab")

        data = {}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/press_tab",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the press_tab action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to press tab: {response.json()['error']}")
        
    def delete_text(self, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError("Must call create_session before calling action delete_text")

        data = {}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/delete_text",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the delete_text action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to delete text: {response.json()['error']}")

    def extract_bbox(self, element_description: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action extract_bbox with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.get(
            f"{BASE_URL}/extract-bbox",
            headers={
                'x-api-key': self.api_key
            },
            params=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the extract_bbox action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return response.json()["bbox"]
        else:
            raise ValueError(f"Failed to extract bbox: {response.json()['error']}")

    def extract_text(self, element_description: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action extract_text with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.get(    
            f"{BASE_URL}/extract-text",
            headers={
                'x-api-key': self.api_key
            },
            params=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the extract_text action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return response.json()["text"]
        else:
            raise ValueError(f"Failed to extract text: {response.json()['error']}")

    def extract_image(self, element_description: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action extract_image with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.get(
            f"{BASE_URL}/extract-image",
            headers={
                'x-api-key': self.api_key
            },
            params=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the extract_image action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return response.json()["image"]
        else:
            raise ValueError(f"Failed to extract image: {response.json()['error']}")

    def scroll(self, pixels: float, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action scroll with pixels={pixels}")

        data = {'pixels': pixels}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/scroll",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the scroll action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to scroll: {response.json()['error']}")

    def wait(self, milliseconds: int, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action wait with milliseconds={milliseconds}")

        data = {'milliseconds': milliseconds}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/wait",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the wait action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to wait: {response.json()['error']}")
    
    def create_login_session(self, url: str, proxies: Optional[bool] = True):
        response = requests.post(
            f"{BASE_URL}/create_login_session",
            headers={
                'x-api-key': self.api_key
            },
            data={'url': url, 'proxies': proxies}
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the create_login_session action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return response.json()["login_session_url"]
        else:
            raise ValueError(f"Failed to create login session: {response.json()['error']}")
    
    def restore_login_session(self, session_data: str, cdp_url: str = None):
        """
        Restore a login session from either a file path or a JSON string.
        
        Args:
            session_data: Either a file path to JSON file or a JSON string
            cdp_url: Optional CDP URL for remote debugging
        """
        try:
            # Try to parse as JSON string first
            session_data_dict = json.loads(session_data)
        except json.JSONDecodeError:
            # If parsing fails, treat as file path
            try:
                with open(session_data, 'r') as f:
                    session_data_dict = json.load(f)
            except Exception as e:
                raise ValueError(f"Failed to load session data. Input must be valid JSON string or path to JSON file. Error: {str(e)}")
        
        data = {
            'session_data': json.dumps(session_data_dict)
        }
        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id
        
        response = requests.post(
            f"{BASE_URL}/restore_login_session",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the restore_login_session action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to restore login session: {response.json()['error']}")

    def click_and_upload(self, element_description: str, file_path: str):
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action click_and_upload with element_description='{element_description}'")

        files = {
            'file': open(file_path, 'rb')
        }
        
        data = {
            'element_description': element_description
        }

        data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/click_and_upload",
            headers={
                'x-api-key': self.api_key
            },
            files=files,
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the click_and_upload action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to click and upload: {response.json()['error']}")
    
    def click_and_download(self, element_description: str):
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action click_and_download with element_description='{element_description}'")
        
        data = {
            'element_description': element_description
        }

        data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/click_and_download",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the click_and_download action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return response.json()["b64"], response.json()["filename"]
        else:
            raise ValueError(f"Failed to click and download: {response.json()['error']}")
    
    def exists(self, element_description: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action exists with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/exists",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the exists action failed to return a response. Did you set your api_key when creating the Simplex class?")
        response_json = response.json()
        if response_json['succeeded']:
            return response_json['exists'], response_json['reasoning']
        else:
            raise ValueError(f"Failed to check if element exists: {response_json['error']}")
