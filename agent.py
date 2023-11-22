from langchain import hub
from tools.tool_collection import *
from langchain.tools.render import render_text_description
from backend_llm.utils import llm
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser

agent_prompt = hub.pull("hwchase17/react")
agent_prompt = agent_prompt.partial(
    tools=render_text_description(task_tools),
    tool_names=", ".join([t.name for t in task_tools]),
)
# print(agent_prompt)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | agent_prompt
    | llm
    | ReActSingleInputOutputParser()
)