from typing import List, Union, Any, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend_llm.utils import llm
import ast 
from prompts import ARGUMENT_EXTRACTION

prompt = PromptTemplate(template=ARGUMENT_EXTRACTION , 
                        input_variables=['function_signature' ,'arg_description','user_query'] ,
                        )
        
signature_chain = LLMChain(llm = llm, prompt = prompt , verbose=True)



def fill_signature(query:str,function_signatures: dict , arg_description:dict)->Dict[str, Union[List[str] , bool]] :
    x = signature_chain.run({'function_signature':function_signatures ,'arg_description' : arg_description , 'user_query':query})
    # print('signature is : ' , x)
    return ast.literal_eval(x)
