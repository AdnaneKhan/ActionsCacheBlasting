import argparse
import requests
import json
import os
import string

parser = argparse.ArgumentParser(description='Upload cache to GitHub Actions')
parser.add_argument('--file-path', dest='file_path', required=True, help='Path to the tzstd archive to upload.')
parser.add_argument('--key', dest='key', required=True, help='Cache key (String)')
parser.add_argument('--version', dest='version', required=True, help='Cache version (String)')
parser.add_argument('--auth-token', dest='auth_token', required=True, help='Actions Runtime Authentication token')
parser.add_argument('--cache-url', dest='cache_url', required=True, help='URL for the cache API')
args = parser.parse_args()

headers = {
    'accept': 'application/json;api-version=6.0-preview.1',
    'content-type': 'application/json',
    'user-agent': 'actions/cache',
    'Authorization': f'Bearer {args.auth_token}',
}

data = {
    "key": args.key,
    "version": args.version,
    # This isn't checked, just need a valid number.
    "cacheSize": 1337
}

response = requests.post(args.cache_url, headers=headers, json=data)
if response.status_code == 201:
    cache_id = response.json()['cacheId']
    file_path = args.file_path
    with open(file_path, 'rb') as f:
        file_data = f.read()

    patch_headers = {
        "Content-Type": "application/octet-stream",
        "Content-Range": f"bytes 0-{len(file_data) -1}/*"
    }
    patch_headers.update(headers)
    patch_response = requests.patch(args.cache_url + '/' + str(cache_id), headers=patch_headers, data=file_data)
    if patch_response.status_code == 204:
        file_size = os.path.getsize(file_path)
        size_data = {
            "size": file_size
        }
        post_response = requests.post(args.cache_url + '/' + str(cache_id), headers=headers, json=size_data)
        print(post_response.status_code)
        print(post_response.text)
    else:
        print(patch_response.status_code)
        print(patch_response.text)
else:
    print(f"Unable to get cache pre-signed upload URL, status code was: {str(response.status_code)}")
    print(response.text)
