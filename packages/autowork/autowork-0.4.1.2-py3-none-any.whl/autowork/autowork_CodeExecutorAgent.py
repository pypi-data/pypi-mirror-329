from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from pathlib import Path

work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)
code_executor = CodeExecutorAgent(
    name="code_executor",
    description="Run it automatically.",
    code_executor=LocalCommandLineCodeExecutor(work_dir=work_dir),
)
