from kubernetes.client.exceptions import ApiException
from ..k8s_cluster import config_check, api_config_handler
from kubernetes import client
from src.codeflare_sdk.common.k8s_cluster.kube_api_helpers import _kube_api_error_handling
from typing import Optional

def get_default_kueue_name(namespace: str):
    # If the local queue is set, use it. Otherwise, try to use the default queue.
    try:
        config_check()
        api_instance = client.CustomObjectsApi(api_config_handler())
        local_queues = api_instance.list_namespaced_custom_object(
            group="kueue.x-k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="localqueues",
        )
    except ApiException as e:  # pragma: no cover
        if e.status == 404 or e.status == 403:
            return
        else:
            return _kube_api_error_handling(e)
    for lq in local_queues["items"]:
        if (
                "annotations" in lq["metadata"]
                and "kueue.x-k8s.io/default-queue" in lq["metadata"]["annotations"]
                and lq["metadata"]["annotations"]["kueue.x-k8s.io/default-queue"].lower()
                == "true"
        ):
            return lq["metadata"]["name"]


def local_queue_exists(namespace: str, local_queue_name: str):
    # get all local queues in the namespace
    try:
        config_check()
        api_instance = client.CustomObjectsApi(api_config_handler())
        local_queues = api_instance.list_namespaced_custom_object(
            group="kueue.x-k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="localqueues",
        )
    except Exception as e:  # pragma: no cover
        return _kube_api_error_handling(e)
    # check if local queue with the name provided in cluster config exists
    for lq in local_queues["items"]:
        if lq["metadata"]["name"] == local_queue_name:
            return True
    return False


def add_queue_label(item: dict, namespace: str, local_queue: Optional[str]):
    lq_name = local_queue or get_default_kueue_name(namespace)
    if lq_name == None:
        return
    elif not local_queue_exists(namespace, lq_name):
        raise ValueError(
            "local_queue provided does not exist or is not in this namespace. Please provide the correct local_queue name in Cluster Configuration"
        )
    if not "labels" in item["metadata"]:
        item["metadata"]["labels"] = {}
    item["metadata"]["labels"].update({"kueue.x-k8s.io/queue-name": lq_name})
