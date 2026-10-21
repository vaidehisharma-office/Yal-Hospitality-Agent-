from dotenv import load_dotenv
import os

load_dotenv()

MODEL = "google/gemma-4-12B-it"

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL")
VLLM_API_KEY = os.getenv("VLLM_API_KEY")

TEMPERATURE = 0.2
MAX_TOKENS = 200
TIMEOUT_S = 60

CONFIDENCE_THRESHOLD = 0.6

PROMPT_VERSION = "v1"