from langchain.agents import Tool
from tools.work_list import WorkList
from tools.summarize_objects import Summarize
from tools.prioritize_objects import Prioritize
task_tools = [
    WorkList() , 
    Summarize() ,
    Prioritize() ,
    
]