from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field, validator
from backend_llm.utils import llm
import ast
from prompts import TOOL_INPUT_PROMPT


examples = [
    {
      'query': "Find all high priority issues related to part 'FEAT-123' created by user 'DEVU-123', prioritize them, and add them to the current sprint" , 
      'intermediate_steps': '''[
                              {{"tool_name": "works_list", "arguments": [{{"argument_name": "issue.priority", "argument_value": "high"}}, 
                                            {{"argument_name": "applies_to_part", "argument_value": "FEAT-123"}}, 
                                            {{"argument_name": "created_by", "argument_value": "DEVU-123"}}]}},
                              {{"tool_name": "prioritize_objects", "arguments": [{{"argument_name": "objects", "argument_value": "$$PREV[0]"}}]}},
                              {{"tool_name": "get_sprint_id", "arguments": []}},
                            ]''',

    'tool_name': 'add_work_items_to_sprint',
    'tool_description': "Adds the given work items to the sprint. This tool needs to know the list of work_id and the sprint_id to which the work items should be added.",
    'tool_input': "Add work items $$PREV[1] to sprint_id $$PREV[2]"
  
  }
]


example_formatter_template = """
query: {query}\n
intermediate steps : {intermediate_steps}\n
tool_name: {tool_name}
tool_description: {tool_description}

tool_input: {tool_input}\n\n
"""
example_prompt = PromptTemplate(
    input_variables=["query", "intermediate_steps" , "tool_name" , "tool_description", "tool_input"],
    template=example_formatter_template,
)

sub_task_prompt = FewShotPromptTemplate( 
    examples=examples,

    # prompt template used to format each individual example
    example_prompt=example_prompt,

    # prompt template string to put before the examples, assigning roles and rules.
    prefix="Here are some few shots of how to create sub-task for a given tool based query, intermediate_steps and tool_description:\n",
    
    # prompt template string to put after the examples.
    suffix=TOOL_INPUT_PROMPT,
    
    # input variable to use in the suffix template
    input_variables=["query" , "intermediate_steps" , "tool_name" , "tool_description"],
    example_separator="\n", 
)

#_______________________________________________________________________________________________________________________________ 
  
# sub_task_prompt = PromptTemplate(template=TOOL_INPUT_PROMPT , 
#                                  input_variables=["query" , "intermediate_steps" , "tool_name" , "tool_description"] , 
#                                  partial_variables={"format_instructions": auxiliary_parser.get_format_instructions()}
#                                  )
sub_task_chain = LLMChain(prompt=sub_task_prompt , llm=llm)

def sub_task(input):
  x = {
      "query": input['query'],
      "intermediate_steps": input['intermediate_steps'],
      "tool_name": input['correct_tool'],
      "tool_description": input['correct_tool_description'],
  
  }
  answer = sub_task_chain.run(x)
  
  if not answer[0]=='{':
    answer = answer[answer.find('{'):]
  print("\033[91m {}\033[00m" .format('sub_task (auxiliary_executor)'))
  print(answer)
  return ast.literal_eval(answer)