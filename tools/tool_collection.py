from langchain.agents import Tool
from tools.work_list import WorkList
from tools.summarize_objects import Summarize
from tools.add_work_items_to_sprint import AddWorkItemsToSprint
from tools.create_actionable_tasks_from_text import CreateActionableTasksFromText
from tools.get_similar_work_items import GetSimilarWorkItems
from tools.get_sprint_id import GetSprintId
from tools.prioritize_objects import Prioritize
from tools.search_object_by_name import SearchObjectByName
from tools.who_am_i import WhoAmI


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
    
    
]