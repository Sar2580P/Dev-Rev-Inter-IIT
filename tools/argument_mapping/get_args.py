from typing import List, Optional, Type, Union, Any, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend_llm.utils import llm
import ast 

TEMPLATE = '''
You are good at extracting values of certain arguments from a user query in natural language.

Below is the signature of arguments with keys as argument names and 
values as  datatypes in which extracted values should be returned :
{function_signature}

below are the columns used in database ,they are arranged according to the samples drawn from database :
{columns}

Below are samples drawn from database to look at how the arguments are used in the database :
{sample_rows}

for 'ticket_needs_response': False --> 0 , True --> 1
Don't fill the values of arguments which are not present in the user query.
You have to extract the following arguments from the user query :
{user_query}

You need to return the dictionary of arguments as keys and extracted values as values.
Check that the extracted arguments are in correct datatypes before returning .
'''
prompt = PromptTemplate(template=TEMPLATE , 
                        input_variables=['function_signature' ,'columns', 'sample_rows' , 'user_query'] ,
                        )
        
signature_chain = LLMChain(llm = llm, prompt = prompt , verbose=True)



def fill_signature(query:str,columns ,sample_rows , function_signatures: dict)->Dict[str, Union[List[str] , bool]] :
    x = signature_chain.run({'function_signature':function_signatures ,'columns':columns , 'sample_rows' : sample_rows , 'user_query':query})
    print('signature is : ' , x)
    return ast.literal_eval(x)
    # return x