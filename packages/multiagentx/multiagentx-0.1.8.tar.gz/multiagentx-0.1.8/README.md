# MultiAgentX

A flexible framework for building multi-agent systems.

## Installation


### Install from pypi

You can install the package from pypi

```bash
pip install multiagentx -i https://pypi.org/simple
```

You can also upgrade the package from pypi

```bash
pip install multiagentx --upgrade -i https://pypi.org/simple
```

### Install from source

You can also install the package directly from source:

```bash
pip install .
```

For development installation:

```bash
pip install -e .
```


## Usage

Comprehensive examples can be located in the [Examples](https://github.com/ZJCODE/multiagentx/tree/main/examples) section.

### Step Zero

```python
from dotenv import load_dotenv
from openai import OpenAI
from multiagentx import Env,Agent,Group

load_dotenv()
# model_client used for creating Openai agent or Group internal processing
model_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL"),
)

```

### Step One

> Agent is the basic unit of the framework, it can build from scratch or connect to third-party agents

Creat Agent like this 

```python
artist = Agent(name="artist",
        role="Artist", 
        description="Transfer to me if you need help with art.",
        persona = "You are a professional artist who has been working in the industry for over 10 years. You have a deep understanding of art history and have a strong passion for creating art. You are known for your unique style and innovative approach to art. You are always looking for new ways to express yourself and push the boundaries of what is possible in the art world.",
        model_client=model_client,
        verbose=True)
```

can use agent like this

```python
response = artist.do("Can you help me with art?",model="gpt-4o-mini")
```

can add tools like this

```python

def web_search(qury:str)->str:
    """
    web search tool
    """
    # do web search
    return "web search result"

researcher = Agent(name="researcher",
        role="Researcher",
        description="Transfer to me if you need help with research.",
        persona = "You are a professional researcher who can do web search to conduct research on a wide range of topics. You have a deep understanding of how to find and evaluate information from a variety of sources. You are known for your ability to quickly find relevant information and present it in a clear and concise manner.",
        tools=[web_search],
        model_client=model_client,
        verbose=True)
```

or equip with memory like this

```python
telos = Agent(name="telos",
              role="Assistant",
              description="Transfer to me if you need help with general questions.",
              persona="You are a general assistant who can help with a wide range of questions. You have a deep understanding of a variety of topics and can provide information and assistance on a wide range of subjects. You are known for your ability to quickly find answers to questions and provide helpful information in a clear and concise manner.",
              model_client=model_client,
              verbose=True)

telos.init_memory(working_memory_threshold=3)
```

or connect a third-party agent that was created at Dify like this.

```python
mathematician = Agent(name="mathematician",
    role="Mathematician", 
    description="Transfer to me if you need help with math.", 
    dify_access_token="app-rlK8IzzWCVkNbkxxxxxxx",
    verbose=True)
# persona is not needed for Dify agent, it already has its own persona
```

or connect a url iagent like this

```python

iAgent = Agent(name="Tim",
               role="Designer",
               description="Transfer to me if you need help with art and design.",
               iagent_url="http://127.0.0.1:7860/v1/chat",
               verbose=True)

iAgent.do(message="Hey,who are you?",sender="Jun")

```

### Step Two

> Env is the environment where agents live, you can add a description and agents to the environment. In addition,it can be created with or without relationships between agents, and can also set the language used in the environment. Env will be used to create a group of agents.

Create Env like this (all agents are fully connected by default)

```python

env = Env(
    description="This is a test environment",
    members=[mathematician, artist]
)
```

or like this (self-defined topology relationships between agents)

```python
env = Env(
    description="This is a test environment",
    members=[mathematician, artist],
    relationships={"agent1": ["agent2"]}
)
```

or set language used in the environment

```python
env = Env(
    description="This is a test environment",
    members=[mathematician, artist],
    language="中文"
)
```


### Step Three

> Group is a collection of agents that can be used to chat, perform tasks, and handle basic control with a human in the loop.

Build Group like this

```python
g = Group(env=env,model_client=model_client,verbose=True)
```

can add extra agent into group dynamically like this

```python

designer = Agent(name="designer",
    role="Designer", 
    description="Transfer to me if you need help with design.", 
    model_client=OpenAI(),
    verbose=True)

g.add_member(designer)
```

or delete agent from group dynamically like this 

```python
takeaway,observed_speakers = g.delete_member("artist") # delete by name
# will return takeaway and observed_speakers for memory retrieval in the future
```

or invite agent to join group dynamically like this

```python
# automatically create agent
g.invite_member("a philosopher who calls himself agent4 , he is a big fan of plato and aristotle")
```

or dismiss the group like this

```python
g.dismiss_group()
# when the group is dismissed, all agents will be deleted and each of them will get their own memory back
```

### Step Four

> Some examples of how to use the group

chat with group of agents(dynamic agent selection)

```python
# build a group with agent like mathematician, artist,resercher etc then do chat with them
response= g.chat("Can you explain the concept of complex numbers?",model="gpt-4o-mini")
response= g.chat("Can you help me with art?",model="gpt-4o-mini")
```

internal dialogue within group of agents based on the current environment description

```python
# build a group with agent like some friends, then let them chat with each other
g.dialogue(model="gpt-4o-mini",max_turns=10)
```

task for group of agents

```python
# build a group with agent like product manager, designer, engineer etc then let them work together to complete a task
response = g.task("I want to build a simplistic and user-friendly bicycle help write a design brief.",model="gpt-4o-mini",strategy="auto")
```

low-level API example

```python
g.user_input("can you help me with math?")
next_agent = g.handoff(next_speaker_select_mode="auto",include_current=True,model="gpt-4o-mini")
```

```python
g.user_input("Discuss the concept of abstract art.")
response = g.call_agent(next_speaker_select_mode="auto",include_current=True,model="gpt-4o-mini")
response = g.call_agent(next_speaker_select_mode="auto",include_current=True,model="gpt-4o-mini")
g.user_input("how do you feel about abstract art?")
response = g.call_agent(next_speaker_select_mode="auto",include_current=True,model="gpt-4o-mini")
response = g.call_agent(next_speaker_select_mode="auto",include_current=True,model="gpt-4o-mini")
response = g.call_agent(next_speaker_select_mode="auto",include_current=True,model="gpt-4o-mini")
```




## Package Upload

First time upload

```bash
pip install build twine
python -m build
twine upload dist/*
```

Subsequent uploads

```bash
rm -rf dist/ build/ *.egg-info/
python -m build
twine upload dist/*
```


