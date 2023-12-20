from typing import List, Optional, Sequence, Any
from langchain.callbacks.base import BaseCallbackManager
from langchain.schema.language_model import BaseLanguageModel
from langchain.agents.mrkl.prompt import SUFFIX
from langchain.prompts import PromptTemplate
from langchain.tools.base import BaseTool
from agent.tool_collection import *
from langchain.agents.mrkl.base import ZeroShotAgent
from agent.mistakes_selection import *
from langchain.agents.agent import Agent, AgentOutputParser
from utils.templates_prompts import PAST_MISTAKES ,PREFIX, FORMAT_INSTRUCTIONS
from agent.tool_collection import get_relevant_tools

from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from icecream import ic


class PersonalAgent(ZeroShotAgent):
    

    @classmethod
    def create_prompt(
        cls,
        
        user_query: str ,
        tools: Sequence[BaseTool] ,
        tool_task: str ,
        wrong_tool_name: str =  None,
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        mistakes :str = PAST_MISTAKES,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
    ) -> PromptTemplate:
<<<<<<< HEAD
        # print("\033[91m {}\033[00m" .format('create_prompt (agent)'))
        
=======
>>>>>>> 5f516336342c6fd86b86fce98fc5db6b4c3765c5

        if tool_task == '':
            mistakes = ''

        else:
            # past_mistakes = analyse(user_query,wrong_tool_name)
            print("\033[91m {}\033[00m" .format('Attaching past mistakes to the prompt... (agent) for \ntool_task : {tool_task}'.format(tool_task=tool_task )))

            tool_task = tool_task.strip('\n').strip()
            if '\n' in tool_task:
                tool_task = tool_task.split('\n')[0]


            
            past_mistakes = analyse(user_query=user_query,wrong_tool_name=wrong_tool_name, tool_task=tool_task)
            formatted_mistakes = ''
            
            if past_mistakes == 'No mistakes found  relevant to this query' or past_mistakes == []:
                formatted_mistakes = 'No mistakes found  relevant to this query'
            else :
                for mistake in past_mistakes:
                    formatted_mistakes += mistake.metadata['learning'] 
    
            mistakes = mistakes.format(mistakes = formatted_mistakes)
            # print(mistakes)
        #________________________________________________________________________________
        tools = get_relevant_tools(user_query)

        tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        tool_names = ", ".join([tool.name for tool in tools])
        format_instructions = format_instructions.format(tool_names=tool_names)
        #________________________________________________________________________________



        template = "\n\n".join([prefix, tool_strings,mistakes, format_instructions,  suffix])
        # ic(template)
        if input_variables is None:
            input_variables = ["input", "agent_scratchpad"]
        
        prompt =  PromptTemplate(template=template, input_variables=input_variables)
        if tool_task != '':
            print("\033[91m {}\033[00m" .format('create_prompt (agent)'))
            print('****',prompt.template.format(input=user_query, agent_scratchpad=''))
        return prompt
    #________________________________________________________________________________________________________________________________
    @classmethod
    def from_llm_and_tools(
        cls,
        llm: BaseLanguageModel,
        tools: Sequence[BaseTool],
        user_query: str = '',
        callback_manager: Optional[BaseCallbackManager] = None,
        output_parser: Optional[AgentOutputParser] = None,
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Agent:
        """Construct an agent from an LLM and tools."""
        cls._validate_tools(tools)

        prompt = cls.create_prompt(
            tools=tools,
            prefix=prefix,
            user_query=user_query,
            suffix=suffix,
            format_instructions=format_instructions,
            input_variables=input_variables,
            wrong_tool_name = None,
            tool_task = '',
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callback_manager=callback_manager,
        )
        tool_names = [tool.name for tool in tools]
        _output_parser = output_parser or cls._get_default_output_parser()
        print(_output_parser)
        return cls(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            output_parser=_output_parser,
            **kwargs,
        )

#________________________________________________________________________________________________________________________________   
agent_obj = PersonalAgent.from_llm_and_tools(
            llm = llm, tools = task_tools, output_parser=ReActSingleInputOutputParser()
            )