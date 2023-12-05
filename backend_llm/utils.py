from langchain.llms.google_palm import GooglePalm
from langchain.llms.openai import OpenAI
import yaml
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
from langchain.callbacks import StdOutCallbackHandler, WandbCallbackHandler
from datetime import datetime
from langchain.embeddings import OpenAIEmbeddings


# os.env["OPENAI_API_KEY"] = "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"

# llm = GooglePalm(temperature=0)

# session_group = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
# wandb_callback = WandbCallbackHandler(
#     job_type="inference",
#     project="Inter-IIT",
#     group=f"minimal_{session_group}",
#     name="llm",
#     tags=["test"],
# )
# callbacks = [wandb_callback]
llm = OpenAI(temperature=0 , model="text-davinci-003")

embedding_func = OpenAIEmbeddings()

#_________________________________________________________________________________________
def load_config(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config 

# config = load_config('backendPython/config.yaml')
#_________________________________________________________________________________________
