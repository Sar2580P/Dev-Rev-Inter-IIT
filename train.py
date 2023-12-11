import pandas as pd
from agent_executor.agent_executer import agent_executor
from agent_executor.agent_memory import *
from langchain.docstore.document import Document
from icecream import ic
from langchain.callbacks import get_openai_callback

data  = pd.read_excel('data\DEVREV Dataset 2.0.xlsx' , sheet_name='New_C+V').iloc[50:70, :]
agent_executor.train()

ct = 0
for i in range(len(data)):
  print("\033[1;32m {}\033[00m" .format('QUERY COUNT : {i}'.format(i=i)))
  query, ground_json = data.iloc[i , 0] , data.iloc[i , 1]
  print("\033[1;32m {}\033[00m" .format('QUERY : ') , "\033[93m {}\033[00m" .format(query))
  print("\033[1;32m {}\033[00m" .format('Ground JSON :') , "\033[93m {}\033[00m" .format(ground_json))

  agent_executor.get_tool_lists(ground_json)
  
  with get_openai_callback() as cb:
    x = agent_executor(inputs={"input": query})
    correct_trajectory , checkpoints = agent_executor.correct_trajectory , agent_executor.checkpoints

    for tool_index, value in checkpoints.items():
      x = {
        "query":query, 
        "correct_tool" :value['correct_tool'] , 
        "wrong_tool" : value['wrong_tool'] ,
        "wrong_tool_description" : value['wrong_tool_description'] ,
        "correct_tool_description" :value['correct_tool_description'] , 
        "correct_trajectory" : correct_trajectory[:tool_index]
      }

      human_eval = 'n'
      # human_eval = input("Do you want to correct the reasoning? (y/n) :")
      if human_eval.lower() == 'n':
        experience = build_experience(x)
      else :
        experience = input("This has been the mistake summary : \n\t{x}. \nPlease write the correct reasoning :".format(x=x))
      
      learning  = '- PAST_QUERY : {a}\n- PAST_MISTAKE : {b}\n'.format(a = x['query'] , b = experience)
      metadata = {
        # 'query': x['query'],
        'correct_tool': x['correct_tool'],
      }
      print('metadata : ' , metadata)
      print('learning : ' , learning)
      doc = Document(page_content=learning , metadata=metadata)
      mistake_memory.stage(doc)
    
  user_decision = input('Do you want to save the experience? (y/n) : ')  
  if user_decision.lower() == 'y':
    ct+= mistake_memory.queue.qsize()
    mistake_memory.push()
  else:
    mistake_memory.clear()
    print("\033[91m {}\033[00m" .format('skipping experience saving...'))
  print("\033[91m {}\033[00m" .format('---------------- QUERY_COST : $ {cost}---------------- MISTAKES LEARNED : {ct}-------------------- QUERY TOKENS : {tokens}-----------------'.format(cost = round(cb.total_cost, 5) , 
                                                                                                                                                                                            ct = ct, tokens = cb.total_tokens)))