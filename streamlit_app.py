import streamlit as st

import asyncio
import os

from teams.analyzer_gpt import getDataAnalyzerTeam
from config.docker_util import getDockerCommandLineExecutor, start_docker_container, stop_docker_container
from models.openai_model_client import get_model_client
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.title("Analyser-GPT : Digital Data Analyst")




uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state= None  

async def run_analyser_gpt(task, docker ,model_client):
    try:
        await start_docker_container(docker)
        team = getDataAnalyzerTeam(docker, model_client)

        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)

        async for message in team.run_stream(task=task):
            if isinstance(message,TextMessage):
                if message.source.startswith('user'):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(message.content)
                elif message.source.startswith('DataAnalyzerAgent'):
                    with st.chat_message('Data Analyzer Agent',avatar='🤖'):
                        st.markdown(message.content)
                elif message.source.startswith('CodeExecutorAgent'):
                    with st.chat_message('Code Executor Agent',avatar='👨🏻‍💻'):
                        st.markdown(message.content)
               
                st.session_state.messages.append(message.content)

            elif isinstance(message,TaskResult):
                st.markdown(f"Stop Reason: {message.stop_reason}")
                st.session_state.messages.append(message.stop_reason)
        
        st.session_state.autogen_team_state = await team.save_state()

        return None    

    except Exception as e:
        st.error(f"Error: {e}") 
        return e

    finally:
        await stop_docker_container(docker)


task = st.chat_input("Enter your task here...")

if task :
    if uploaded_file is not None :
        
        if not os.path.exists('temp'):
            os.makedirs('temp')

        with open('temp/data.csv','wb') as f:
            f.write(uploaded_file.getbuffer())

        model_client = get_model_client()
        docker = getDockerCommandLineExecutor()

        error = asyncio.run(run_analyser_gpt(task, docker, model_client))

        if error:
            st.error(f"An error occured: {error}")

        # # see all the *.png in temp and show them on streamlit app
        # png_files = [f for f in os.listdir('temp') if f.endswith('.png')]
        # if png_files:
        #     for png_file in png_files:
        #         st.image(os.path.join('temp', png_file), caption=png_file)    

        if os.path.exists('temp/output.png'):
            st.image('temp/output.png', caption='Output Image')    
          
    else:
        st.warning("Please upload the file first")

else:
        st.warning("Please provide the task")