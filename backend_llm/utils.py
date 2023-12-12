from langchain.llms.openai import OpenAI
import yaml
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
from langchain.callbacks import StdOutCallbackHandler, WandbCallbackHandler
from datetime import datetime
from langchain.embeddings import OpenAIEmbeddings
from chromadb.api.types import Documents, Embeddings

#_________________________________________________________________________________________

llm = OpenAI(temperature=0.0 ,frequency_penalty = 0.1 ,max_tokens=1000,  model="gpt-3.5-turbo-instruct")

embedding_func = OpenAIEmbeddings()

#_________________________________________________________________________________________
def load_config(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config 

# config = load_config('backendPython/config.yaml')
#_________________________________________________________________________________________
