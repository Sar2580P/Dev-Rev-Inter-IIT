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
$ tree <task>/<version>
<task>/<version>/
├── agent
│   ├── 0_0.txt
│   ├── 1_0.txt
│   ├── ...
│   ├── 8_0.txt
│   └── 9_0.txt
├── agent_executor
│   ├── search
│   ├── select_home_type
│   ├── ...
│   ├── set_num_garages
│   └── set_num_swimming_pools
└── test.jsonl
├── backend_llm
├── tools
```
