import os
import json
import asyncio
import logging
import functools
import threading
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv
import openai
import aiohttp

# Load environment variables
load_dotenv()

# Setup logging
LOG_FILE = "maya_optimize.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Cache storage
CACHE_FILE = "maya_cache.json"
cache = {}

# Batch requests queue
BATCH_REQUESTS = defaultdict(list)
BATCH_SIZE = 5
BATCH_TIME_LIMIT = 10  # seconds

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# 🔄 **Load Cache from File**
def load_cache():
    global cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
                logging.info("Cache loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load cache: {str(e)}")


# 💾 **Save Cache to File**
def save_cache():
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=4)  # Added indentation for readability
        logging.info("Cache saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save cache: {str(e)}")


# 🚀 **Cache Wrapper for API Calls**
def cache_results(ttl=300):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            now = datetime.utcnow()

            # Check cache
            if key in cache and now - datetime.fromisoformat(cache[key]["timestamp"]) < timedelta(seconds=ttl):
                logging.info(f"Cache hit for {key}")
                return cache[key]["result"]

            # Execute function & store result
            result = func(*args, **kwargs)
            cache[key] = {"timestamp": now.isoformat(), "result": result}
            save_cache()  # Save cache immediately after update
            return result

        return wrapper

    return decorator


# ⚡ **Async API Call Optimization**
async def async_openai_request(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        start_time = datetime.utcnow()
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, timeout=10) as response:
                response_data = await response.json()
        
        end_time = datetime.utcnow()
        logging.info(f"OpenAI request completed in {(end_time - start_time).total_seconds()} seconds.")
        return response_data

    except asyncio.TimeoutError:
        logging.error("OpenAI request timed out.")
        return {"error": "Request timed out"}
    except Exception as e:
        logging.error(f"OpenAI request failed: {str(e)}")
        return {"error": "Request failed"}


# 🚀 **Batch Processing API Calls**
async def process_batch_requests():
    while True:
        if BATCH_REQUESTS:
            for key, prompts in list(BATCH_REQUESTS.items()):
                if len(prompts) >= BATCH_SIZE:
                    logging.info(f"Processing batch of {len(prompts)} requests.")
                    batch_response = await asyncio.gather(
                        *[async_openai_request(prompt) for prompt in prompts]
                    )
                    for i, response in enumerate(batch_response):
                        BATCH_REQUESTS[key][i] = response
                    del BATCH_REQUESTS[key]

        await asyncio.sleep(BATCH_TIME_LIMIT)


# 🔍 **Fine-Tuning Models (Placeholder)**
def fine_tune_model():
    """Future placeholder for fine-tuning AI models based on performance metrics."""
    logging.info("Fine-tuning models is not yet implemented.")


# 🛠 **Optimization Event Listener (Runs in Background)**
def optimize_event_handler():
    logging.info("Optimization event listener started.")

    def run_event_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_batch_requests())

    # Run the event loop in a background thread
    threading.Thread(target=run_event_loop, daemon=True).start()


# 🔥 **Auto-Run When Imported**
load_cache()
optimize_event_handler()  # Now runs in the background instead of blocking the main thread
