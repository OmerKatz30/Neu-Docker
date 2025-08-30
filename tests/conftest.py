import pytest
import docker
import requests
import time
from docker.errors import ImageNotFound, DockerException

CONTAINER_IMAGE_NAME = "test-app:latest"


@pytest.fixture(scope="session")
def app_container():
    try:
        client = docker.from_env()
        # Check if Docker daemon is running
        client.ping()
    except (DockerException, requests.exceptions.ConnectionError) as e:
        pytest.fail(f"Docker daemon not running. Please start Docker Desktop. Error: {e}")

    container = None
    try:
        print("\nForcing a fresh Docker image build...")
        try:
            client.images.remove(image=CONTAINER_IMAGE_NAME, force=True)
        except ImageNotFound:
            pass

        # Build the Docker image
        client.images.build(path=".", tag=CONTAINER_IMAGE_NAME, rm=True, nocache=True)

        # Start the container
        print("Starting container...")
        container = client.containers.run(
            CONTAINER_IMAGE_NAME,
            detach=True,
            ports={'5000/tcp': 5000}
        )

        # Wait for the app to be ready
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f"http://localhost:5000/reverse?in=ping", timeout=1)
                if response.status_code == 200:
                    print("Container is ready.")
                    break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        else:
            print("Container failed to start or become ready within the timeout.")
            print("Container logs:")
            print(container.logs().decode('utf-8'))
            pytest.fail("Container failed to start")

        yield container

    finally:
        if container:
            print("Stopping and removing container...")
            container.stop(timeout=5)
            container.remove(v=True, force=True)


@pytest.fixture
def client():
    """Configures the app for testing and provides a test client."""
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client