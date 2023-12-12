from flask import Flask, request
from agent_executor.agent_executer import agent_executor

# app = Flask(__name__)

# @app.route('/predict' , methods = ['POST'])
# def predict():
#   input_data = request.json['input']
#   output = predict_function(input_data)
#   return {'output': output}

import json 

def predict_function(query):
  agent_executor.eval()
  x = agent_executor(inputs={"input": query})
  predict_json = agent_executor.return_schema
  # json.dump(predict_json, open('predict.json', 'w'))
  thought_action_observations = agent_executor.execution_chain

  a =  {'thought': thought_action_observations ,'output': predict_json , }
  json.dump(a, open('abc.json', 'w'), indent = 4)
  return a

# if __name__ == '__main__':
  # app.run()

# predict_function('If $$PREV[0] is greater than $$PREV[1] then return 1 else return 3')
predict_function('what are my p0 issues.')
# predict_function('Find the first work item similar to TKT-500 and assign it to the current sprint')