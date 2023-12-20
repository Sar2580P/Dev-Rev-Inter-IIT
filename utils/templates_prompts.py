from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from utils.parsers import *


PAST_MISTAKES ='''

Before proceeding further, below I have mentioned common mistakes made by you while using the tools.

{mistakes}

!! PLEASE GO THROUGH THEM CAREFULLY AND AVOID MAKING SIMILAR MISTAKES.

'''
PREFIX = """
Below are the tools in your tool-kit along with their description to help you decide on tool choice.
"""

#____________________________________________________________________________________________________________
FORMAT_INSTRUCTIONS = """
ALERT !!!
  - The Thought-Action-Observation repeats until we feel that agent has completely answered the user query.
  - Each time this process repeates, you need to write some reason in Thought of choosing a particular tool.

Use the following format:

Question: the input question you must answer

Thought : The reason of picking the tool in process of answering user query.

Action : the Tool to take , should be one of [{tool_names}]

Action Input: the input to the tool

Observation : the result of the Tool
... (this Thought/Action/Action Input/Observation can repeat N times)


Thought : I now know the final answer
Final Answer: 

  
"""

# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================

# MISTAKE_SELECTION =  '''

# Below you are provided with one of the past mistakes made by another AI agent on some other user query :
# {mistake}

# Below you are provided with the current user query :
# CURRENT_USER_QUERY : {input}

# Check diligently if the current user query is similar to the past query, in terms of the vulnerability of the AI agent to make the same mistake.
# If there are some chances of making the same or similar mistake on the current user query, return 1 else return 0.

# ANSWER : 
# '''

MISTAKE_SELECTION =  '''
Below you are provided with the current user query :

- Do not to do the same mistake again and use the following context to choose a tool!!

CURRENT_USER_QUERY : {input}
Below you are provided with one of the past mistakes made on other user query :
{mistake}

- ANSWER : 
'''

# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================

TOOL_INPUT_PROMPT = '''
The user query is as follows:
  User_Query : {query}

The intermediate steps taken till now to solve the above query are as follows:
{intermediate_steps}

Below is the next tool that needs to be used as next tool in intermediate steps: {tool_name}

The short description of the tool, to help you reason out, is as follows:
{tool_description}

You are expected to create a sub-task for the above tool from the given user_query, tool_description and the intermediate steps taken till now.

While creating the sub-task for above tool, adhere to tool description. 
Don't query tool for tasks which are not mentioned in tool description.

FORMAT INSTRUCTIONS :
{format_instructions}
'''
# ===================================================================================================================================================================================================


