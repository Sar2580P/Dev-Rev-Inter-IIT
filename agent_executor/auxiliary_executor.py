from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field, validator
from backend_llm.utils import llm
import ast
#_______________________________________________________________________________________________________________________________
sub_task_template = '''
You are expected to create a sub-task from the given user query and the intermediate steps that the agent has taken till now.

The user query is as follows:
  User_Query : {query}

The intermediate steps taken by the agent till now are as follows:
{intermediate_steps}

Below is the correct tool that needs to be used next in the intermediate steps:
  Correct_Tool : {correct_tool}

The short description of the correct tool, to help you reason out,  is as follows:
{correct_tool_description}

Just return a dictionary with the following keys ,with no backticks: 
  "tool_input" : The sub-task in natural language based on user query, intermediate steps and tool description 
  "reason" : Reason why above tool should be chosen based on intermediate steps and tool description, at max 30 words and atleast 15 words

Don't forget to use the format instructions while returning the dictionary. 
'''
#_______________________________________________________________________________________________________________________________
class Auxiliary_Parser(BaseModel):
  tool_input : str = Field(description="The input for the correct tool")
  correct_reasoning : str = Field(description="Correct reasoning for using the correct tool ")

  @validator('tool_input')
  def tool_input_must_be_present(cls, v):
    if len(v)<5 or len(v) > 30:
      raise ValueError('tool_input must be present')
    return v
  
  @validator('correct_reasoning')
  def correct_reasoning_must_be_present(cls, v):
    if len(v)<5 or len(v) > 20:
      raise ValueError('Correct reasoning must be present')
    return v
#_______________________________________________________________________________________________________________________________  
auxiliary_parser = PydanticOutputParser(pydantic_object=Auxiliary_Parser)
sub_task_prompt = PromptTemplate(template=sub_task_template , 
                                 input_variables=["query" , "intermediate_steps" , "correct_tool" , "correct_tool_description"] , 
                                #  partial_variables={"format_instructions": auxiliary_parser.get_format_instructions()}
                                 )

sub_task_chain = LLMChain(prompt=sub_task_prompt , llm=llm)

def sub_task(input):
  answer = sub_task_chain.run(input)
  
  if not answer[0]=='{':
    answer = answer[answer.find('{'):]
  print("\033[91m {}\033[00m" .format('sub_task (auxiliary_executor)'))
  return ast.literal_eval(answer)