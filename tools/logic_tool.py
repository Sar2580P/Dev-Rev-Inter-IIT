from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import sys, os
sys.path.append(os.getcwd())
from utils.llm_utility import llm
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.templates_prompts import VAR_ARGS_LOGIC_TOOL, LOGICAL_TEMPLATE
import ast

prompt = PromptTemplate(
input_variables=["query"],
template= VAR_ARGS_LOGIC_TOOL,
)
extract_var_args = LLMChain(llm = llm , prompt=prompt)
generate_code_prompt = PromptTemplate(template=LOGICAL_TEMPLATE, input_variables=['query' , 'language'])
generate_code = LLMChain(llm = llm , prompt=generate_code_prompt)

class LogicalTool(BaseTool):
    name = "logic_tool"
    description = '''
    THIS TOOL REQUIRES OUTPUTS OF OTHER TOOLS, I.E. IT MUST BE USED ONLY AFTER OTHER TOOLS HAVE BEEN CALLED!!!! 
    This tool is specialised to perform logical operations on its inputs like:
    conditional statements, while loops, addition, subtraction, iterate over lists etc.    
    '''
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside logic_tool tool...')
        code = generate_code.run({'query' : query , 'language' : 'python'})
        print("\033[97m {}\033[00m" .format('Generated Code : \n{i}'.format(i=code)))
        li = []
        li.append({
            'code' : code,
        })
        return   li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")