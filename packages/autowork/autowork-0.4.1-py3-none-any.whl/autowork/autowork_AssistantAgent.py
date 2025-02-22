from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autowork_ModelClient import model_client



# assistant_my = AssistantAgent("assistant", model_client=model_client)

assistant = AssistantAgent(name="assistant_agent", 
                    model_client=model_client,
                    tools=[],
                    handoffs=[],
                    description="An agent that provides assistance with ability to use tools.",
                    system_message='''
                    You are a helpful assistant. Solve tasks carefully. 
                    If the output has code, just give one block of code. 
                    Do not give me multiple suggestions. When done, say TERMINATE.
                    ''',
                    model_client_stream=True)

# something is missing:
# 