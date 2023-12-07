from typing import List, Union, Any, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend_llm.utils import llm
from tools.argument_mapping.tool_memory import retrieve_tool_experience
from icecream import ic
import ast
from prompts import TOOLS_PROMPT_EXAMPLES

prompt = PromptTemplate(template=TOOLS_PROMPT_EXAMPLES , 
                        input_variables=['function_signature' ,'arg_description','user_query','memory_examples'] ,
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
