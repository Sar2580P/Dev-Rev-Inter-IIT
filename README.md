## Dev-Rev-Inter-IIT (Team-72)

Problem Statement : 
A Language model L has a set of tools T, and a user query Q is given. To answer query Q, we 
 need to use existing tools. You need to output the subset of tools to be used to answer the 
 query, the arguments that these tools should be called with, and how to compose the tools to 
 answer the query. The query is conversational, like so 
```

Unset 
 user_message: "Hello!" 
 agent_message: "Hello, how can I help you today?" 
 user_message: "Can you tell me my P0 issues?", 
 agent_message: "Sure, here is the list... ", 
 user_message: "Okay, can you change this list to show only those that are 
 in triage stage?", 
 agent_message: "Sure, this is the updated list ... ",
```

## Prerequisites
Credentials
* Create an OpenAI account and register an API key.

## Repository Structure:
```
$ tree <task>
<task>
├── agent
│   ├── agent.py
│   ├── mistakes_selection.py
│   ├── tool_collection.py
│   
├── agent_executor
│   ├── agent_executer.py
│   ├── agent_memory.py
│   ├── auxiliary_executor.py
│  
├── backend_llm
│   ├── evaluator.py
│   ├── memory.py
│   ├── utils.py
│
├── tools
│   ├── argument_mapping ├──├──├──├──├──├──├──├── tool_memory.py
│   ├── add_work_items_to_sprint.py           ├── get_args.py
│   ├── create_actionable_tasks_from_text.py
│   ├── get_similar_work_items.py
│   ├── get_sprint_id.py
│   ├── logic_tool.py
│   ├── prioritize_objects.py
│   ├── search_object_by_name.py
│   ├── summarize_objects.py
│   ├── who_am_i.py
│   ├── work_list.py
│
├── train_analysis 
│   ├── predict.py
│   ├── train.py
│
├── main.py
├── prompts.py
├── requirements.txt
```
* *agent.py* : to manipulate the prompt passed to LLM reasoning Agent by attaching it with past mistakes committed by LLM in tool selection.
* *mistakes_selection.py* : Putting a filter over past mistakes after searching from mistake vectore-db, by asking LLM to check its relevency wrt current user query.
* *tool_collection.py* : Storing all tools for access to AI agent.
* *agent_executor.py* : Tracks all reasoning from AI agent and responses from tools used by AI agent, maintains and returns the final output JSON schema.
* *agent_memory.py* : Staging and pushing mistakes commited by AI agent in tool picking on past user queries.
* *predict.py* : The file to predict output JSON on user queries.
* *train.py* : For building the experience of AI agent, on the mistakes it commits while tool selection for sub-tasks.
* *prompts.py* : All the prompting used for guiding LLM at various agents.
* *utils.py* : Initializes OpenAI text and embedding model.
* *evaluator* : Keeps a programmatic, non-LLM check whether AI agent selects correct tool using the ground json by observing the topological structural similarity of AI generated with ground JSON

## Getting Started : 
``` pip install -r requirements.txt
* Create a .env file and store the api keys there.
* to create a local host, main.py is provided.
* create a vectore store to store the mistakes of AI agent, while running on personal queries.

```

## HOW TO ADD NEW TOOL : 
* To add new tool to the setup, run add_tool.py
* Provide all the necessary info, it asks while running.
* Add the tool to tools_collection.py as other tools are added.

## SETUP:
The setup can be run in 2 modes:
 * Train mode
 * Eval Mode

### Train Mode :
* The query runs, if it makes some mistake, you can decide whether to save that experience in vectore_db or not
* Just visit train.py , where you can build your experience in rl-setup

### Eval Mode : 
* Just run predict.py on user queries
* The past mistake memory is added to agent prompt to help it assist in avoiding similar mistakes again.
  

##