EXAMPLES = [
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


EXAMPLE_FORMATTER_TEMPLATE = """
query: {query}\n
intermediate steps : {intermediate_steps}\n
tool_name: {tool_name}
tool_description: {tool_description}

tool_input: {tool_input}\n\n
"""

EXAMPLE_PROMPT = PromptTemplate(
    input_variables=["query", "intermediate_steps" , "tool_name" , "tool_description", "tool_input"],
    template=EXAMPLE_FORMATTER_TEMPLATE,
)

# ===================================================================================================================================================================================================

sub_task_prompt = FewShotPromptTemplate( 
    examples=EXAMPLES,

    # prompt template used to format each individual example
    example_prompt=EXAMPLE_PROMPT,

    # prompt template string to put before the examples, assigning roles and rules.
    prefix="Here are some few shots of how to create sub-task for a given tool based query, intermediate_steps and tool_description:\n",
    
    # prompt template string to put after the examples.
    suffix=TOOL_INPUT_PROMPT,
    
    # input variable to use in the suffix template
    input_variables=["query" , "intermediate_steps" , "tool_name" , "tool_description"],
    example_separator="\n", 
    partial_variables= {'format_instructions' : sub_task_parser.get_format_instructions()}
)


# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================

MISSED_TOOL_TEMPLATE = '''

There is an AI agent which is picking up tools under ReAct framework to solve user queries.
It misses picking up correct tool, being unable to reason out its usage for the given query.

You are also provided with the sequence of thoughts and actions taken by the agent till now to solve the query.

AGENT_SCRATCHPAD :
{agent_scratchpad}

CORRECT_TOOL_NAME : {correct_tool_name}
TOOL_DESCRIPTION : {tool_description}

USER_QUERY : {query}

- You need to provide an eye-catchy insight of why that tool should not be missed for the given query based on the user query and tool description. 
- You insight will help the agent to learn from its mistakes. Don't be super-specific to user query, keep the tool description in consideration. 
- Keep your insight within 20 words and at least 9 words. Present answer in a paragraph.

ANSWER : 
'''

missed_tool_prompt = PromptTemplate(template=MISSED_TOOL_TEMPLATE, input_variables=['agent_scratchpad','query' ,'correct_tool_name' , 'tool_description'])

# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================

TOOLS_PROMPT_EXAMPLES = '''

Your task is to extract the argument value from user query based on argument description and argument type.

Below you are provided the data-type of how the argument expects the value to be :
{arg_dtype}

Below is the meaning of argument to help you assist in extracting the argument value from the query:
{arg_description}

The above mentioned arguments have their values present in the query. You need to extract the argument value from the query.
Don't pollute the information, stick to information provided in the user query.

ALERT !!!
- If the Query contains specific keywords like $$PREV[i], where i is the index of the output you want to use, then it is a symbolic representation of the output and is NOT THE ACTUAL OUTPUT
- use $$PREV[i] as whole and don't pass invalid representation like "$$PREV" OR "$$PREV[]" or i

You are provided with a user query below :
QUERY : {user_query}

FORMAT INSTRUCTIONS --->
  - Don't return anything else other than the argument value.
  - Ensure that the argument value is in correct data type before returning.
  - If the argument value is not explicitly present in the query, then return "NONE".

ANSWER :
'''

#____________________________________________________________________________________________________________

ARG_FILTER_PROMPT = '''
You need to work as a filter to filter out the arguments which are not relevant to the user query.

Below is the argument name:
ARGUMENT_NAME : {arg_name}

Below is the argument description:
ARGUMENT_DESCRIPTION : {arg_description}

Below is the user query:
QUERY : {query}

FORMAT INSTRUCTIONS --->
  - Return 1 if argument name mentioned above can be filled with a value extracted from user query, else return 0.
  - Stick to the information provided in user-query and argument description.
  - DO NOT pollute the information or your decision with any assumptions.
  
  
ANSWER :
'''
#____________________________________________________________________________________________________________
VAR_ARGS_LOGIC_TOOL = '''
You will be provided with the following user query:
{query}

You need to infer the probable arguments and also their data types from the user query.
You need to return the following dictionary of arguments as keys and their data types as values:

Below I provide a sample dictionary of arguments as keys and their data types as values:
"arg1":"str"
"arg2":"int"
"arg3" : "List"

- Use your knowledge if argument types of certain arguments can't be inferred from the user query.
- Don't pollute the dictionary with unnecessary arguments. Stick to information provided in the user query.
- Ensure that the arguments are in correct data types before returning the dictionary.
- Simply return the dictionary of arguments with keys as argument names and values as their data types, with no backticks.
'''

#____________________________________________________________________________________________________________

LOGICAL_TEMPLATE = '''

You will be provided with the following user query:
{query}

You need to return a code block executing the above user query in the given programming language.
Create a function with the name "sum" with proper variables and call that function with the above provided arguments.


Below I provide an example code block in python so that you know the desired output format:
```
def sum(arg1 , arg2 , arg3):
    return arg1+arg2+arg3
    
sum($$PREV[0] , $$PREV[6] , 123)
```
you may devise any function of your own using a combination of sum, variables, loops, if-else statements etc.

- Make sure that the code is in correct syntax before returning.
- Don't return anything else other than the code block. 
- Simply return the code block, nothing else to be returned

'''
# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================
CRITIQUE_TEMPLATE = '''

Below you are provided the tools available in toolkit and their description :
{tools}

FORMAT INSTRUCTIONS :
{format_instructions}

Hint :
  - Philosophical , emotional (joy, sadness, life related) questions cannot be answered with available tools

QUERY : {query}
'''

critique_prompt = PromptTemplate(template=CRITIQUE_TEMPLATE, input_variables=['query' ,'tools'], 
                                                      partial_variables={'format_instructions' : critique_parser.get_format_instructions()})

# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================
# ===================================================================================================================================================================================================

# You are also provided the dataypes of arguments present in the user query:
# {function_signature}


# ["red" , ""$$PREV[0]"]

'''

QUERY_EXAMPLE : "What is the use of life?"
ANSWER : 0
REASON : The available tools are not useful to answer the query.

QUERY_EXAMPLE : "List all work items similar to TKT-420 and add the top 2 highest priority items to the current sprint"
ANSWER : 1
REASON : The available tools are useful to answer the query.

QUERY_EXAMPLE : "Search for youtube videos of user id DEVU-67"
ANSWER : 0
REASON : no tool is present to search for youtube videos.

QUERY_EXAMPLE : "Create a excel file of work items in the current sprint"
ANSWER : 0
REASON : no tool is present to create excel file.

ANSWER : 
REASON :
'''