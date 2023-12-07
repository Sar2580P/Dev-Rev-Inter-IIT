import pandas as pd
from agent_executor.agent_executer import agent_executor
from backend_llm.utils import callbacks , wandb_callback
import time  
simple_data = pd.read_csv('DevRev - Data - Simple.csv')
print('Simple_data :\n' ,simple_data.head(2))
complex_data = pd.read_csv('devrev_complex.csv')
print('Complex_data :\n' ,complex_data.head(2), end = '\n\n\n')

def get_simple_predictions(data):
  df = pd.DataFrame(columns=['Query', 'Original' , 'Predicted', 'Latency'])
  error_set = []
  for i in range(len(data)):
    if i>2:
     break
    query = data.iloc[i, 0]
    true = data.iloc[i,1]
    # try:
    start = time.time()
    agent_executor(query)
    # wandb_callback.flush_tracker(agent_executor, reset=False, finish=True)
    predicted = agent_executor.return_schema
    print('\n\n\n\n' , predicted)
    time_taken = time.time() -start
    df.loc[i] = [query, true, predicted , time_taken]
    # except:
    #   print('skipped')
    #   li = [i ,query]
    #   error_set.append(li)
    #   df.loc[i] = [query, true, 'error' , 'error']
    print(i)
    

  df.to_csv('predictions.csv', index=False)
  return error_set



error_set = get_simple_predictions(simple_data)
print(error_set)