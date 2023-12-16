from langchain.tools import BaseTool
from typing import Optional, Type, List, Any, Tuple
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from utils.get_args import fill_signature, arg_filter
from utils.llm_utility import llm

class WorkList(BaseTool):
    name = "works_list"
    description = '''
    - This tool can handle all queries related to work items.
    
    Some salient features of this tool are :
\   - Can enquire about creators , owners of work items, issues, tickets, tasks, etc.
    - Can serch for work items applied to a specific part.
    - Can limit the number of work items to be returned.
    - Can filter work items on the basis of issue 
            - priority  : p0 , p1 , p2
            - rev_orgs  : list of rev_orgs
    - Can filter work items on the basis of ticket
            - severity  : blocker , high , medium , low
            - rev_org   : list of rev_orgs
            - source_channel : list of source_channels
            - needs_response : True , False
    - Can filter work items on the basis of stage
            - name : list of stage names
    - Can filter work items on the basis of type : issues , ticket , task
    '''

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Any:
        print('\ninside work_list tool...')
        

        filtered_signature , filtered_arg_description = self._filtered_arguments(query)
        li = []
        for key, value in filtered_signature.items():
            arg_dtype = {
                'argument_name': key,
                'argument_value': value,
            }
            arg_descr = {
                'argument_name': key,
                'argument_value': filtered_arg_description[key],
            }
            x = fill_signature(query = query, arg_name = key , arg_dtype = arg_dtype , arg_descr = arg_descr, tool_name = self.name)
            if x.strip('\n').strip() != 'NONE':
                li.append({
                    'argument_name': key,
                    'argument_value': x,
                })
        
        print('Extracted arguments are : ',li)
        return   li

#____________________________________________________________________________________________________________________________________
    def _filtered_arguments(self, query: str) -> Tuple[dict, dict]:
        """Returns the filtered arguments and their descriptions."""

        signature = {
                    'created_by': List[str] ,
                    'issue.rev_orgs': List[str] ,
                    'owned_by': List[str] ,
                    'ticket.needs_response': bool ,
                    'ticket.rev_org': List[str] ,
                    'ticket.source_channel': List[str] ,
                   }
        
        arg_description = {
            'applies_to_part': "specific keywords should be present --> 'part to which issue applies' , 'applies' , 'part/s'",
            'created_by': 'name of person who created the issue',
            'issue.priority': '''can be either of types : "p0" , "p1" , "p2". Nothing else is allowed''',
            'issue.rev_orgs': 'orgs that reviewed issue',
            'limit' : 'maximum number of work-items to return. Specific keyword must be present --> "limit"' , 
            'owned_by': 'name of person who owns the issue',
            'stage.name': 'stage of issue',
            'ticket.needs_response': 'Filters for tickets that need a response, either of types : "True" , "False"',
            'ticket.rev_org': 'Filters for tickets associated with any of the provided Rev organizations ',
            'ticket.severity': 'either of types : blocker , high , medium , low',
            'ticket.source_channel': 'Filters for tickets with any of the provided source channels',
            'type': 'either of types : issues , ticket , task'
        }

        filtered_signature = {}
        filtered_arg_description = {}

        query = query.lower().strip()
        arguments = arg_description.keys()
        if 'p0'in query or 'p1'in query or 'p2'in query:
            filtered_signature['issue.priority'] = str
            filtered_arg_description['issue.priority'] = arg_description['issue.priority']

        if "\bpart.*applied\b" in query or "applied" in query or "\applied.*parts\b" in query :
            filtered_signature['applies_to_part'] = List[str]
            filtered_arg_description['applies_to_part'] = arg_description['applies_to_part']

        if 'all' in query or 'limit..\b' in query:
            filtered_signature['limit'] = int
            filtered_arg_description['limit'] = arg_description['limit']

        if 'issues' in query or  'ticket' in query or  'task' in query:
            filtered_signature['type'] = List[str]
            filtered_arg_description['type'] = arg_description['type']

        if 'blocker' in query or 'high' in query or 'medium' in query or 'low' in query:
            filtered_signature['ticket.severity'] = List[str]
            filtered_arg_description['ticket.severity'] = arg_description['ticket.severity']

        if 'stage' in query:
            filtered_signature['stage.name'] = List[str]
            filtered_arg_description['stage.name'] = arg_description['stage.name']


        x = set(filtered_signature.keys())
        x.add('issue.priority')
        x.add('applies_to_part')
        x.add('limit')
        x.add('type')
        x.add('ticket.severity')
        x.add('stage.name')

        remaining_arguments = set(arguments) - x

        # filtering remaining arguments semantically using llm
        for arg in remaining_arguments:
            ans = arg_filter.run({'query':query,'arg_description':arg_description[arg] , 'arg_name' : arg})
            if '1' in ans.strip() :
                filtered_signature[arg] = signature[arg]
                filtered_arg_description[arg] = arg_description[arg]

        return filtered_signature, filtered_arg_description

#____________________________________________________________________________________________________________________________________
    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
