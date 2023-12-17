PAST_MISTAKES ='''

Before proceeding further, below I have mentioned common mistakes made by you while using the tools.

{mistakes}

!! PLEASE GO THROUGH THEM CAREFULLY AND AVOID MAKING SIMILAR MISTAKES.
'''

SUFFIX = """
ALERT !!!
  - whenever $$PREV[i] is shown as a tool output, it is a symbolic representation of the output and is NOT THE ACTUAL OUTPUT
  - DO NOT PASS INVALID REPRESENTATION LIKE "$$PREV" OR "$$PREV[]"
  - Always use it as $$PREV[i] where i is the index of the output you want to use 
  

Begin!

Question: {input}
Thought:{agent_scratchpad}

"""

#____________________________________________________________________________________________________________
FORMAT_INSTRUCTIONS = """
ALERT !!!
 - Don't use one tool as action input to another tool. 
 - If you feel that a particular tool needs to be used before the specific tool, then use it first as seperate step.

Use the following format:

Question: the input question you must answer

Thought : explain your thought process behind the action you are going to take, in less than 40
Action : the Tool to take, should be one of [{tool_names}]
Action Input:  the input to the Tool

Observation : the result of the Tool
... (this Thought/Action/Action Input/Observation can repeat N times)


Thought : I now know the final answer
Final Answer: 

"""

# NOTE : 
#   

# NOTE:
# - The Tool you choose along with your Action Input and Tool description will be passed to another agent that will have to fill the arguments for the tool
  # Hence ensure that the Action Input is comprehensive enough for the other agent to fill the tool arguments
# ____________________________________________________________________________________________________________

MISTAKE_SELECTION =  '''

Below you are provided with one of the past mistakes made by another AI agent on some other user query :
{mistake}

Below you are provided with the current user query :
CURRENT_USER_QUERY : {input}

Check diligently if the current user query is similar to the past query, in terms of the vulnerability of the AI agent to make the same mistake.
If there are some chances of making the same or similar mistake on the current user query, return 1 else return 0.

ANSWER : 
'''

# ____________________________________________________________________________________________________________

TOOL_INPUT_PROMPT = '''
You are expected to create a sub-task from the given user query and the intermediate steps taken till now.

The user query is as follows:
  User_Query : {query}

The intermediate steps taken till now to solve the above query are as follows:
{intermediate_steps}

Below is the next tool that needs to be used: {tool_name}

The short description of the tool, to help you reason out, is as follows:
{tool_description}

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

Based on the above information, generate a brief experience for the agent, which will help it to learn from its mistakes :
    - Extract some highlight/ semantics understanding focussing on why is wrong tool not fit for the user query.
    - Extract some highlight /semantics from correct tool description focussing on user query.

* Keep the experience text short and crisp, at max 30 words and atleast 7 words.
* Be specific don't use general statements.
* Put everything as a paragraph in the experience text.

Again repeating, you need to generate an experience for the agent, which will help it to learn from its mistakes.
'''

CORRECT_TRAJECTORY_TILL_NOW = """
tool_name : {tool_name}
tool_input: {tool_input}
tool_reasoning : {log}\n
"""

#____________________________________________________________________________________________________________

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
  0) If the argument value is not explicitly present in the query, then return 0.
  1) Stick to information provided in the user query while filtering the argument.
  2) Return 1 if the argument is relevant to the user query, else return 0.
  3) Don't return anything else other than 1 or 0.
  
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

#____________________________________________________________________________________________________________
CRITIQUE_TEMPLATE = '''

Below you are provided the tools available in toolkit and their description :
{tools}

FORMAT INSTRUCTIONS :
{format_instructions}

Hint :
  - Philosophical , emotional (joy, sadness, life related) questions cannot be answered with available tools

QUERY : {query}
'''

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