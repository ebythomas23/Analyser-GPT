
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constants import WORK_DIR_DOCKER,TIMEOUT_DOCKER



def getDockerCommandLineExecutor():
    docker = DockerCommandLineCodeExecutor(
        image="amancevice/pandas",
        work_dir= WORK_DIR_DOCKER,
        timeout= TIMEOUT_DOCKER
    )

    return docker


async def start_docker_container(docker):
    print("Starting docker container")
    await docker.start()
    print("Docker container started")


async def stop_docker_container(docker):
    print("Stopping docker container") 
    await docker.stop()
    print("Docker container stopped" )        