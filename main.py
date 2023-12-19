from flask import Flask, request
from agent_executor.agent_executer import *

app = Flask(__name__)

@app.route('/predict' , methods = ['POST'])
def predict():
  input_data = request.json['input']
  output = predict_function(input_data)
  return {'output': output}

import json 

def predict_function(query):
  agent_executor.eval()
  print('response_schema : ' , agent_executor.return_schema)
  x = agent_executor(inputs={"input": query})
  predict_json = agent_executor.return_schema
  # json.dump(predict_json, open('predict.json', 'w'))
  thought_action_observations = agent_executor.thought_execution_chain

  a =  {'thought': thought_action_observations ,'output': predict_json , }
  json.dump(a, open('abc.json', 'w'), indent = 4)
  return a

# if __name__ == '__main__':
#   app.run()

# predict_function('If $$PREV[0] is greater than $$PREV[1] then return 1 else return 3')
# predict_function('Get all work items similar to TKT-123, summarize them, create issues from that summary, and prioritize them.')
# predict_function('Prioritize all tickets from the support channel "Email"')
predict_function('List all high severity tickets coming in from slack from customer Cust123  and generate a summary of them.')