from langchain.llms.google_palm import GooglePalm
from langchain.llms.openai import OpenAI
import yaml
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
import os 
# os.env["OPENAI_API_KEY"] = "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"

# llm = GooglePalm(temperature=0)
llm = OpenAI(temperature=0 )
#_________________________________________________________________________________________
def load_config(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config 

# config = load_config('backendPython/config.yaml')
#_________________________________________________________________________________________
