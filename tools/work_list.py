from langchain.tools import BaseTool
from typing import Optional, Type, List, Any
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from utils.get_args import fill_signature
from utils.llm_utility import llm


class WorkList(BaseTool):
    name = "works_list"
    description = '''This tool is useful when following arguments are present in the query :  
        
        Below are the arguments and their description :
            'applies_to_part': 'part to which issue applies',
            'created_by': 'name of person who created the issue',
            'issue.priority': ' either of types : "p0" , "p1" , "p2" ',
            'issue.rev_orgs': 'orgs that reviewed issue',
            'limit' : 'maximum number of work-items to return' , 
            'owned_by': 'name of person who owns the issue',
            'stage.name': 'stage of issue',
            'ticket.needs_response': 'either of types : "True" , "False"',
            'ticket.rev_org': 'orgs that reviewed ticket',
            'ticket.severity': 'either of types : blocker , high , medium , low',
            'ticket.source_channel': 'source channel of ticket',
            'type': 'either of types : issues , ticket , task'
        
    '''

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside work_list tool...')
        signature = {'applies_to_part': List[str],
                    'created_by': List[str] ,
                    'issue.priority': str ,
                    'issue.rev_orgs': List[str] ,
                    'limit' : int ,
                    'owned_by': List[str] ,
                    'stage.name': List[str] ,
                    'ticket.needs_response': bool ,
                    'ticket.rev_org': List[str] ,
                    'ticket.severity': List[str] , 
                    'ticket.source_channel': List[str] ,
                    'type': List[str],}
        
        arg_description = {
            'applies_to_part': 'part to which issue applies',
            'created_by': 'name of person who created the issue',
            'issue.priority': ' either of types : "p0" , "p1" , "p2" ',
            'issue.rev_orgs': 'orgs that reviewed issue',
            'limit' : 'maximum number of work-items to return' , 
            'owned_by': 'name of person who owns the issue',
            'stage.name': 'stage of issue',
            'ticket.needs_response': 'Filters for tickets that need a response, either of types : "True" , "False"',
            'ticket.rev_org': 'Filters for tickets associated with any of the provided Rev organizations ',
            'ticket.severity': 'either of types : blocker , high , medium , low',
            'ticket.source_channel': 'Filters for tickets with any of the provided source channels',
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
