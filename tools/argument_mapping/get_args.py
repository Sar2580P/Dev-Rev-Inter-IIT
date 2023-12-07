from typing import List, Union, Any, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend_llm.utils import llm
from tools.argument_mapping.tool_memory import retrieve_tool_experience
from icecream import ic
import ast 

TEMPLATE = '''
You are good at extracting values of certain arguments from a user query in natural language.

Below is the signature of arguments with keys as argument names and 
values as  datatypes in which extracted values should be returned :

{function_signature}


Before moving forward , you need to know the description of each argument :
Specific arguments take only certain values , so you need to know the description of each argument.
{arg_description}


Don't fill the values of arguments which are not present in the user query.
You have to extract the following arguments from the user query :

{user_query}

Drop the arguments which are not present in the user query.
You need to return the dictionary of arguments as keys and extracted values as values.
The argument values are string , so enclose them in double quotes.
Check that the extracted arguments are in correct datatypes before returning .
'''
prompt = PromptTemplate(template=TEMPLATE , 
                        input_variables=['function_signature' ,'arg_description','user_query'] ,
                        )
        
signature_chain = LLMChain(llm = llm, prompt = prompt , verbose=True)


def fill_signature(query:str, function_signatures: dict , arg_description:dict, tool_name:str)->Dict[str, Union[List[str] , bool]] :

    # Retrieve the examples from memory
    formated_example = ''
    memory_examples = retrieve_tool_experience(user_query=tool_name, tool_name=tool_name)
    ic(memory_examples)
    if isinstance(memory_examples , str) or memory_examples == []:
        formated_example = 'No mistakes found'
    else:
        for example in memory_examples:
            formated_example += 'Example: \n{ex}\n'.format(ex = example.page_content)

    # Run the Chain
    x = signature_chain.run({'function_signature':function_signatures ,'arg_description' : arg_description , 'user_query' : query, 'memory_examples' : formated_example})
    # print('signature is : ' , x)
    return ast.literal_eval(x)
