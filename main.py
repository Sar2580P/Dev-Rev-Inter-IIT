from flask import Flask, request
from agent_executor.agent_executer import *
from langchain.callbacks import get_openai_callback
import time

app = Flask(__name__)

@app.route('/predict' , methods = ['POST'])
def predict():
  input_data = request.json['input']
  output = predict_function(input_data)
#   if output["output"] == [] and thought==[]:
#      output["thought"] = "Encountered internal error!"

  return {'output': output}

import json 

cot = 0

def predict_function(query):

    agent_executor.eval()
    print('response_schema : ' , agent_executor.return_schema)

    start_time = time.time()
    with get_openai_callback() as cb:
        x = agent_executor(inputs={"input": query})
    end_time = time.time()

    elapsed_time = end_time - start_time

    predict_json = agent_executor.return_schema
    # json.dump(predict_json, open('predict.json', 'w'))
    web_sc={
          'thought':agent_executor.thought_execution_chain[-1].split('\n')[0] + f"\n Total cost: ${round(cb.total_cost,5)} , time-taken: {round(elapsed_time*1000,4)}ms",
          'tool':predict_json
    }
    agent_executor.web_schema.append(web_sc)
    #a =  {'thought': thought_action_observations ,'output': predict_json , }
    a=agent_executor.web_schema
    global cot 
    json.dump(a, open(f"abc{cot}.json", 'w'), indent = 4)
    cot = cot + 1
    return a

# if __name__ == '__main__':
#   app.run()

# predict_function('If $$PREV[0] is greater than $$PREV[1] then return 1 else return 3')
# predict_function('Get all work items similar to TKT-123, summarize them, create issues from that summary, and prioritize them.')
# predict_function('List all high severity tickets coming in from slack from customer abc123 and generate a summary of them.')
# predict_function('How is life going?')
# predict_function('How crocodiles give birth?')
# predict_function('Prioritize all tickets from the support channel "Email"')


# Dataset Queries:

# predict_function('Summarize issues similar to don:core:dvrv-us-1:devo/0:issue/1') 
# predict_function('What is the meaning of life?')
# predict_function('Prioritize my P0 issues and add them to the current sprint')
# predict_function('Summarize high severity tickets from the customer UltimateCustomer')
# predict_function('What are my all issues in the triage stage under part FEAT-123? Summarize them.')
# predict_function('List all high severity tickets coming in from slack from customer Cust123 and generate a summary of them.')
# predict_function('Given a customer meeting transcript T, create action items and add them to my current sprint')
predict_function('Get all work items similar to TKT-123, summarize them, create issues from that summary, and prioritize them')


# predict_function('Prioritize my P0 issues and what is the meaning of life')



