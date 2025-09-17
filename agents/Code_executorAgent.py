from autogen_agentchat.agents import CodeExecutorAgent

def getCodeExecutorAgent(code_executor):
   
   code_executor_Agent = CodeExecutorAgent(
    name= 'CodeExecutorAgent',
    code_executor =code_executor)

   return code_executor_Agent 

