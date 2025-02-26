import docker
import logging

logger = logging.getLogger(__name__)


class DockerImageRun:
    def __init__(self, image, ports):
        self.image = image
        self.ports = ports
        self.container = None
        try:
            self.client = docker.from_env()
        except Exception as e:
            logger.error('IS DOCKER RUNNING???')
            raise

    def __enter__(self):
        # Try to pull the image if it's not present
        try:
            self.client.images.get(self.image)
        except docker.errors.ImageNotFound:
            print('Image not found locally. Pulling from Docker Hub...')
            self.client.images.pull(self.image)

        # Start the container
        print(f'Starting container for image [{self.image}]...')
        self.container = self.client.containers.run(self.image, detach=True, ports=self.ports)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'Stopping container for image [{self.image}]...')
        self.container.stop()