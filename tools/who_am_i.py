from langchain.tools import BaseTool
from typing import Optional, List, Any 
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from backend_llm.utils import llm

class WhoAmI(BaseTool):
    name = "whoami"
    description = '''
            Whenever pronouns are present in query like "me", "I" , etc.
            Call this tool first to get the user_id of the user who is asking the query.
            Do not call this tool if the query is related to another user or the user is asking some task for another user.
            This tool will return the user_id which can be used by other tools.
            
'''

    def _run(
        self, query:str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print('inside who_am_i tool , query is : \n' , query) 
        
        return list()
    

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")



