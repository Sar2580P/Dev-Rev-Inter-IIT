from langchain.tools import BaseTool
from typing import Optional, List, Any
import sys , os
sys.path.append(os.getcwd())
from tools.work_list import WorkList
from tools.summarize_objects import Summarize
from tools.add_work_items_to_sprint import AddWorkItemsToSprint
from tools.create_actionable_tasks_from_text import CreateActionableTasksFromText
from tools.get_similar_work_items import GetSimilarWorkItems
from tools.get_sprint_id import GetSprintId
from tools.prioritize_objects import Prioritize
from tools.search_object_by_name import SearchObjectByName
from tools.who_am_i import WhoAmI
import ast 
from backend_llm.utils import llm, small_llm
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompts import TOOL_RELEVENCY_TEMPLATE

task_tools = [
    WhoAmI(),
    SearchObjectByName(),
    GetSprintId(),
    WorkList() , 
    Summarize() ,
    AddWorkItemsToSprint(),
    CreateActionableTasksFromText(),
    GetSimilarWorkItems(),
    Prioritize(),
    # Search(), 
    # Lookup()
]

tool_relevency_prompt = PromptTemplate(template= TOOL_RELEVENCY_TEMPLATE , input_variables=['query' , 'tool_name' , 'tool_description'])
check_relevency = LLMChain(llm = small_llm , prompt = tool_relevency_prompt)

def get_relevent_tools(user_query:str) -> List[BaseTool]:
    relevent_tools = []
    relevent_tool_names = set()
    for tool in task_tools:
        input = {
            "query" : user_query,
            "tool_name" : tool.name,
            "tool_description" : tool.description
        }
        ans =check_relevency(inputs = input)
        # print('\n\n\n\n' ,ans, '\n\n\n')
        print('\n\n\n\n' ,ans['text'], '\n\n\n')
        is_tool_relevent = int(ans['text']) == 1
        if is_tool_relevent:
            relevent_tools.append(tool)
            relevent_tool_names.add(tool.name)
    # TODO: sort tools by relevency
    if "add_work_items_to_sprint" in relevent_tool_names and "get_sprint_id" not in relevent_tool_names:
        relevent_tools.append(GetSprintId())
        relevent_tool_names.add("get_sprint_id")

    print("\033[91m {}\033[00m" .format('Finally picking below tools ...\n{relevent_tool_names}'.format(relevent_tool_names = relevent_tool_names)))
    print(relevent_tools)
    return relevent_tools


query = "Prioritize my P0 issues and add them to the current sprint"
tools = get_relevent_tools(query)

{'query': 'Prioritize my P0 issues and add them to the current sprint', 'tool_name': 'whoami', 'tool_description': '\n            Whenever pronouns are present in query like "me", "I" , etc.\n            Call this tool first to get the user_id of the user who is asking the query.\n            Do not call this tool if the query is related to another user or the user is asking some task for another user.\n            This tool will return the user_id which can be used by other tools.\n            \n', 'text': '0'}
