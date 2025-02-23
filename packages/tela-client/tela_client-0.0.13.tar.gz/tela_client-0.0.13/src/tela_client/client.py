import base64
import json
import os
import requests
import pandas as pd
import hashlib
import pickle
from pathlib import Path
from datetime import datetime, timedelta


def encoded(filepath):
    with open(filepath, "rb") as file:
        encoded_content = base64.b64encode(file.read()).decode("utf-8")
    return f"data:application/pdf;base64,{encoded_content}"


def file(filepath, parser_type="tela-pdf-parser", range=None, **options):
    file_options = options.copy()
    file_options["parserType"] = parser_type
    if range is not None:
        file_options["range"] = range
    print(filepath)
    file_url = filepath if filepath and filepath.startswith(('http://', 'https://')) else encoded(filepath) if filepath else None
    
    return {
        "file_url": file_url,
        "options": file_options
    }

def files(file_paths, parser_type="tela-pdf-parser", range=None, **options):
    """
    Create a files payload from a list of file paths with optional parameters.
    
    Args:
        file_paths (list): List of file paths or URLs to process
        parser_type (str, optional): Type of parser to use. Defaults to "tela-pdf-parser"
        range (str, optional): Page range to process. Defaults to None
        **options: Additional options to pass to the parser
        
    Returns:
        dict: Files payload with list of processed files
    """
    file_list = []
    for f in file_paths:
        file_list.append(file(f, parser_type=parser_type, range=range, **options))
        
    return {
        "files": file_list
    }

class TelaClient:
    def __init__(self, api_key, api_url="https://api.tela.com", max_attempts=3, cache_dir=".tela_cache"):
        self.api_key = api_key
        self.api_url = api_url
        self.max_attempts = max_attempts
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def upload_file(self, file_path):
        """
        Upload a file to Tela API and return the download URL
        
        Args:
            file_path (str): Path to the file to upload
            
        Returns:
            str: Download URL for the uploaded file
        """
        # Check if file exists in cache
        file_hash = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()
        cache_key = f"upload_{file_hash}"
        
        cached_response = self._get_cached_response(cache_key, check_age=True)
        if cached_response:
            return cached_response['download_url']
            
        # Get upload URL from Tela API
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.post(f'{self.api_url}/v2/file', headers=headers)
        upload_url = response.json()['upload_url']
        
        # Upload file to the provided URL
        with open(file_path, 'rb') as file:
            upload_response = requests.put(upload_url, data=file)
            upload_response.raise_for_status()
        
        # Cache the response
        self._cache_response(cache_key, response.json())
        
        # Return the download URL
        return response.json()['download_url']

    def _get_cache_key(self, documents, canvas_id, override):
        # Create a string containing all input parameters
        cache_str = f"{json.dumps(documents, sort_keys=True)}_{canvas_id}_{json.dumps(override, sort_keys=True) if override else ''}"
        # Create a hash of the input parameters
        return hashlib.sha256(cache_str.encode()).hexdigest()

    def _get_cached_response(self, cache_key, check_age=False):
        cache_file = self.cache_dir / f"{cache_key}.pickle"
        if cache_file.exists():
            if check_age:
                cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
                if cache_age >= timedelta(hours=12):
                    return None
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None

    def _cache_response(self, cache_key, response):
        cache_file = self.cache_dir / f"{cache_key}.pickle"
        with open(cache_file, 'wb') as f:
            pickle.dump(response, f)

    def clear_canvas_cache(self, canvas_id):
        # Iterate through all cache files
        cleared_count = 0
        for cache_file in self.cache_dir.glob("*.pickle"):
            # Read the cache file to check if it contains the canvas_id
            with open(cache_file, 'rb') as f:
                try:
                    cache_data = pickle.load(f)
                    # Check if the cache entry is related to the specified canvas_id
                    if isinstance(cache_data, dict) and cache_data.get("uses") == canvas_id:
                        # Delete the cache file
                        cache_file.unlink()
                        cleared_count += 1
                except:
                    # Skip if there's any error reading the cache file
                    continue
        return cleared_count

    def clear_all_cache(self):
        # Delete all cache files in the cache directory
        cleared_count = 0
        for cache_file in self.cache_dir.glob("*.pickle"):
            try:
                cache_file.unlink()
                cleared_count += 1
            except:
                continue
        return cleared_count

    def request(self, documents, canvas_id, override=None, use_cache=True):
        if use_cache:
            cache_key = self._get_cache_key(documents, canvas_id, override)
            cached_response = self._get_cached_response(cache_key)
            if cached_response:
                return cached_response

        try:
            # print("v2")
            url = f"{self.api_url}/v2/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            data = {
                "canvas_id": canvas_id,
                "variables": documents,
                "long_response": True,
            }
            print(data)
            if override:
                data["override"] = override
            # print(data)
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print(response.json())
            if response.status_code != 200:
                print(response.status_code)
                print(response.json())
                return response.json()
            response_data = response.json()
            
            if use_cache:
                self._cache_response(cache_key, response_data)
                
            return response_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def new_canvas(self, canvas_id, expected_input=None):
        return Canvas(self, canvas_id, expected_input, self.max_attempts)


