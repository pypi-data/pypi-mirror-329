import os

from kortical.docker import docker
from kortical.cli._cmd_registry import command
from kortical.helpers.print_helpers import print_info


@command('docker')
def command_docker(args):
    """
Controls building and pushing of images to your Kortical Cloud container registry. These commands should be run at the root of an app folder.

usage:
    kortical docker [-h]
    kortical docker get-registry
    kortical docker list-images [--show-versions]
    kortical docker build <image-name> [--plain-text]
    kortical docker push <image-name>
    kortical docker build-push <image-name> [--plain-text]


options:
    -h, --help         Display help.
    <image-name>       Name of the image you want to build/push.
    --show-versions    Returns the latest version numbers of your container registry images.
    --plain-text       Returns plain text output. Good for CI/CD.

commands:
    list-images        Returns a list of Docker images in your container registry.
    build              Builds a Docker image; needs to be run from the root of an app's repository,
                       and requires the path [<app-directory>/docker/<image-name>/Dockerfile].
    push               Pushes a locally built Docker image.
    build-push         Builds and pushes an image (i.e combines the two above commands).

    """

    app_directory = os.getcwd()

    if args['get-registry']:
        container_registry = docker.get_container_repo()
        print_info(container_registry)

    elif args['list-images']:
        images = docker.list_images(args['--show-versions'])

        if args['--show-versions']:
            for image_name, versions in images['images'].items():
                print(f"{image_name}: {max(versions)}")
        else:
            print("\n".join(images['images']['image_names']))

    elif args['build']:
        if args['--plain-text']:
            plain_text = True
        else:
            plain_text = False
        docker.build(args['<image-name>'], app_directory, plain_text=plain_text)

    elif args['push']:
        docker.push(args['<image-name>'], app_directory)

    elif args['build-push']:
        if args['--plain-text']:
            plain_text = True
        else:
            plain_text = False
        docker.build_push(args['<image-name>'], app_directory, plain_text=plain_text)
