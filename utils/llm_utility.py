from langchain.llms.openai import OpenAI
import yaml
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
from langchain.callbacks import StdOutCallbackHandler, WandbCallbackHandler
from datetime import datetime
from langchain.embeddings import OpenAIEmbeddings
from chromadb.api.types import Documents, Embeddings


# session_group = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
# wandb_callback = WandbCallbackHandler(
#     job_type="inference",
#     project="langchain_callback_demo",
#     group=f"minimal_{session_group}",
#     name="llm",
#     tags=["test"],
# )
# callbacks = [StdOutCallbackHandler(), wandb_callback]
#_________________________________________________________________________________________

llm = OpenAI(temperature=0.40 ,frequency_penalty = 0.1 ,n = 5 ,max_tokens=1000,  model="gpt-3.5-turbo-instruct")
# llm = OpenAI(temperature=0.00 ,frequency_penalty = 0.1 ,n = 5 ,max_tokens=1000,  model="gpt-3.5-turbo-instruct")

embedding_func = OpenAIEmbeddings()

#_________________________________________________________________________________________
def load_config(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config 

# config = load_config('backendPython/config.yaml')
#_________________________________________________________________________________________