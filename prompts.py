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
Below you are provided with the current user query :
CURRENT_USER_QUERY : {input}

Below you are provided with one of the past mistakes made by another AI agent on some other user query :
SOME_PAST_QUERY : {past_query}
CORRESPONDING_PAST_MISTAKE : {past_mistake}

Check diligently if the current user query is similar to the past query, in terms of the vulnerability of the AI agent to make the same mistake.
If there are some chances of making the same or similar mistake on the current user query, return 1 else return 0.
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
The agent attempts to select the next tool, which turns out to be wrong choice, in the trajectory based on the user query.
Below I have mentioned the correct tool that should have been used instead of the wrong tool.
    Correct Tool : {correct_tool}
    Correct Tool Description : {correct_tool_description}

Below I provide the wrong tool that was selected by the agent and its description.
    Wrong Tool : {wrong_tool}
    Wrong Tool Description : {wrong_tool_description}

Based on the above information :
  1-) Reason why the wrong tool should not be selected by the agent based on:
    a-) contrast between tool capabilities (based on wrong tool description) and user query,
  2-) Reason why agent failed to pick the correct tool based on:
    a-) similarity between tool capability (description of correct tool) and the user query, 
    b-) reason out how the agent failed to pick the correct tool based on the trajectory of right tools used till now 

Be specific don't use general statements.
Put everything as a paragraph in the experience text.

Again repeating, you need to generate an experience for the agent, which will help it to learn from its mistakes.
The experience text should not exceed 30 words and not less than 7 words, don't add too many stop words
'''

CORRECT_TRAJECTORY_TILL_NOW = """
tool_name : {tool_name}
tool_input: {tool_input}
tool_reasoning : {log}\n
"""

#____________________________________________________________________________________________________________


TOOLS_PROMPT_EXAMPLES = '''
You are good at extracting values of certain arguments from a user query in natural language.
Below is the signature of arguments with keys as argument names and 
values as  datatypes in which extracted values should be returned :
{function_signature}

Before moving forward , you need to know the description of each argument :
Specific arguments take only certain values , so you need to know the description of each argument.
{arg_description}

FORMAT INSTRUCTION -->
- You need to return the dictionary of arguments as keys and extracted values as values.
- Ensure that argument values are in double quotes.
- Check that the extracted arguments are in correct datatypes before returning.

Don't mention those arguments in final query whose values are not present in user query.
You have to extract the following arguments from the user query :
{user_query}

Before returning the dictionary of arguments, ensure that all keys and values are in double quotes.
Simply return the dictionary of arguments with keys as argument names and values as extracted values, with no backticks.
Nothing else should be returned.
'''

#____________________________________________________________________________________________________________

TOOL_RELEVENCY_TEMPLATE = '''
You are good at deciding whether a tool is relevant to a user query or not.
Below you are provided with the following information:

Query --> 
{query}

Tool_name --> 
{tool_name}

Tool_description -->
{tool_description}

FORMAT INSTRUCTION --> 
  1) Don't return a dictionary. Only return 1 or 0.
  2) Return 1 if the tool is relevant to the user query, else return 0.
'''
#____________________________________________________________________________________________________________