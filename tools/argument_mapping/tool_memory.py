from memory import Memory
from backend_llm.utils import *
from langchain.vectorstores.chroma import Chroma
from langchain.docstore.document import Document
from evaluator import *

#__________________________________________________________________________________________________________________________

tool_database = Chroma(embedding_function = embedding_func, persist_directory= 'database/tool_mistake_db' , 
                                relevance_score_fn='similarity_search_with_score')
tool_mistake_memory = Memory(k=2, vector_db=tool_database)

#__________________________________________________________________________________________________________________________

def build_tool_experience(llm_tool, correct_tool):
    ic(llm_tool)
    ic(correct_tool)
    response, analogy, correct_tool = validate(correct_tool, llm_tool)
    ic(analogy, response)
    
    if response is not True:
        experience = analogy
        metadata = {
            'tool_name': llm_tool[0]['tool_name']
        }
        doc = Document(page_content=experience , metadata=metadata)
        tool_mistake_memory.stage(doc)

def retrieve_tool_experience(tool_name:str, user_query:str):
    if(tool_mistake_memory.queue.empty() == False):
        tool_mistake_memory.push()
    filter = {
        'tool_name':tool_name,
    }
    tool_mistakes = tool_mistake_memory.pull(query=user_query,filter=filter) if user_query != '' else ''    
    return tool_mistakes

    


