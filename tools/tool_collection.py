from langchain.agents import Tool
from tools.work_list import WorkList
from tools.summarize_objects import Summarize

task_tools = [
    WorkList() , 
    Summarize() ,
    
]