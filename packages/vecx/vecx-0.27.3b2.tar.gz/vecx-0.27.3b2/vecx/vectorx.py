import requests
import secrets
from vecx.exceptions import raise_exception
from vecx.index import Index
from vecx.user import User
from vecx.crypto import get_checksum
from vecx.utils import is_valid_index_name

SUPPORTED_REGIONS = ["us-west", "india-west", "local"]
class VectorX:
    def __init__(self, token:str|None=None):
        self.token = token
        self.region = "local"
        self.base_url = "http://127.0.0.1:8080/api/v1"
        # Token will be of the format user:region:token
        if token:
            token_parts = self.token.split(":")
            if len(token_parts) > 2:
                self.region = token_parts[2]
                if self.region not in SUPPORTED_REGIONS:
                    raise ValueError(f"Invalid region: {self.region}")
            if self.region == "us-west":
                self.base_url = "https://us-west.vectorxdb.ai"
            elif self.region == "india-west":
                self.base_url = "https://india-west.vectorxdb.ai"
        self.version = 1

    def __str__(self):
        return self.token

    def set_token(self, token:str):
        self.token = token
        self.region = self.token.split (":")[1]
    
    def set_base_url(self, base_url:str):
        self.base_url = base_url
    
    def generate_key(self)->str:
        # Generate a random hex key of length 32
        key = secrets.token_hex(16)  # 16 bytes * 2 hex chars/byte = 32 chars
        print("Store this encryption key in a secure location. Loss of the key will result in the irreversible loss of associated vector data.\nKey: ",key)
        return key

    def create_index(self, name:str, dimensions:int, key:str|None, distance_metric:str, use_fp16:bool=True, version:int=None):
        if is_valid_index_name(name) == False:
            raise ValueError("Invalid index name. Index name must be alphanumeric and can contain underscores and less than 48 characters")
        distance_metric = distance_metric.lower()
        if distance_metric not in ["cosine", "l2", "ip"]:
            raise ValueError(f"Invalid distance metric: {distance_metric}")
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'index_name': name,
            'dim': dimensions,
            'max_elements': 1000000,
            'space_type': distance_metric,
            'M':16,
            'ef_construction': 200,
            'checksum': get_checksum(key),
            'use_fp16': use_fp16,
            'version': version
        }
        response = requests.post(f'{self.base_url}/index/create', headers=headers, json=data)
        if response.status_code != 200:
            print(response.text)
            raise_exception(response.status_code)
        return "Index created successfully"

    def list_indexes(self):
        #print("Token: ", self.token)
        headers = {
            'Authorization': f'{self.token}',
        }
        response = requests.get(f'{self.base_url}/index/list', headers=headers)
        if response.status_code != 200:
            raise_exception(response.status_code)
        indexes = response.json()
        for index in indexes:
            index['name'] = '_'.join(index['name'].split('_')[2:])
        return indexes
    
    # TODO - Delete the index cache if the index is deleted
    def delete_index(self, name:str, key:str):
        # Get index details from the server. Delete at the edge and then delete at the server
        headers = {
            'Authorization': f'{self.token}',
        }
        response = requests.get(f'{self.base_url}/index/{name}/get', headers=headers)
        if response.status_code != 200:
            raise_exception(response.status_code)
        data = response.json()
        edge_url = data['edge_url']
        checksum = get_checksum(key)
        headers = {
            'Authorization': f'{self.token}:{name}:{checksum}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{edge_url}/index/{name}/delete', headers=headers)
        if response.status_code != 200:
            print(response.text)
            raise_exception(response.status_code)
        headers = {
            'Authorization': f'{self.token}',
        }
        response = requests.get(f'{self.base_url}/index/{name}/delete', headers=headers)
        if response.status_code != 200:
            print(response.text)
            raise_exception(response.status_code)
        return f'Index {name} deleted successfully'


    def get_index(self, name:str, key:str|None=None):
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }
        # Get index details from the server
        response = requests.get(f'{self.base_url}/index/{name}/info', headers=headers)
        if response.status_code != 200:
            raise_exception(response.status_code)
        data = response.json()
        print(data)
        #print(data)
        # Raise error if checksum does not match
        checksum = get_checksum(key)
        if checksum != data['checksum']:
            raise_exception(460)
        idx = Index(name=name, key=key, token=self.token, url=self.base_url, distance_metric=data['space_type'], dimensions=data['dimension'], version=self.version)
        return idx
    
    def get_user(self):
        return User(self.base_url, self.token)

