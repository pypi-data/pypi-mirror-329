from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination


#text_termination = TextMentionTermination("TERMINATE")
text_termination = TextMentionTermination("APPROVE")
#text_termination2 = TextMentionTermination("q") # not working
max_msg_termination = MaxMessageTermination(max_messages=100)
termination = max_msg_termination | text_termination
