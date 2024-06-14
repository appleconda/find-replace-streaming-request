import os
import json
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from stream_parser import KMPSearch
import logging
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = FastAPI()

mappings = [["Mark", "Jasmine"]]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def make_api_request(method, url, headers=None, data=None, params=None, stream=False):
    try:
        response = requests.request(method, url, headers=headers, json=data, params=params, stream=stream)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTPError: {str(e)}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

@app.post('/v1/chat/completions')
async def get_streaming_response(request: Request):
    with open('app.log', 'w'):
        pass
    request_data = await request.json()

    def event_stream():
        global mappings
        api_url = f"https://api.openai.com/v1/chat/completions"
        try:
            response = make_api_request('POST', api_url, headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                                        data=request_data, stream=True)
            if response.status_code == 200:
                chunk_iter = response.iter_content(chunk_size=1024)
                for chunk in KMPSearch(mappings, chunk_iter, logger):
                    # Decode and print the chunk for debugging purposes
                    # decoded_chunk = chunk.decode('utf-8')
                    # logger.info(f"[Main] Chunk yielded by KMPSearch: {decoded_chunk}")
                    yield chunk
            else:
                yield json.dumps({"error": "Failed to stream response"}).encode('utf-8')
                logger.error(f"Failed to stream response with status code: {response.status_code}")
        except Exception as e:
            yield json.dumps({"error": "Failed to stream response due to an internal error"}).encode('utf-8')
            logger.error(f"Failed to stream response due to an internal error: {str(e)}")

    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
