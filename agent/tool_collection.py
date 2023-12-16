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
from utils.llm_utility import llm
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from tools.logic_tool import LogicalTool
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import icecream as ic

task_tools = [
  
    WhoAmI(),
    SearchObjectByName(),
    GetSprintId(),
    WorkList() , 
    Summarize() ,
    AddWorkItemsToSprint(),
    # LogicalTool(),
    CreateActionableTasksFromText(),
    GetSimilarWorkItems(),
    Prioritize(),
    
]

def get_relevant_tools(query: str ) -> List[BaseTool]:
    """Returns the list of relevant tools for the query."""
    relevant_tools = []
    for tool in task_tools:
        if tool.name == 'works_list':
            relevant_tools.append(tool)
            continue

        tool_bag_of_words = tool.bag_of_words
        for word in tool_bag_of_words:
            if word.strip() in query.lower().strip():
                relevant_tools.append(tool)
                break

    return relevant_tools



# x = get_relevant_tools('Get all my work items with status as "In Progress" and add them to sprint')

# print(x)
