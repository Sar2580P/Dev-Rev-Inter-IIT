from langchain.vectorstores.chroma import Chroma
from backend_llm.utils import *
from langchain.docstore.document import Document
from queue import Queue
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain

class Memory():
    def __init__(self, k) -> None:
        self.queue = Queue(maxsize=10) # current List to be added to Long Term Memory
        self.k = 5
        self.vector_db = Chroma(embedding_function = embedding_func, persist_directory= 'database/mistakes_db' , 
                                relevance_score_fn='similarity_search_with_score')
    
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
    
    # def reset(self , mistake):
    #     self.vector_db.delete()
#__________________________________________________________________________________________________________________________

mistake_memory = Memory(k=5)

prefix_template = '''
You are good at reasoning on mistakes that has been made by another AI agent while deciding the next tool to be used for the given query.

Below is the user query:
    Query : {query}

Below is the trajectory of right tools used till now and their tool input as well as the reasoning behind using them.
'''
#__________________________________________________________________________________________________________________________
suffix_template = '''

The agent attempts to select the next tool, which turns out to be wrong choice, in the trajectory based on the user query:
    Wrong Tool : {wrong_tool}
    Wrong Reasoning : {wrong_reasoning}

The agent was expected to select the following tool inplace of above tool with following reasoning:
    Correct Tool : {correct_tool}
    Correct Reasoning : {correct_reasoning}

Based on the above information , you are expected to highlight on the information present in user query which was missed by agent
Again repeating, you need to generate an experience for the agent, which will help it to learn from its mistakes.

The experience text should not exceed 30 words.

'''
#__________________________________________________________________________________________________________________________
example_formatter_template = """
tool_name : {tool_name}
tool_input: {tool_input}
tool_reasoning : {log}\n
"""
example_prompt = PromptTemplate(
    input_variables=["tool_name", "tool_input" , "tool_reasoning"],
    template=example_formatter_template,
)

#__________________________________________________________________________________________________________________________

def build_experience(x):
    examples = x['correct_trajectory']

    few_shot_prompt = FewShotPromptTemplate( 
    examples=examples,

    # prompt template used to format each individual example
    example_prompt=example_prompt,

    # prompt template string to put before the examples, assigning roles and rules.
    prefix=prefix_template,
    
    # prompt template string to put after the examples.
    suffix= suffix_template,
    
    # input variable to use in the suffix template
    input_variables=["query", "wrong_tool" , "wrong_reasoning" , "correct_tool" , "correct_reasoning"],
    example_separator="\n", 
)
    chain = LLMChain(llm=llm, prompt=few_shot_prompt)
    print("\033[91m {}\033[00m" .format('build_experience (memory)'))
    y = chain.run({"query": x['query'] ,"wrong_tool": x['wrong_tool'] , "wrong_reasoning": x['wrong_reasoning'] , 
                          "correct_tool": x['correct_tool'] , "correct_reasoning": x['correct_reasoning'] })
    return y




























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

