PAST_MISTAKES ='''

Before proceeding further, below I have mentioned common mistakes made by you while using the tools.

{mistakes}

!! PLEASE GO THROUGH THEM CAREFULLY AND AVOID MAKING SIMILAR MISTAKES.
'''
SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}

"""


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
You are good at extracting values of certain arguments from a user query in natural language.
Below is the signature of arguments with keys as argument names and 
values as  datatypes in which extracted values should be returned :
{function_signature}

Before moving forward , you need to know the description of each argument :
Specific arguments take only certain values , so you need to know the description of each argument.
{arg_description}

FORMAT INSTRUCTION -->
- Don't create argument names that are not present above.
- You need to return the dictionary of arguments as keys and extracted values as values.
- Ensure that argument values are in double quotes.
- Check that the extracted arguments are in correct datatypes before returning.

Don't mention those arguments in final query whose values are not present in user query.
You have to extract the following arguments from the user query :
{user_query}

Before returning the dictionary of arguments, 
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

- You need to judge whether the query can be answered by the tools available in toolkit or not, ALONG WITH REASON.
- Return 1 if the query can be answered by the tools available in toolkit, else return 0 , ALONG WITH REASON.
- Nothing else should be returned.

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

QUERY : {query}
ANSWER : 
REASON :
'''

# You are also provided the dataypes of arguments present in the user query:
# {function_signature}