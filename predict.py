import pandas as pd
from agent_executor.agent_executer import agent_executor
from agent_executor.agent_memory import *
from langchain.docstore.document import Document
from langchain.callbacks import get_openai_callback
import time 

data  = pd.read_excel('data\DEVREV Dataset 2.0.xlsx' , sheet_name='Direct_C+V').iloc[49:51, :]
prediction_df = pd.DataFrame(columns=['query' , 'groundJson' , 'predicted_json' , 'latency (in seconds)' , 'queryCost' , 'queryTokens'])
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
    predict_json = agent_executor.return_schema
    latency = time.time() - start 
    query_cost = cb.total_cost
    query_tokens = cb.total_tokens
    prediction_df.loc[i] = [query , ground_json , predict_json , round(latency,2) , round(query_cost,5) , query_tokens]
  print("\033[91m {}\033[00m".format('---------------- QUERY_COST : $ {cost}---------------- MISTAKES LEARNED : {ct}-------------------- QUERY TOKENS : {tokens}-----------------'.format(cost = round(cb.total_cost, 5) , 
                                                                                                                                                                                            ct = ct, tokens = cb.total_tokens)))
prediction_df.to_csv('data/Direct_C+V_prediction.csv', index=False)

