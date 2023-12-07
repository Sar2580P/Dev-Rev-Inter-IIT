from langchain.vectorstores.chroma import Chroma
from backend_llm.utils import *
from langchain.docstore.document import Document
from queue import Queue
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from prompts import PREFIX_MISTAKE_MEMORY, SUFFIX_MISTAKE_MEMORY, CORRECT_TRAJECTORY_TILL_NOW

class Memory():
    def __init__(self,vector_db, k) -> None:
        self.queue = Queue(maxsize=10) # current List to be added to Long Term Memory
        self.k = 5
        self.vector_db = vector_db
    
    def stage(self, docs:Document):
        self.queue.put(docs)
        
    def push(self):
        print("Pushing Queue...")
        while not self.queue.empty():
            self.vector_db.add_documents([self.queue.get()])
        
    def pull(self, query:str):
        results  = self.vector_db.search(query, k=self.k , search_type='similarity')
        print("Pulling from Memory...\n" , results) 
        return results
    
    def reset(self):
        self.vector_db.delete()
#__________________________________________________________________________________________________________________________

V_db = Chroma(embedding_function = small_embedding_func, persist_directory= 'database/mistakes_db' , 
                                relevance_score_fn='similarity_search_with_score')
mistake_memory = Memory(k=5,vector_db=V_db)

#__________________________________________________________________________________________________________________________
example_prompt = PromptTemplate(
    input_variables=["tool_name", "tool_input" , "tool_reasoning"],
    template=CORRECT_TRAJECTORY_TILL_NOW,
)

#__________________________________________________________________________________________________________________________

def build_experience(x):
    examples = x['correct_trajectory']

    few_shot_prompt = FewShotPromptTemplate( 
    examples=examples,

    # prompt template used to format each individual example
    example_prompt=example_prompt,

    # prompt template string to put before the examples, assigning roles and rules.
    prefix=PREFIX_MISTAKE_MEMORY,
    
    # prompt template string to put after the examples.
    suffix= SUFFIX_MISTAKE_MEMORY,
    
    # input variable to use in the suffix template
    input_variables=["query", "wrong_tool" , "wrong_reasoning" , "correct_tool" , "correct_reasoning"],
    example_separator="\n", 
)
    chain = LLMChain(llm=llm, prompt=few_shot_prompt)
    print("\033[91m {}\033[00m" .format('build_experience (memory)'))
    y = chain.run({"query": x['query'] ,"wrong_tool": x['wrong_tool'] , "wrong_reasoning": x['wrong_reasoning'] , 
                          "correct_tool": x['correct_tool'] , "correct_reasoning": x['correct_reasoning'] })
    return y

# def delete_experience():
#     mistake_memory.reset()



























# from transformers import pipeline


# def LLMsummarizer(query, tool_list, tool, signal):

#     ARTICLE = f"""
#     You are a Robot's memory that keep logs of all the actions you have yet taken.

#     The current task list is as follows:
#     {tool_list}, it represents the tools which have already been used for the provide query.
#     provided query is {query}, this is given to you by the user.
#     at the current moment after using all the above tools from the tool list we try to use the following tool {tool},
#     the use of this tool turned out to be {signal}.
#     Surmmarize this whole scenario in Natural Language.

#     Remmember the output is based on the user evaluation which is '{signal}';.

#     """

#     print(ARTICLE)

#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#     res = summarizer(ARTICLE, max_length=100, min_length=50, do_sample=False)
#     return res

