from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field, validator
from backend_llm.utils import llm, small_llm
import ast
from prompts import TOOL_INPUT_PROMPT


# class Auxiliary_Parser(BaseModel):
#   tool_input : str = Field(description="The input for the correct tool")
#   correct_reasoning : str = Field(description="Correct reasoning for using the correct tool ")

#   @validator('tool_input')
#   def tool_input_must_be_present(cls, v):
#     if len(v)<5 or len(v) > 30:
#       raise ValueError('tool_input must be present')
#     return v
  
#   @validator('correct_reasoning')
#   def correct_reasoning_must_be_present(cls, v):
#     if len(v)<5 or len(v) > 20:
#       raise ValueError('Correct reasoning must be present')
#     return v

# auxiliary_parser = PydanticOutputParser(pydantic_object=Auxiliary_Parser)
#_______________________________________________________________________________________________________________________________ 
#  
sub_task_prompt = PromptTemplate(template=TOOL_INPUT_PROMPT , 
                                 input_variables=["query" , "intermediate_steps" , "correct_tool" , "correct_tool_description"] , 
                                #  partial_variables={"format_instructions": auxiliary_parser.get_format_instructions()}
                                 )

sub_task_chain = LLMChain(prompt=sub_task_prompt , llm=llm)

def sub_task(input):
  answer = sub_task_chain.run(input)
  
  if not answer[0]=='{':
    answer = answer[answer.find('{'):]
  print("\033[91m {}\033[00m" .format('sub_task (auxiliary_executor)'))
  print(answer)
  return ast.literal_eval(answer)