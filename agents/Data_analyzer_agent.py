from autogen_agentchat.agents import AssitantAgent
from prompts.data_analyzer_message import DATA_ANALYSER_SYSTEM_MESSAGE

def getDataAnalyzerAgent(model_client):
    data_analyzer_agent = AssitantAgent(
        name ='Data_Analyzer_agent',
        model_client= model_client,
        description = " an agent that solves Data analysis problem and give the code as well",
        system_message=DATA_ANALYSER_SYSTEM_MESSAGE     
    )
    return data_analyzer_agent
