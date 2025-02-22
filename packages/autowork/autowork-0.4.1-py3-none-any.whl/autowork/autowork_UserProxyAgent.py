#from autogen_agentchat.agents import UserProxyAgent

""" from autogen_agentchat.agents import UserProxyAgent

class CustomUserProxyAgent(UserProxyAgent):
    def __init__(self, name="user", input_func=input):
        super().__init__(name=name)
        self.input_func = input_func

    async def on_input(self, prompt: str) -> str:
        user_input = input(prompt)
        if user_input.strip().lower() == 'q':
            print("Exiting the program.")
            raise SystemExit
        return user_input
"""
from autogen_agentchat.agents import UserProxyAgent

class CustomUserProxyAgent(UserProxyAgent):
    def __init__(self, name="user", description=None, input_func=input):
        super().__init__(name=name, description=description, input_func=input_func)
        self.input_func = input_func

    async def on_input(self, prompt: str) -> str:
        user_input = self.input_func(prompt)
        if user_input.strip().lower() == 'q':
            print("Exiting the program.")
            raise SystemExit
        return user_input


#user_proxy = UserProxyAgent(name = "user_proxy", input_func=input,
#                            description="An agent that can represent a human user through an input function.",
#                            )
        
user_proxy = CustomUserProxyAgent(name = "user_proxy", input_func=input,
                description="An agent that can represent a human user through an input function.",
)
 