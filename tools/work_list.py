from langchain.tools import BaseTool
from typing import Optional, Type, List, Any
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from tools.argument_mapping.get_args import fill_signature
from backend_llm.utils import llm


class WorkList(BaseTool):
    name = "works_list"
    description = '''This tool is useful when following arguments are present in the query :  
        
        Below are the arguments and their description :
            'applies_to_part': 'part to which issue applies',
            'created_by': 'name of person who created the issue',
            'issue_priority': ' either of types : "p0" , "p1" , "p2" ',
            'issue_rev_orgs': 'orgs that reviewed issue',
            'limit' : 'maximum number of work-items to return' , 
            'owned_by': 'name of person who owns the issue',
            'stage_name': 'stage of issue',
            'ticket_needs_response': 'either of types : "True" , "False"',
            'ticket_rev_org': 'orgs that reviewed ticket',
            'ticket_severity': 'either of types : blocker , high , medium , low',
            'ticket_source_channel': 'source channel of ticket',
            'type': 'either of types : issues , ticket , task'
        
    '''

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside work_list tool...')
        signature = {'applies_to_part': List[str],
                    'created_by': List[str] ,
                    'issue_priority': str ,
                    'issue_rev_orgs': List[str] ,
                    'limit' : int ,
                    'owned_by': List[str] ,
                    'stage_name': List[str] ,
                    'ticket_needs_response': bool ,
                    'ticket_rev_org': List[str] ,
                    'ticket_severity': List[str] , 
                    'ticket_source_channel': List[str] ,
                    'type': List[str],}
        
        arg_description = {
            'applies_to_part': 'part to which issue applies',
            'created_by': 'name of person who created the issue',
            'issue_priority': ' either of types : "p0" , "p1" , "p2" ',
            'issue_rev_orgs': 'orgs that reviewed issue',
            'limit' : 'maximum number of work-items to return' , 
            'owned_by': 'name of person who owns the issue',
            'stage_name': 'stage of issue',
            'ticket_needs_response': 'whether ticket needs response',
            'ticket_rev_org': 'orgs that reviewed ticket',
            'ticket_severity': 'either of types : blocker , high , medium , low',
            'ticket_source_channel': 'source channel of ticket',
            'type': 'either of types : issues , ticket , task'
        }
        column_args = fill_signature(query,function_signatures= signature , arg_description=arg_description,tool_name=self.name)
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
