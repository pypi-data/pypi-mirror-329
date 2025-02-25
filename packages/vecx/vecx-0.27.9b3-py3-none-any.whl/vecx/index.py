import requests, json, zlib
import numpy as np
from google.protobuf.json_format import Parse, MessageToJson
from .libvx import encode, decode, encode_vector
from .crypto import get_checksum,json_zip,json_unzip
from .exceptions import raise_exception
from .vecx_pb2 import VectorObject, VectorBatch, ResultSet, VectorResult

class Index:
    def __init__(self, name:str, key:str, token:str, url:str, dimension:int, space_type:str="cosine", version:int=1):
        self.name = name
        self.key = key
        self.token = token
        self.url = url
        self.space_type = space_type
        self.dimension = dimension
        self.version = version
        self.checksum = get_checksum(self.key)
        self.num_rows = 0

    def __str__(self):
        return self.name
    
    def _normalize_vector(self, vector):
        # Normalize only if using cosine distance
        if self.space_type != "cosine":
            return vector, 1.0
        vector = np.array(vector, dtype=np.float32)
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector, 1.0
        normalized_vector = vector / norm
        return normalized_vector.tolist(), float(norm)

    def upsert(self, input_array):
        if len(input_array) > 1000:
            raise ValueError("Cannot insert more than 1000 vectors at a time")

        batch = VectorBatch()
        for item in input_array:
            # Prepare vector object
            vector_obj = VectorObject()
            vector_obj.id = str(item.get('id', ''))
            vector_obj.filter = json.dumps(item.get('filter', ""))
            # Meta is zipped
            meta = json_zip(dict=item.get('meta', ""))
            vector_obj.meta = meta
            vector, norm = self._normalize_vector(item['vector'])
            vector_obj.vector.extend(vector)
            vector_obj.norm = norm
            
            # Encode the vector
            # if self.checksum >= 0:
            #     # TODO: Implement your vector encoding logic here
            #     encoded_vector = self._encode_vector(item['vector'])
            #     vector_obj.vector.extend(encoded_vector)
            # else:
            #     vector_obj.vector.extend(item['vector'])

            # Add to batch
            batch.vectors.append(vector_obj)
        # Serialize batch
        serialized_data = batch.SerializeToString()
        # Prepare headers
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/x-protobuf'
        }

        # Send request
        response = requests.post(
            f'{self.url}/index/{self.name}/vector/batch', 
            headers=headers, 
            data=serialized_data
        )

        if response.status_code != 200:
            raise_exception(response.status_code, response.text)

        return "Vectors inserted successfully"

        
    def query(self, vector, top_k=10, filter=None, include_vectors=False, log=False):
        if top_k > 100:
            raise ValueError("top_k cannot be greater than 100")
        checksum = get_checksum(self.key)

        # Normalize query vector if using cosine distance
        normalized_vector, _ = self._normalize_vector(vector)

        #encoded_vector = encode_vector(key=self.key,lib_token=self.lib_token,space_type=self.space_type, version=self.version, vector=vector)
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'vector': normalized_vector,
            'k': top_k,
            'include_vectors': include_vectors
        }
        if filter:
            data['filter'] = json.dumps(filter)
        response = requests.post(f'{self.url}/index/{self.name}/search', headers=headers, json=data)
        if response.status_code != 200:
            raise_exception(response.status_code, response.text)

        # Parse protobuf ResultSet
        result_set = ResultSet()
        result_set.ParseFromString(response.content)

        # Convert to a more Pythonic list of dictionaries
        processed_results = []
        for result in result_set.results:
            processed_result = {
                'id': result.id,
                'distance': result.distance,
                'similarity': 1 - result.distance,
                'meta': json_unzip(result.meta)
            }
            # Filter will come as "" - default value in protobuf
            if filter != "":
                processed_result['filter'] = json.loads(result.filter)

            # Include vector if requested and available
            if include_vectors and result.vector:
                processed_result['vector'] = list(result.vector)

            processed_results.append(processed_result)

        return processed_results

    def delete_vector(self, id):
        checksum = get_checksum(self.key)
        headers = {
            'Authorization': f'{self.token}',
            }
        response = requests.delete(f'{self.url}/index/{self.name}/vector/{id}/delete', headers=headers)
        if response.status_code != 200:
            raise_exception(response.status_code)
        return response.text + " rows deleted"
    
    # Delete multiple vectors based on a filter
    def delete_with_filter(self, filter):
        checksum = get_checksum(self.key)
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
            }
        data = {"filter": filter}
        print(filter)
        response = requests.delete(f'{self.url}/index/{self.name}/vectors/delete', headers=headers, json=data)
        if response.status_code != 200:
            print(response.text)
            raise_exception(response.status_code)
        return response.text
    
    def describe(self):
        checksum = get_checksum(self.key)
        headers = {
            'Authorization': f'{self.token}',
        }
        response = requests.get(f'{self.url}/index/{self.name}/info', headers=headers)
        if response.status_code != 200:
            raise_exception(response.status_code)
        data = {
            "name": self.name,
            "dimension": self.dimension,
            "space_type": self.space_type,
            "num_rows": self.num_rows
        }
        return data

