from langchain.llms.openai import OpenAI
import yaml
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file
from langchain.callbacks import StdOutCallbackHandler, WandbCallbackHandler
from datetime import datetime
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.google_palm import GooglePalm
import google.generativeai as palm
from chromadb.api.types import Documents, Embeddings

small_llm = GooglePalm(temperature=0, max_output_tokens=500)

models = [m for m in palm.list_models() if 'embedText' in m.supported_generation_methods]
model = models[0]    # models\embedding-gecko-001 ---> input_token_limit=1024,

class Embedding:
  def __init__(self):
    self.embedder = palm

  def embed_documents(self, texts: Documents) -> Embeddings:
    # Embed the documents using any supported method
    return  [self.embedder.generate_embeddings(model=model, text=text)['embedding']
            for text in texts]
  
  def embed_query(self,query):
    return  self.embedder.generate_embeddings(model=model, text=query)['embedding']
            
small_embedding_func = Embedding()
#_________________________________________________________________________________________
# session_group = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
# wandb_callback = WandbCallbackHandler(
#     job_type="inference",
#     project="Inter-IIT",
#     group=f"minimal_{session_group}",
#     name="llm",
#     tags=["test"],
# )
# callbacks = [wandb_callback]
llm = OpenAI(temperature=0 , model="gpt-3.5-turbo-instruct")

embedding_func = OpenAIEmbeddings()

#_________________________________________________________________________________________
def load_config(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config 

# config = load_config('backendPython/config.yaml')
#_________________________________________________________________________________________
import requests

API_URL = "https://api-inference.huggingface.co/models/forestai/fireact_codellama_34b_lora"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Can you please let us know more details about your ",
})
print(output)