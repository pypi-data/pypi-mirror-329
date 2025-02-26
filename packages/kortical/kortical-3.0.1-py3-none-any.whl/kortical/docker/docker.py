import os

from kortical import api
from kortical.docker import image_helpers
from kortical.helpers.print_helpers import print_info, print_error


def build(image_name, app_directory=None, plain_text=False):
    if app_directory is None:
        app_directory = os.getcwd()

    dockerfile_path = os.path.join(app_directory, "docker", image_name, "Dockerfile")
    if not os.path.isfile(dockerfile_path):
        print_error(f'Image [{app_directory}/docker/{image_name}/Dockerfile] was not found.')
        return

    image_helpers.build(image_name, dockerfile_path, app_directory, plain_text=plain_text)


def push(image_name, app_directory=None):
    if app_directory is None:
        app_directory = os.getcwd()

    # Push docker
    print_info(f'Pushing image [{image_name}] to Kortical Cloud...')
    tag_name = image_helpers.push(image_name)
    print_info(f'Created tag {tag_name}')

    # Check and update reference to updated docker in files from k8s/docker folders.
    file_paths = []
    for (dirpath, _, filenames) in os.walk(f"{app_directory}/k8s"):
        file_paths += [os.path.join(dirpath, file) for file in filenames]
    for (dirpath, _, filenames) in os.walk(f"{app_directory}/docker"):
        file_paths += [os.path.join(dirpath, file) for file in filenames]

    image_helpers.update_image_version_in_files(tag_name, file_paths)

    return tag_name


def build_push(image_names, app_directory=None, plain_text=False):
    if app_directory is None:
        app_directory = os.getcwd()

    if type(image_names) == str:
        image_names = [image_names]

    for image_name in image_names:
        build(image_name, app_directory, plain_text=plain_text)
        push(image_name, app_directory)


def list_images(show_tags):
    request_data = {'show_tags': show_tags}
    print_info(f'Getting image list from Kortical container repository{" with tags..." if show_tags else "..."}')
    response = api.get('/api/v1/docker/images', params=request_data)

    return {'images': response.json()}


def get_container_repo():
    response = api.get('/api/v1/docker/container_registry')
    return response.text


def get_local_images(app_directory=None):
    if app_directory is None:
        app_directory = os.getcwd()

    images = []
    docker_directory = os.path.join(app_directory, 'docker')
    if os.path.exists(docker_directory):
        images = os.listdir(docker_directory)
    return images
