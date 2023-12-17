from langchain.agents.agent import *
import sys, os
sys.path.append(os.getcwd())
import ast
from utils.llm_utility import *
from agent.tool_collection import *
from langchain.agents import AgentExecutor
from langchain.agents.loading import AGENT_TO_CLASS
import json
from agent_executor.auxiliary_executor import *
from agent.agent import PersonalAgent
from evaluator import *
from memory.tool_memory import build_tool_experience
import copy
from utils.prompts import CRITIQUE_TEMPLATE
from wandb.integration.langchain import WandbTracer



# agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
# agent_cls = AGENT_TO_CLASS[agent]
# agent_obj = agent_cls.from_llm_and_tools(
#             llm, task_tools,  
#         )


response_schemas = [
    ResponseSchema(name="answer", description="Return 1 if user query can be answered by the available tools, else 0."),
    ResponseSchema(name="reason", description="Reason why available tools can/ cannot answer the user query based on tool descriptions.")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

critique = LLMChain(llm = llm , prompt=PromptTemplate(template=CRITIQUE_TEMPLATE, input_variables=['query' ,'tools'], 
                                                      partial_variables={'format_instructions' : output_parser.get_format_instructions()}))

class CustomAgentExecutor(AgentExecutor):
    return_schema :List[Dict] = []   # added by me
    tool_count : int = 0             # added by me
    train_mode : bool = True      # added by me
    checkpoints = {}                 # added by me
    true_tools : List[str] = None                 # added by me
    correct_trajectory : List[Dict] = []            # added by me
    ground_truth : List[Dict] = []
    execution_chain : List[Dict] = []   # added by me
    
    #_______________________________________________________________________________________________
    def eval(self):
        self.train_mode = False
    def train(self):
        self.train_mode = True

    def get_tool_lists(self , ground_truth:str):
        ground_truth = json.loads(ground_truth)
        self.ground_truth = ground_truth
        self.true_tools = [tool['tool_name'] for tool in ground_truth]
    
    #_______________________________________________________________________________________________
    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        
        """Run text through and get agent response."""

        # is_query_valid = critique.run({'query' : inputs['input'] , 'tools' : "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])})
        # print('Critique output: {s}\n'.format(s = is_query_valid))
        # if '0' in is_query_valid:
        #     print("hi")
        #     return self._return(
        #             output=AgentFinish(return_values = {'output':'dvdvsdd'} ,
        #                                  log ='I now know the final answer.\nFinal Answer : sarvagya'),
        #                                  intermediate_steps = [] , run_manager=run_manager
        #     )
        
        # Construct a mapping of tool name to tool for easy lookup
        name_to_tool_map = {tool.name: tool for tool in self.tools}
        # We construct a mapping from each tool to a color, used for logging.
        color_mapping = get_color_mapping(
            [tool.name for tool in self.tools], excluded_colors=["green", "red"]
        )
        intermediate_steps: List[Tuple[AgentAction, str]] = []
        # Let's start tracking the number of iterations and time elapsed

        iterations = 0
        time_elapsed = 0.0
        start_time = time.time()
        
        # We now enter the agent loop (until it returns something).
        print("\033[1;35;40m {} \033[0m" .format('updating agent prompt with mistakes'))
        self.agent.llm_chain.prompt = self.agent.create_prompt(tools = self.tools, 
                                                               user_query=inputs['input'])
        
        while self._should_continue(iterations, time_elapsed):
            if self.tool_count == 0:        
                self.return_schema = []        
                intermediate_steps = []   
                self.correct_trajectory = []    
                self.checkpoints = {}   
                self.execution_chain = []    

            next_step_output = self._take_next_step(
                                                    name_to_tool_map,
                                                    color_mapping,
                                                    inputs,
                                                    intermediate_steps,
                                                    run_manager=run_manager,
                                                )
            if isinstance(next_step_output, AgentFinish):
                self.tool_count = 0             
                print("\033[1;35;40m {} \033[0m" .format('checkpoints ---> '))
                print("\033[1;35;40m {} \033[0m" .format(self.checkpoints))


                return self._return(
                    next_step_output, intermediate_steps, run_manager=run_manager
                )
            
            self.tool_count += 1            # added by me

            intermediate_steps.extend(next_step_output)
            if len(next_step_output) == 1:
                next_step_action = next_step_output[0]
                # See if tool should return directly
                tool_return = self._get_tool_return(next_step_action)
                if tool_return is not None:
                    return self._return(
                        tool_return, intermediate_steps, run_manager=run_manager
                    )
            iterations += 1
            time_elapsed = time.time() - start_time
        output = self.agent.return_stopped_response(
            self.early_stopping_method, intermediate_steps, **inputs
        )
        return self._return(output, intermediate_steps, run_manager=run_manager)
    #_______________________________________________________________________________________________
    def _return(
        self,
        output: AgentFinish,
        intermediate_steps: list,
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        if run_manager:
            run_manager.on_agent_finish(output, color="green", verbose=self.verbose)
        final_output = output.return_values
        if self.return_intermediate_steps:
            final_output["intermediate_steps"] = intermediate_steps
        return final_output
    #_______________________________________________________________________________________________
    def _take_next_step(
        self,
        name_to_tool_map: Dict[str, BaseTool],
        color_mapping: Dict[str, str],
        inputs: Dict[str, str],
        intermediate_steps: List[Tuple[AgentAction, str]],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Union[AgentFinish, List[Tuple[AgentAction, str]]]:
        """Take a single step in the thought-tool-observation loop.

        Override this to take control of how the agent makes and acts on choices.
        """
        try:
            intermediate_steps = self._prepare_intermediate_steps(intermediate_steps)
            # ic(intermediate_steps)

            # Call the LLM to see what to do.
            output = self.agent.plan(
                intermediate_steps,
                callbacks=run_manager.get_child() if run_manager else None,
                **inputs,
            )
            ic(inputs , intermediate_steps , output , self.train_mode)
            print("\033[1;35;40m {} \033[0m" .format('inside _take_next_step , agent.plan completed ...'))
            if self.train_mode :   # added by me
                if self.tool_count == len(self.true_tools):
                    output = AgentFinish(return_values = {'output':'User query successfully answered'} ,
                                         log ='I now know the final answer.\nFinal Answer : sarvagya')
                if isinstance(output ,AgentAction):

                #==============================================================================================================
                    current_schema = copy.deepcopy(self.return_schema)
                    current_schema.append({                        
                        'tool_name': output.tool,
                        'arguments': [],
                    })
                    
                    # ic(self.ground_truth, current_schema[:-1], output.tool)
                    is_right_decision, analogy, correct_arg = validate(self.ground_truth, current_schema[:-1], output.tool)  # added by me , evaluator

                    # ic(is_right_decision, analogy, correct_arg)

                    if(is_right_decision == True):
                        analogy = ''

                #==============================================================================================================
                    if not is_right_decision:
                        print("\033[1;35;40m {} \033[0m" .format('agent planned wrongly, picked tool : {} ...'.format(output.tool)))
                        curr_step = {
                                    'correct_tool': self.true_tools[self.tool_count],
                                    'correct_tool_description': name_to_tool_map[self.true_tools[self.tool_count]].description,
                                    'wrong_tool': output.tool,
                                    'wrong_tool_description': name_to_tool_map[output.tool].description,
                            }
                        self.checkpoints[self.tool_count] = curr_step
                        
                        input = {
                            'correct_tool' : self.true_tools[self.tool_count] ,
                            'correct_tool_description' : name_to_tool_map[self.true_tools[self.tool_count]].description ,
                            'query' : inputs['input'] ,
                            'intermediate_steps' : intermediate_steps ,
                        }
                        print("\033[1;35;40m {} \033[0m".format('\ncalling auxiliary_executor ...\nCreating sub task for tool : {} '.format(self.true_tools[self.tool_count])))
                        answer = sub_task(input)   
                        tool_input, log = answer['tool_input'], answer['reason']                     
              
                        output.tool = self.true_tools[self.tool_count]
                        output.tool_input = tool_input
                        output.log = log+"\nAction: {tool}\nAction Input:{tool_input}".format(tool=output.tool, 
                                                                                              tool_input=output.tool_input)
                    
                    self.correct_trajectory.append({
                        'tool_name': output.tool,
                        'tool_input': output.tool_input,
                        'log': analogy+". "+ output.log.split('\n')[0]
                    })
                
        except OutputParserException as e:
            if isinstance(self.handle_parsing_errors, bool):
                raise_error = not self.handle_parsing_errors
            else:
                raise_error = False
            if raise_error:
                raise ValueError(
                    "An output parsing error occurred. "
                    "In order to pass this error back to the agent and have it try "
                    "again, pass `handle_parsing_errors=True` to the AgentExecutor. "
                    f"This is the error: {str(e)}"
                )
            text = str(e)
            if isinstance(self.handle_parsing_errors, bool):
                if e.send_to_llm:
                    observation = str(e.observation)
                    text = str(e.llm_output)
                else:
                    observation = "Invalid or incomplete response"
            elif isinstance(self.handle_parsing_errors, str):
                observation = self.handle_parsing_errors
            elif callable(self.handle_parsing_errors):
                observation = self.handle_parsing_errors(e)
            else:
                raise ValueError("Got unexpected type of `handle_parsing_errors`")
            output = AgentAction("_Exception", observation, text)
            if run_manager:
                run_manager.on_agent_action(output, color="green")
            tool_run_kwargs = self.agent.tool_run_logging_kwargs()
            observation = ExceptionTool().run(
                output.tool_input,
                verbose=self.verbose,
                color=None,
                callbacks=run_manager.get_child() if run_manager else None,
                **tool_run_kwargs,
            )
            return [(output, observation)]
        # If the tool chosen is the finishing tool, then we end and return.
        if isinstance(output, AgentFinish):
            return output
        
        actions: List[AgentAction]
        if isinstance(output, AgentAction):
            actions = [output]
        else:
            actions = output
        result = []
        for agent_action in actions:
            if run_manager:
                run_manager.on_agent_action(agent_action, color="green")
            # Otherwise we lookup the tool
            if agent_action.tool in name_to_tool_map:
                tool = name_to_tool_map[agent_action.tool]
                return_direct = tool.return_direct
                color = color_mapping[agent_action.tool]
                tool_run_kwargs = self.agent.tool_run_logging_kwargs()
                if return_direct:
                    tool_run_kwargs["llm_prefix"] = ""
                # We then call the tool on the tool input to get an observation
                arguments = tool.run(
                    agent_action.tool_input,
                    verbose=False,
                    color=color,
                    callbacks=run_manager.get_child() if run_manager else None,
                    **tool_run_kwargs,
                )
                observation = "$$PREV[{i}]".format(i=self.tool_count)
               
                #==============================================================================================================
                tool_schema = {                        
                    'tool_name': tool.name,
                    'arguments': arguments,
                }

                if self.train_mode :
                    print("\033[1;35;40m {} \033[0m".format('Checking Argument Correctness... (agent_executor)'))
                    response, correct_arguments = build_tool_experience(self.ground_truth, self.return_schema+[tool_schema])
                    if response is False:
                        tool_schema["arguments"] = correct_arguments

                self.return_schema.append(tool_schema)

                #==============================================================================================================

            else:
                tool_run_kwargs = self.agent.tool_run_logging_kwargs()
                observation = InvalidTool().run(
                    {
                        "requested_tool_name": agent_action.tool,
                        "available_tool_names": list(name_to_tool_map.keys()),
                    },
                    verbose=self.verbose,
                    color=None,
                    callbacks=run_manager.get_child() if run_manager else None,
                    **tool_run_kwargs,
                )
            result.append((agent_action, observation))
        return result
    
    def reset_mistakes(self):
        pass
    
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser

#____________________________________________________________________________________________________
agent_obj = PersonalAgent.from_llm_and_tools(
            llm = llm, tools = task_tools, output_parser=ReActSingleInputOutputParser()
            )
agent_executor = CustomAgentExecutor(
                                agent=agent_obj ,
                                tools=task_tools,
                                verbose=True,
                                return_intermediate_steps=True,
                                handle_parsing_errors=True,
                                )


#____________________________________________________________________________________________________

ground = '''
[ 
 { 
 "tool_name":  "search_object_by_name", 
 "arguments":  [ 
 { 
 "argument_name":  "query", 
 "argument_value":  "UltimateCustomer" 
 } 
] 
 }, 
 { 
 "tool_name":  "works_list", 
 "arguments":  [ 
 { 
 "argument_name":  "ticket.rev_org", 
 "argument_value":  "$$PREV[0]" 
 } 
 ] 
 }, 
 { 
 "tool_name":  "summarize_objects", 
 "arguments":  [ 
 { 
 "argument_name":  "objects", 
 "argument_value":  "$$PREV[1]" 
 } 
 ] 
 } 
 ]
'''
# from langchain.callbacks import get_openai_callback

# "For customer 'CustomerA', summarize all high-severity issues and check if similar issues exist in other parts."
# agent_executor.eval()
# agent_executor.get_tool_lists(ground)
# with get_openai_callback() as cb:

#     x = agent_executor({"input":'Prioritize my P0 issues and add them to the current sprint'})
#     print(x)
#     print('\n\n\n\n\n\n\n\n' , agent_executor.return_schema)

#     print('\n\n\n\n\n' ,cb.total_cost)


