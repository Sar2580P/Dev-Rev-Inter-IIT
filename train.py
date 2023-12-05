import pandas as pd
from agent_executor.agent_executer import agent_executor
from agent_executor.memory import *
from langchain.docstore.document import Document

data  = pd.read_csv('data/DevRev - Data - Simple.csv')
agent_executor.train()

for i in range(len(data)):
  query, ground_json = data.iloc[i , 0] , data.iloc[i , 1]
  agent_executor.get_tool_lists(ground_json)
  x = agent_executor(inputs={"input": query})
  correct_trajectory , wrong_checkpoints = agent_executor.correct_trajectory , agent_executor.wrong_checkpoints

  for key, value in wrong_checkpoints.items():
    wrong_tool , wrong_reasoning = value['tool'] , value['reasoning']
    correct_tool , correct_reasoning  , correct_tool_input = correct_trajectory[key]['tool'] , \
                                                              correct_trajectory[key]['reasoning'] , correct_trajectory[key]['tool_input']
    
    trajectory_before_wrong_checkpoint = correct_trajectory[:key]
    
    experience = build_experience(trajectory_before_wrong_checkpoint, correct_tool , correct_reasoning, 
                                  wrong_tool ,wrong_reasoning,  query)
    
    metadata = {
      'correct_tool': correct_tool ,
      'correct_tool_input': correct_tool_input ,
      'correct_reasoning': correct_reasoning ,

    }
    doc = Document(page_content=experience , metadata=metadata)

    mistake_memory.stage(doc)
  mistake_memory.push()




