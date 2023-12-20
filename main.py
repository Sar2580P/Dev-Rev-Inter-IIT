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
predict_function('Calculate the difference in count between P1 and P2 issues')


# predict_function('Prioritize my P0 issues and what is the meaning of life')


def keep_digits(string):
    return re.sub(r'[^\d]+', '', string)

def parser(arguments_dict,function_signatures):

    for key,values in arguments_dict.copy().items():
        if key not in function_signatures.keys():
            continue
        if values==[]:
            del arguments_dict[key]
            continue
        if values==False and key=='ticket_needs_response':
            del arguments_dict[key]
            continue
        if type(values)==list:
            for i,value in enumerate(values):

                if type(value)==str:
                    if "PREV" in value:
                        arguments_dict[key][i]=f"$$PREV[{keep_digits(value)}]"

                    if function_signatures[key]==str:
                        arguments_dict[key]=value
                    else:
                        arguments_dict[key][i].replace(arguments_dict[key][i],value)
        else:
            if type(values)==str:
                    if "PREV" in values:
                        arguments_dict[key]=f"$$PREV[{keep_digits(values)}]"

                    if function_signatures[key]==List[str]:
                        if type(values)!=list:
                            arguments_dict[key]=[values]

    return arguments_dict
