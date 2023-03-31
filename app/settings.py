import os

# Determine the root directory of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_DIR = "configs/"
PROMPT_DIR = "prompts/"

CONFIG_PATH = os.path.join(ROOT_DIR, CONFIG_DIR)
PROMPT_PATH = os.path.join(ROOT_DIR, PROMPT_DIR)

PROTOCOL = "GPT-3.5"

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
