PAST_MISTAKES ='''

Before proceeding further, below I have mentioned common mistakes made by you while using the tools.
Please go through them carefully and try to avoid them in future.

{mistakes}

'''
SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}

"""


# ____________________________________________________________________________________________________________

MISTAKE_SELECTION =  '''
Below you are provided with the user query :
{input}

Below you are provided with one of the mistakes made by another AI agent on some other user query :
{mistake}

Now, the AI agent wants to know whether the above mistake is relevant to the user query or not, i.e, 
it should be looked into or not while providing the answer to the user query.

Return 1 if the mistake is relevant to the user query, else return 0.
'''

# ____________________________________________________________________________________________________________

TOOL_INPUT_PROMPT = '''
You are expected to create a sub-task from the given user query and the intermediate steps taken till now.

The user query is as follows:
  User_Query : {query}

The intermediate steps taken till now to solve the above query are as follows:
{intermediate_steps}

Below is the correct tool that needs to be used next in the intermediate steps:
  Correct_Tool : {correct_tool}

The short description of the correct tool, to help you reason out, is as follows:
{correct_tool_description}

While creating the sub-task for above tool, adhere to tool description. 
Don't query tool for tasks which are not mentioned in tool description.

Just return a dictionary with the following keys ,with no backticks: 
  "tool_input" : The sub-task in natural language based on user query, intermediate steps and tool description 
  "reason" : Reason why above tool should be chosen based on intermediate steps and tool description, at max 30 words and atleast 15 words

Don't forget to use the format instructions while returning the dictionary. 
'''

# ____________________________________________________________________________________________________________
PREFIX_MISTAKE_MEMORY = '''
You are good at reasoning on mistakes that has been made by another AI agent while deciding the next tool to be used for the given query.

Below is the user query:
    Query : {query}

Below is the trajectory of right tools used till now and their tool input as well as the reasoning behind using them.
'''

SUFFIX_MISTAKE_MEMORY = '''

The agent attempts to select the next tool, which turns out to be wrong choice, in the trajectory based on the user query:
    Wrong Tool : {wrong_tool}
    Wrong Reasoning : {wrong_reasoning}

The agent was expected to select the following tool inplace of above tool with following reasoning:
    Correct Tool : {correct_tool}
    Correct Reasoning : {correct_reasoning}

Based on the above information , you are expected to highlight on the information present in user query which was missed by agent
Again repeating, you need to generate an experience for the agent, which will help it to learn from its mistakes.

The experience text should not exceed 30 words.
'''

CORRECT_TRAJECTORY_TILL_NOW = """
tool_name : {tool_name}
tool_input: {tool_input}
tool_reasoning : {log}\n
"""

#____________________________________________________________________________________________________________


TOOLS_PROMPT_EXAMPLES = '''
You are good at extracting values of certain arguments from a user query in natural language.

Below is the user query which you are expected to extract the values of arguments from:
{user_query}

Below is the signature of arguments with keys as argument names and 
values as  datatypes in which extracted values should be returned :
{function_signature}

Below is the description of arguments with keys as argument names, to help you find the values of arguments :
{arg_description}

Don't fill the values of arguments which are not present in the user query. 
Stick to information mentioned in user query.

Just return the dictionary of arguments as keys and their extracted values as values, with no backticks.
'''

#____________________________________________________________________________________________________________

TOOL_RELEVENCY_TEMPLATE = '''
You are good at deciding whether a tool is relevant to a user query or not.
Below you are provided with the following information:

Query --> 
{query}

FORMAT INSTRUCTION --> 
  1) Don't return a dictionary. Only return 1 or 0.
  2) Return 1 if the tool is relevant to the user query, else return 0.

Tool_name --> 
{tool_name}

Tool_description -->
{tool_description}

 
'''
#____________________________________________________________________________________________________________