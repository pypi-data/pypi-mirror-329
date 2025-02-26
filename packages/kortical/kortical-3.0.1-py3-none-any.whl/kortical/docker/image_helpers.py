import os
import re
import subprocess
import time
from packaging import version
from pathlib import Path
import platform
from tempfile import gettempdir
from uuid import uuid4
import tarfile
import hashlib

import requests
from multiprocessing import Pool, Manager
from ctypes import c_wchar_p
import zlib
import yaml
import json

from kortical import api
from kortical.helpers.console import Console
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_info, print_success, print_error
from kortical.helpers.run_cmd import run_cmd

MINIMUM_DOCKER_VERSION = '19.03.1'
MAXIMUM_DOCKER_VERSION_TESTED = '27.4.0'
# if using the containerd image-store ( Storage Driver: overlayfs), we don't need to use compression and in fact it will break if we do
CONTAINERD_BACKEND_NO_COMPRESSION_NEEDED = 'overlayfs'


def get_docker_storage_driver():
    try:
        # Run the 'docker info' command
        result = subprocess.run(["docker", "info"], capture_output=True, text=True, check=True)

        # Search for the Storage Driver line
        match = re.search(r"Storage Driver:\s+(\S+)", result.stdout)

        if match:
            return match.group(1)
        else:
            raise KorticalKnownException("Storage Driver not found when running [docker info]")

    except subprocess.CalledProcessError as e:
        raise KorticalKnownException(f"Error executing Docker command: {e}")

    except FileNotFoundError:
        raise KorticalKnownException("Docker is not installed or not in PATH")


def _should_use_compression():
    """
    Determines if compression should be used based on Docker storage driver
    """
    storage_driver = get_docker_storage_driver()

    if storage_driver != CONTAINERD_BACKEND_NO_COMPRESSION_NEEDED:
        return True
    return False


# Windows doesn't enable buildkit with an inline environment variable
BUILDKIT_ENABLED = False if platform.system() == 'Windows' else True


def _get_formatted_layer_size(size):
    units = [("GB", 1000000000), ("MB", 1000000), ("kB", 1000), ("bytes", 1)]
    for unit_name, unit_value in units:
        if size >= unit_value:
            return f"{size / unit_value:.2f} {unit_name}"
    return f"{size} bytes"


def _get_formatted_time(seconds):
    units = [("days", 86400), ("hours", 3600), ("minutes", 60)]

    output = []
    leftover_seconds = seconds

    for unit_name, unit_value in units:
        if leftover_seconds >= unit_value:
            output.append(f"{int(leftover_seconds / unit_value)} {unit_name}")
            leftover_seconds = leftover_seconds % unit_value

    output.append(f"{leftover_seconds:.2f} seconds")

    formatted_time = ', '.join(output)
    return formatted_time


