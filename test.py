import requests

def test_streaming_api(url, headers=None):
    # Make a GET request to the streaming API endpoint
    with requests.post(url, headers=headers, stream=True) as response:
        if response.status_code == 200:
            print("Connected to the streaming API.")
            # Iterate over the response in chunks
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    print(chunk.decode('utf-8'))
        else:
            print(f"Failed to connect. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace with your streaming API URL
    STREAMING_API_URL = "http://localhost:8000/v1/chat/completions"
    test_streaming_api(STREAMING_API_URL)
