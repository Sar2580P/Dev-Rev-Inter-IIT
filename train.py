import pandas as pd
from agent_executor.agent_executer import agent_executor
from agent_executor.memory import *
from langchain.docstore.document import Document

data  = pd.read_csv('data/DevRev - Data - Simple.csv').iloc[:2 , :]
agent_executor.train()

print("\033[91m {}\033[00m" .format('train.py'))

for i in range(len(data)):
  
  query, ground_json = data.iloc[i , 0] , data.iloc[i , 1]
  print('query : ' , query)
  print('ground_json : ' , ground_json) 
  agent_executor.get_tool_lists(ground_json)
  x = agent_executor(inputs={"input": query})
  correct_trajectory , wrong_checkpoints = agent_executor.correct_trajectory , agent_executor.wrong_checkpoints

  for tool_index, value in wrong_checkpoints.items():
    x = {
      "query":query, 
      "wrong_tool" :value['tool'] , 
      "wrong_reasoning" :value['reasoning'] , 
      "correct_tool" :correct_trajectory[tool_index]['tool_name'] , 
      "correct_reasoning": correct_trajectory[tool_index]['log'] ,
      "correct_trajectory" : correct_trajectory[:tool_index]
    }
    
    experience = build_experience(x)
    
    metadata = {
      'correct_tool': x['correct_tool'] ,
      'correct_tool_input': correct_trajectory[tool_index]['tool_input'] ,
      'correct_reasoning': correct_trajectory[tool_index]['log'] ,

    }
    doc = Document(page_content=experience , metadata=metadata)
    print('wrong_tool : ' , value['tool'])
    print('experience : ' , experience)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    mistake_memory.stage(doc)


  print("\033[91m {}\033[00m" .format('-----------------------------------------------------------------------------------'))
  
  mistake_memory.push()




