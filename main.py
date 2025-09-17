import asyncio
from teams.analyzer_gpt import getDataAnalyzerTeam
from config.docker_util import getDockerCommandLineExecutor, start_docker_container, stop_docker_container
from models.openai_model_client import get_model_client
from autogen_agentchat.messages import TextMessage


async def main():
    docker = getDockerCommandLineExecutor()
    model_client = get_model_client()

    team = getDataAnalyzerTeam(docker, model_client)

    try: 
        task ="can you give me a graph of types of flowers in Iris.csv "

        await start_docker_container(docker)

        async  for message in team.run_stream(task= task):
            print(message)

    except Exception as e:
        print(e)

    finally:
        await start_docker_container(docker)            



if __name__ == "__main__":
     asyncio.run(main())
