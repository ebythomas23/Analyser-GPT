import streamlit as st

import asyncio
import os

from teams.analyzer_gpt import getDataAnalyzerTeam
from config.docker_util import getDockerCommandLineExecutor, start_docker_container, stop_docker_container
from models.openai_model_client import get_model_client
from autogen_agentchat.messages import TextMessage

st.title("Analyser-GPT : Digital Data Analyst")




uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])

async def run_analyser_gpt(task, docker ,model_client):
    try:
        await start_docker_container(docker)
        team = getDataAnalyzerTeam(docker, model_client)

        async for message in team.run_stream(task=task):
            st.markdown(f"**{message}")

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
          
    else:
        st.warning("Please upload the file first")

else:
        st.warning("Please provide the task")