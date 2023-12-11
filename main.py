from flask import Flask, request
from agent_executor.agent_executer import agent_executor

app = Flask(__name__)

@app.route('/predict' , methods = ['POST'])
def predict():
  input_data = request.json['input']
  output = predict_function(input_data)
  return {'output': output}

def predict_function(query):
  agent_executor.eval()
  x = agent_executor(inputs={"input": query})
  predict_json = agent_executor.return_schema
  thought_action_observations = agent_executor.thought_action_observations

  return {'thought': thought_action_observations ,'output': predict_json , }

if __name__ == '__main__':
  app.run()

# predict_function('If $$PREV[0] is greater than $$PREV[1] then return 1 else return 3')