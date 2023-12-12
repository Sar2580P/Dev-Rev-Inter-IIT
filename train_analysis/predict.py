import pandas as pd
import sys, os
sys.path.append(os.getcwd())
from agent_executor.agent_executer import agent_executor
from agent_executor.agent_memory import *
from langchain.docstore.document import Document
from langchain.callbacks import get_openai_callback
import time 

data  = pd.read_csv('data\DEVREV Dataset 2.0 - Single Tool.csv').iloc[50: , ]

if not os.path.exists('prediction_data/DEVREV Dataset 2.0 - Single Tool.csv'):
  prediction_df = pd.DataFrame(columns=['query' , 'groundJson' , 'predicted_json' , 'latency (in seconds)' , 'queryCost' , 'queryTokens'])
  prediction_df.to_csv('prediction_data/DEVREV Dataset 2.0 - Single Tool.csv', index=False)

prediction_df = pd.read_csv('prediction_data/DEVREV Dataset 2.0 - Single Tool.csv')
agent_executor.eval()

ct = 0
for i in range(len(data)):
  print("\033[1;32m {}\033[00m" .format('QUERY COUNT : {i}'.format(i=i)))
  query, ground_json = data.iloc[i , 0] , data.iloc[i , 1]
  print("\033[1;32m {}\033[00m" .format('QUERY : ') , "\033[93m {}\033[00m" .format(query))
  print("\033[1;32m {}\033[00m" .format('Ground JSON :') , "\033[93m {}\033[00m" .format(ground_json))

  
  with get_openai_callback() as cb:
    start = time.time()
    x = agent_executor(inputs={"input": query})
    try: 
      predict_json = agent_executor.return_schema
      latency = time.time() - start 
      query_cost = cb.total_cost
      query_tokens = cb.total_tokens
      prediction_df.loc[len(prediction_df)] = [query , ground_json , predict_json , round(latency,2) , round(query_cost,5) , query_tokens]
    except:
      print("Skipping query ....")
  print("\033[91m {}\033[00m".format('---------------- QUERY_COST : $ {cost}---------------- QUERY TOKENS : {tokens}-----------------'.format(cost = round(cb.total_cost, 5) , 
                                                                                                                                             tokens = cb.total_tokens)))
  prediction_df.to_csv('prediction_data/DEVREV Dataset 2.0 - Single Tool.csv', index=False)

