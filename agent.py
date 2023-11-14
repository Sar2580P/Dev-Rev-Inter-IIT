from langchain.agents import ZeroShotAgent, AgentExecutor
from backend_llm.utils import llm
from tools.tool_collection import *
from langchain.agents import initialize_agent
from langchain.agents import AgentType


class PersonalAgent:
    def __init__(self):
        
        # agent
        self.agent = initialize_agent(
                        task_tools,
                        llm,
                        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                        verbose=True,
                        return_intermediate_steps=True,
                        )

    def run(self, query):
        try:
            response = self.agent(query)
            return response
        except Exception as e:
            print(e)
        return "I did not get that. Please try again."


agent_chain = PersonalAgent()
x = agent_chain.run('list p0 issues')
print('\n\n\n\n\n\n\n\n\n' , x)
