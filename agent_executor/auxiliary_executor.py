from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field, validator
from backend_llm.utils import llm

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

You are expected to create a tool_input for the correct tool based on the user query and intermediate steps taken by agent till now.
Also return a reasoning for the correct tool based on the user query and intermediate steps taken by agent till now.
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
    if len(v)<5 or len(v) > 40:
      raise ValueError('Correct reasoning must be present')
    return v
#_______________________________________________________________________________________________________________________________  
auxiliary_parser = PydanticOutputParser(pydantic_object=Auxiliary_Parser)
sub_task_prompt = PromptTemplate(template=sub_task_template , 
                                 input_variables=["query" , "intermediate_steps" , "correct_tool" , "correct_tool_description"] , 
                                 partial_variables={"format_instructions": auxiliary_parser.get_format_instructions()}
                                 )

sub_task_chain = LLMChain(prompt=sub_task_prompt , llm=llm)