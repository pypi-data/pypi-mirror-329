from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

GPT_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_MODEL_DEFAULT = 'gpt-4o'
gpt_client_default = OpenAI(api_key=GPT_API_KEY)
