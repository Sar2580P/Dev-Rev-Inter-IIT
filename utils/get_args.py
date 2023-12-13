from typing import List, Union, Any, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.llm_utility import llm
from memory.tool_memory import retrieve_tool_experience
from utils.prompts import TOOLS_PROMPT_EXAMPLES
import re
from utils.tool_output_parser import parser
from icecream import ic

prompt = PromptTemplate(template=TOOLS_PROMPT_EXAMPLES , 
                        input_variables=['function_signature' ,'arg_description','user_query','memory_examples'] ,
                        )
        
signature_chain = LLMChain(llm = llm, prompt = prompt , verbose=True)


def fill_signature(query:str, function_signatures: dict , arg_description:dict, tool_name:str)->Dict[str, Union[List[str] , bool]] :

    # Retrieve the examples from memory
    # formated_example = 'No errors made by the agent'
    # memory_examples = retrieve_tool_experience(user_query=tool_name, tool_name=tool_name)
    # # ic(memory_examples)

    # formated_example = ""
    # if isinstance(memory_examples , str) or memory_examples == []:
    #     formated_example = 'No mistakes found'
    # else:
    #     for example in memory_examples:
    #         formated_example += 'Example: \n{ex}\n'.format(ex = example.page_content)
   
    extracted_args = {}
    for key in function_signatures.keys():
        ic(tool_name)
        ic(key)
        data_type = str(function_signatures[key])
        ic(data_type)
        description = arg_description[key]
        ic(description)
        x = signature_chain.run({'argument_type':data_type ,'arg_description' : description , 'user_query' : query})

        # 
        x = re.sub(r'""', '"', x)
        x = re.sub('true','True',x)
        x = re.sub('false','False',x)
        print('signature is : ' , x)
        extracted_args[key] = x

    return extracted_args
