import asyncio

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat


from autowork_ModelClient import model_client
from autowork_AssistantAgent import assistant
from autowork_UserProxyAgent import user_proxy
from autowork_CodeExecutorAgent import code_executor
from autowork_Termination import termination


# team = RoundRobinGroupChat([assistant, user_proxy, code_executor], termination_condition=termination)

team = SelectorGroupChat([assistant, user_proxy, code_executor], 
                         termination_condition=termination,
                         model_client=model_client,
                         allow_repeated_speaker=False,
                         selector_prompt="""You are in a role play game. The following roles are available:
{roles}.
Read the following conversation. Then select the next role from {participants} to play. Only return the role.

{history}

Read the above conversation. Then select the next role from {participants} to play. Only return the role. 
At the beginning of the task, always starts from assistant and not from code_executor or user_proxy.
""")



stream = team.run_stream(task=input("Hello! I am your Assistant. How could I help you?\n"))


# Use asyncio.run(...) when running in a script.
# await Console(stream)

asyncio.run(Console(stream, output_stats=True))
