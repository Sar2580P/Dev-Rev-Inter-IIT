from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm
from tools.argument_mapping.get_args import fill_signature

class WhoAmI(BaseTool):
    name = "whoami"
    description = '''
            Whenever pronouns are present in query like "me", "I" , etc.
            Call this tool first to get the user_id of the user who is asking the query.
            Do not call this tool if the query is related to another user or the user is asking some task for another user.
            This tool will return the user_id which can be used by other tools.
            
'''

    # def _run(
    #     self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    # ) -> str:
    #     print('inside who_am_i tool , query is : \n' , query) 
        
    #     return list()
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        # print('inside who_am_i tool , query is : \n' , query) 
        signature = {
                        'ids': List[str],
                    }
        
        # TODO
        arg_description = {
            'ids': 'the list of ids of the users',
        }
        column_args = fill_signature(query,function_signatures= signature ,arg_description=arg_description, tool_name = self.name)
        li = []
        for key, value in column_args.items():
            x = {
                'argument_name': key,
                'argument_value': value,
            }
            li.append(x)
        return   li


    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")



