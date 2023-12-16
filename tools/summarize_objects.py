from langchain.tools import BaseTool
import sys, os
sys.path.append(os.getcwd())
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from utils.llm_utility import llm
from utils.get_args import fill_signature

class Summarize(BaseTool):
    name = "summarize_objects"
    description = '''
    - This tool is useful for summarizing purposes.
    - It needs a list of objects as input and returns a summary of the objects. 
    '''
    
    bag_of_words = set(["summary", "summarize", "summarize objects", "summarization"])
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside SummarizeTool tool...') 
        signature = {
                        'objects': List[object],
                    }

        arg_description = {
            'objects': 'the objects to be summarized',
        }
        li = []
        
        for key, value in signature.items():
            arg_dtype = {
                'argument_name': key,
                'argument_value': value,
            }
            arg_descr = {
                'argument_name': key,
                'argument_value': arg_description[key],
            }
            query = query.strip('\n').strip()
            ans = query    ## $$PREV[*] is a special keyword that means "use the previous value of this argument"

            if  len(query) !=9:
                
                ans = fill_signature(query = query, arg_name = key , arg_dtype = arg_dtype , arg_descr = arg_descr, tool_name = self.name)
            if ans.strip('\n').strip() != 'NONE':
                li.append({
                    'argument_name': key,
                    'argument_value': ans,
                })
       
        print('Extracted arguments are : ',li)
        return   li
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

# print(('$$PREV[0]' == '$$PREV[..]'))