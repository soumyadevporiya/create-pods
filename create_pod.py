import urllib.request

from flask import jsonify
import json

import time

# Required for Kubernetes POD Management, ensure RBAC authorisation is configured
import os
import kubernetes
from kubernetes import client, config, watch
from kubernetes.client.models import V1PodSpec
from kubernetes.client.models import V1Container
from kubernetes.client.models import V1Pod
from kubernetes.client.models import V1ObjectMeta
from kubernetes.client import V1EnvVar

config.load_incluster_config()
v1 = kubernetes.client.CoreV1Api()

container_name = 'container-with-envs'
namespace = 'default'
pod_name = 'my-bq-read-pod-{}'.format(11)

image = 'gcr.io/level-approach-382012/bq_storage_reader_client:latest'
env = V1EnvVar(name='PARTITION_FIELD', value='11')
container = V1Container(name=container_name, image=image, env=[env])
podspec = V1PodSpec(containers=[container], restart_policy="Always")
metadata = V1ObjectMeta(name=pod_name, namespace=namespace)
pod = V1Pod(api_version='v1', kind='Pod', metadata=metadata, spec=podspec)

my_pod = v1.create_namespaced_pod(namespace, pod)

while True:
    resp = v1.read_namespaced_pod(name=pod_name, namespace='default')
    if resp.status.phase != 'Pending':
        break
    time.sleep(1)

# ret = v1.read_namespaced_pod(pod_name, namespace)

# if ret:
# details = "POD Created"

# print(jsonify({"message": "POD Details ", "Information: ": details}))

while True:
    resp = v1.read_namespaced_pod(name=pod_name, namespace='default')
    if resp.status.phase == 'Succeeded':
        break

# delete_response = v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
print("Pod is created")