def get_image_names_from_k8(k8_path):
    def get_image_names_from_config(conf):
        containers = conf['spec']['template']['spec']['containers']
        image_names = []
        for container in containers:
            fully_qualified_image_name = container['image']
            image_with_version = fully_qualified_image_name.split('/')[-1]
            image_name = image_with_version[:image_with_version.index(':')]
            image_names.append(image_name)
        return list(set(image_names))

    with open(k8_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            return get_image_names_from_config(config)
        except yaml.composer.ComposerError:
            f.seek(0)
            k8_configs = yaml.safe_load_all(f)
            config = next(config for config in k8_configs if config.get('kind') == 'StatefulSet')
            return get_image_names_from_config(config)
        except:
            raise KorticalKnownException(f'Could not parse k8 config {k8_path} for deployment.')


def build(image_name, dockerfile_path, app_directory, plain_text=False):
    docker_version_str = None
    docker_version_parsed = None

    try:
        # On Windows this command can return new line chars and inside quotes so strip these out.
        docker_version_str = run_cmd("docker version --format '{{.Server.Version}}'").strip("\n").strip("'")

        if docker_version_str:
            # sometimes we have suffixes to the version string which 'version' module can't parse, so need to remove them
            docker_version_parsed = version.parse(re.sub(r'[a-zA-Z\-]', '', docker_version_str))

            # Check min version
            if docker_version_parsed < version.parse(MINIMUM_DOCKER_VERSION):
                raise KorticalKnownException(
                    f"This tool requires Docker version {MINIMUM_DOCKER_VERSION} or higher, "
                    f"found {docker_version_str}."
                )
        else:
            # We didn't detect any Docker version
            raise KorticalKnownException(
                f"Docker error. Please ensure your Docker installation is at least version "
                f"{MINIMUM_DOCKER_VERSION}, but we did not detect any Docker version installed."
            )
    except Exception:
        # If we fail to parse or run Docker, let’s raise a known exception
        raise KorticalKnownException(
            f"Docker error. Please ensure your Docker installation is at least "
            f"version {MINIMUM_DOCKER_VERSION}. Detected: {docker_version_str or 'None'}"
        )

    # Construct the Docker build command
    build_command = (
        "docker build "
        f"{'--ssh default ' if BUILDKIT_ENABLED else ''}"
        f"{'--progress=plain ' if plain_text else ''}"
        f"--platform=linux/amd64 "
        f"-t {image_name} "
        f"-f \"{dockerfile_path}\" "
        f"\"{app_directory}\""
    )

    print_info(f"Starting Docker build for {image_name}...")
    start_time = time.time()
    if not plain_text:
        if BUILDKIT_ENABLED:
            build_command = f"DOCKER_BUILDKIT=1 {build_command}"
        return_code = os.system(build_command)
    else:
        environment_variables = {"DOCKER_BUILDKIT": "1"} if BUILDKIT_ENABLED else None
        with Console.run(build_command, environment_variables=environment_variables) as console:
            return_code = console.wait_for_exit()
    end_time = time.time()

    if return_code != 0:
        # Build a more explicit error message
        # We'll note if we’re above our tested max version or if Docker wasn’t found.
        # (We won’t *fail* if above the max—just let the user know it’s untested.)

        # Base error message:
        error_message = (
            "ERROR: Docker build command failed. Check the docker output for errors but please also ensure "
            f"you have at least version {MINIMUM_DOCKER_VERSION} of Docker. "
            f"We've tested it works with up to Docker version {MAXIMUM_DOCKER_VERSION_TESTED}, "
        )

        if docker_version_parsed:
            if docker_version_parsed > version.parse(MAXIMUM_DOCKER_VERSION_TESTED):
                # Docker is newer than our tested version
                error_message += (
                    f"where you are running Docker version {docker_version_str} (untested newer version). "
                )
            else:
                # Docker is within or below our tested version range
                error_message += f"where you are running Docker version {docker_version_str}. "
        else:
            # We couldn’t parse or detect Docker version at all
            error_message += (
                "we did not detect any Docker version installed. "
            )

        # Add instructions for checking root directory, etc.
        error_message += (
            "Please also check you are in the root directory of the app when running this command."
        )

        print_error(error_message)
        raise Exception(f"Docker build terminated unexpectedly. Return code {return_code}")

    time_elapsed = _get_formatted_time(end_time - start_time)
    print_success(f"Completed Docker build in {time_elapsed}.")


def _threaded_request(method, url, project_url, cookie_shared_value, login_lock, *args, **kwargs):
    """Request and thread safe login handling."""
    kwargs["headers"] = kwargs.get("headers", {})
    kwargs["headers"]["Cookie"] = cookie_shared_value.value
    failed = False
    retries = 3
    while True or retries > 0:
        response = None
        with login_lock:
            if kwargs['headers']['Cookie'] == cookie_shared_value.value and failed:
                print_error(f"Retrying as user has been logged out.")
                api.init()
                api_response = api.get('')
                cookie_shared_value.set(api_response.request.headers['Cookie'])
                kwargs['headers']['Cookie'] = cookie_shared_value.value
            elif kwargs['headers']['Cookie'] != cookie_shared_value.value:
                kwargs['headers']['Cookie'] = cookie_shared_value.value

        try:
            response = requests.request(method=method, url=project_url + url, *args, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            retries -= 1
            if retries <= 0:
                raise e
            print_error(f"Retrying due to connection drop")
            time.sleep(1)
        if response is None or response.status_code == 401:
            failed = True
        elif response.status_code not in [200, 201, 202, 204, 404]:
            raise Exception(f"Request [{url}] failed with status code [{response.status_code}]\n\n{response.content.decode()}")
        else:
            return response


def _threaded_head(url, cookie_shared_value, project_url, login_lock, *args, **kwargs):
    """Make authenticated head requests in a thread safe manner."""
    return _threaded_request("head", url, project_url, cookie_shared_value, login_lock, *args, **kwargs)


def _threaded_put(url, cookie_shared_value, project_url, login_lock, *args, **kwargs):
    """Make authenticated put requests in a thread safe manner."""
    return _threaded_request("put", url, project_url, cookie_shared_value, login_lock, *args, **kwargs)


def _send_layer(image_name, layer_tar, docker_upload_uuid, project_url, cookie_shared_value, login_lock):
    """Upload a layer to the registry with conditional compression.

    Args:
        image_name: Name of the Docker image
        layer_tar: The raw tar layer data
        docker_upload_uuid: UUID for the upload session
        project_url: Base URL for the project
        cookie_shared_value: Shared cookie value for authentication
        login_lock: Lock for thread-safe login handling

    Returns:
        dict: Information about the uploaded layer including digest and size
    """
    layer_tar_size = len(layer_tar)
    digest = hashlib.sha256(layer_tar).hexdigest()

    # Check if the layer was previously uploaded
    head_response = _threaded_head(
        url=f"/api/v1/docker/images/{image_name}/blobs/sha256:{digest}",
        project_url=project_url,
        cookie_shared_value=cookie_shared_value,
        login_lock=login_lock
    )

    if head_response.status_code == 200:
        print_info(f'Layer {digest} already pushed.')
        return {"digest": f"sha256:{digest}", "size": layer_tar_size, "sent": True}

    headers = {
        'Content-Type': 'application/octet-stream'
    }

    if _should_use_compression():
        print_info(f'Compressing layer {digest}...')
        start_time = time.time()
        compressor = zlib.compressobj(level=zlib.Z_BEST_COMPRESSION, wbits=31)
        compressed_layer_tar = compressor.compress(layer_tar) + compressor.flush()
        compression_time = time.time() - start_time
        new_layer_tar_size = len(compressed_layer_tar)
        print_success(
            f'Layer {digest} compression done in {_get_formatted_time(compression_time)} '
            f'to {_get_formatted_layer_size(new_layer_tar_size)}, '
            f'{str(round((new_layer_tar_size / layer_tar_size) * 100, 2))}% original size.'
        )

        headers['Content-Encoding'] = 'gzip'
        layer_data = compressed_layer_tar
    else:
        layer_data = layer_tar

    push_start_time = time.time()

    try:
        print_info(f'Pushing layer {digest}...')
        response = _threaded_put(
            url=f"/api/v1/docker/images/{image_name}/blobs/uploads/{docker_upload_uuid}?digest=sha256:{digest}",
            data=layer_data,
            headers=headers,
            project_url=project_url,
            cookie_shared_value=cookie_shared_value,
            login_lock=login_lock,
        )

        push_time = time.time() - push_start_time
        print_success(f'Layer {digest} pushed in {_get_formatted_time(push_time)}.')
        return {"digest": f"sha256:{digest}", "size": layer_tar_size, "sent": True}
    except Exception as e:
        print_error(f"ERROR: Failed to push layer [{digest}] of image [{image_name}].")
        raise


def _send_layers(image_name, tar_file, image_layer, layers):
    """Send multiple layer to the registry"""
    # If this call fails, the backend system is most likely not up to date.
    try:
        upload_kocation_response = api.post(f"/api/v1/docker/images/{image_name}/blobs/uploads", data="")
    except Exception:
        print_error(f"ERROR: Failed to query image upload API, the platform is most likely out of date.")
        raise
    docker_upload_uuid = upload_kocation_response.headers['Docker-Upload-UUID']
    cookie = upload_kocation_response.request.headers['Cookie']
    print_info(f'{len(layers) + 1} layers to push.')
    manager = Manager()
    cookie_shared_value = manager.Value(c_wchar_p, cookie)
    login_lock = manager.Lock()
    layers.append(image_layer)
    # Generate as many processes as available, spread the uploads among them.
    with Pool() as p:
        result_layers = p.starmap(_send_layer, [(
            image_name,
            tar_file.extractfile(layer).read(),
            docker_upload_uuid,
            api.get_project_url(),
            cookie_shared_value,
            login_lock
        ) for layer in layers])
    return {"image_layer": result_layers[-1], "layers": result_layers[:-1]}


def _make_manifest(image_name: str, tag: str, upload_results):
    """
    Generate the manifest used to describe the docker image.
    Reproduces the manifest resulting of a push and pull of an image to a local repo with the following:
    docker run -d -p 127.0.0.1:5000:5000 --restart=always --name kortical_local_registry registry:2
    docker tag <image_name> 127.0.0.1:5000/<image_name>
    docker push 127.0.0.1:{port}/<image_name>
    docker pull 127.0.0.1:{port}/<image_name>
    docker manifest inspect --insecure 127.0.0.1:5000/<image_name>
     Uses appropriate media type based on compression setting.

    """
    use_compression = _should_use_compression()
    return {
        "schemaVersion": 2,
        "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
        "config": {
            "mediaType": "application/vnd.docker.container.image.v1+json",
            "size": upload_results['image_layer']['size'],
            "digest": upload_results['image_layer']['digest']
        },
        "name": image_name,
        "platform": {
            "architecture": "amd64",
            "os": "linux"
        },
        "tag": tag,
        "layers": [
            {
                "size": uploaded_layer['size'],
                "digest": uploaded_layer['digest'],
                # Use appropriate media type based on compression setting
                "mediaType": "application/vnd.oci.image.layer.v1.tar" if use_compression else "application/vnd.docker.image.rootfs.diff.tar"
            } for uploaded_layer in upload_results['layers']
        ]
    }


def push(name):
    try:
        images = run_cmd('docker images')
    except Exception:
        raise KorticalKnownException("Can't connect to docker daemon, is the docker engine running ?")
    if name not in images:
        raise KorticalKnownException(f"Image [{name}] was not found.\n"
                                     f"For a list of available images, run [docker images].")

    tar_file_path = os.path.join(gettempdir(), f'{uuid4()}.tar')
    try:
        run_cmd(f'docker save {name} > "{tar_file_path}"')
    except Exception:
        print_error(f'ERROR: Docker command to save image [{name}] failed.')
        raise

    try:
        with tarfile.open(tar_file_path) as tar_file:
            tar_manifest = json.load(tar_file.extractfile("manifest.json"))[0]
            layers = tar_manifest['Layers']
            start_time = time.time()
            upload_results = _send_layers(name, tar_file, tar_manifest['Config'], layers)
            # Get the next version tag
            tag = api.get(url=f"/api/v1/docker/images/{name}/next_tag").text
            new_manifest = _make_manifest(name, tag, upload_results)
            print_info(f'Pushing {name} manifest...')
            # Sending image manifest.
            put_manifest_response = api.put(
                f"/api/v1/docker/images/{name}/manifests/{tag}",
                json=new_manifest,
                headers={"Content-Type": "application/vnd.docker.distribution.manifest.v2+json"},
            )
            end_time = time.time()
            time_elapsed = _get_formatted_time(end_time - start_time)
            print_success(f'Completed in {time_elapsed}.')

            print_success(f'Pushed image [{name}] to Kortical cloud container repository.')

            return put_manifest_response.text
    except (FileNotFoundError, KeyError) as e:
        raise KorticalKnownException(f'ERROR: Failed to open image tar file.')


def split_image_tag(full_tag):
    image_repo_path, version = full_tag.split(':')
    image_repo_path_components = image_repo_path.split('/')
    image_name = image_repo_path_components[-1]
    image_repo = '/'.join(image_repo_path_components[:-1])

    return image_repo, image_name, version


def update_image_version_in_files(image_tag, file_paths):
    print_info(f'Updating image name in k8s and docker folders...')
    image_repo, image_name, image_version = split_image_tag(image_tag)
    file_details = {}

    for file_path in file_paths:
        file_name = Path(file_path).name
        file_name, _ = os.path.splitext(file_name)
        file_details[file_name] = file_path

        with open(file_path, "r+") as f:
            data = f.read()
            data = re.sub(
                r'({}\/{}:)[\w\d]+'.format(image_repo, image_name),
                r"\1{}".format(image_version),
                data)
            f.seek(0)
            f.write(data)
            f.truncate()

    print_success(f'Updated all k8s and docker files.')
    return file_details