class Canvas:
    def __init__(self, tela_client, canvas_id, expected_input=None, max_attempts=3):
        self.canvas_id = canvas_id
        self.tela_client = tela_client
        self.expected_input = expected_input
        self.max_attempts = max_attempts

    def run(self, output_type='json', override=None, use_cache=True, **kwargs):
        documents = {}
        if self.expected_input:
            for i in self.expected_input:
                if i in kwargs:
                    documents[i] = kwargs[i]
                else:
                    raise ValueError(f"Missing expected input: {i}")
        else:
            documents = kwargs

        attempts = 0
        response = None
        while attempts < self.max_attempts:
            response = self.tela_client.request(documents, self.canvas_id, override, use_cache)
            if response and "choices" in response and len(response["choices"]) > 0:
                break
            attempts += 1

        if response and "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            if output_type == 'dataframe':
                return self._json_to_dataframe(content)
            return content
        return None

    def run_batch(self, inputs, output_type='json', max_workers=5, use_cache=True):
        print("will run batch")
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def process_input(index, input_data):
            print("running for")
            result = self.run(output_type=output_type, use_cache=use_cache, **input_data)
            print("finished running")
            return {'input': input_data.get('name', f'input_{index}'), 'result': result}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_input, i, input_data) for i, input_data in enumerate(inputs)]
            results = []
            for future in as_completed(futures):
                results.append(future.result())

        return results

    def _json_to_dataframe(self, json_data):
        def flatten_json(data, prefix=''):
            items = {}
            for key, value in data.items():
                new_key = f"{prefix}{key}"
                if isinstance(value, dict):
                    items.update(flatten_json(value, f"{new_key}_"))
                elif isinstance(value, list):
                    items[new_key] = json.dumps(value)
                else:
                    items[new_key] = value
            return items

        def process_json(data):
            if isinstance(data, dict):
                return [flatten_json(data)]
            elif isinstance(data, list):
                return [flatten_json(item) if isinstance(item, dict) else item for item in data]

        processed_data = process_json(json_data)
        df = pd.DataFrame(processed_data)

        # Expand columns that contain JSON strings (lists or list of objects)
        for column in df.columns:
            try:
                df[column] = df[column].apply(json.loads)
                if df[column].apply(lambda x: isinstance(x, list)).all():
                    if isinstance(df[column].iloc[0][0], dict):
                        # Handle list of objects
                        expanded_df = pd.json_normalize(df[column].explode().tolist())
                        expanded_df.index = df.index.repeat(df[column].str.len())
                        expanded_df.columns = [f"{column}_{subcol}" for subcol in expanded_df.columns]
                        df = df.drop(columns=[column]).join(expanded_df)
                    else:
                        # Handle simple lists
                        df = df.explode(column)
            except:
                pass

        return df


# EXAMPLE USAGE
# from tela.tela import TelaClient, file

# TELA_API_KEY = "Your API KEY"
# tela_client = TelaClient(TELA_API_KEY)

# canvas_id = "2b57f4ae-c48e-4883-a0a4-130a573ffdfc"
# canvas = tela_client.new_canvas(canvas_id, expected_input=['document'])

# FILE_NAME = "./Cartao CNPJ produtor.pdf"
# canvas.run(document=file(FILE_NAME))