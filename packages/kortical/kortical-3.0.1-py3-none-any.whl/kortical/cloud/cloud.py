import os
import kubernetes


# TODO: remove old PASSWORD check on platform breaking change version.
IS_KUBERNETES_ENVIRONMENT = ((os.environ.get('CLOUD_APP') \
                            and os.environ.get('SERVICE_ACCOUNT_EMAIL') \
                            and os.environ.get('SERVICE_ACCOUNT_SECRET')) is not None) \
                            or ((os.environ.get('CLOUD_APP') \
                            and os.environ.get('SERVICE_ACCOUNT_EMAIL') \
                            and os.environ.get('SERVICE_ACCOUNT_PASSWORD')) is not None)

if IS_KUBERNETES_ENVIRONMENT:
    kubernetes.config.load_incluster_config()
    kubernetes.client.rest.logger.setLevel('WARNING')

def is_beta_system():
    if not IS_KUBERNETES_ENVIRONMENT:
        return False
    pod_details = kubernetes.client.CoreV1Api().read_namespaced_pod(
        os.environ.get('K8S_POD_NAME'),
        os.environ.get('KORE_K8S_NAMESPACE')
    )
    if pod_details.metadata.labels.get('kore_is_beta_system', 'False') == 'True':
        return True
    else:
        return False