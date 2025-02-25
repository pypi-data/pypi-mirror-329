import requests
import sseclient
import json
import os
from EscrowAICI.utils import generate_frontoffice_url, generate_notifications_url
from EscrowAICI.general import find_keys
from azure.storage.blob import BlobClient


def upload_algo(
    env,
    project,
    name,
    org,
    version_description,
    algo_type,
    file,
    token,
    algorithm_description,
    algo_version_tag,
    compute,
    exists,
    algo_id,
):
    try:
        baseUrl = generate_frontoffice_url(environment=env)
        data_attestation, validation_criteria = find_artifacts(
            env, project, algo_type, token
        )
        wcek_version = find_keys(env, project, True, token)[2]
        cvm = False
        aci = False
        if compute == "CVM":
            cvm = True
        if compute == "Microsoft ACI":
            aci = True

        if not exists:
            response = requests.post(
                f"{baseUrl}/composite/algorithm/",
                headers={"Authorization": "Bearer " + token},
                data={
                    "algorithm": '"{\\"name\\":\\"'
                    + name
                    + '\\",\\"description\\":\\"'
                    + algorithm_description
                    + '\\",\\"project\\":\\"'
                    + project
                    + '\\",\\"organization\\":\\"'
                    + org
                    + '\\"}"',
                    "version_tag": "v1",
                    "description": version_description,
                    "algorithm_type": algo_type,
                    "validation_criteria_version": validation_criteria,
                    "data_attestation_version": data_attestation,
                    "has_phi_agreement": "true",
                    "upload_type": "Upload Zip",
                    "upload_file_name": os.path.basename(file),
                    "wcek_version": wcek_version,
                    "is_fortanix_sgx_enabled": "false",
                    "is_microsoft_aci_enabled": str(aci),
                    "is_cvm_enabled": str(cvm),
                },
                files=[("0", (file, open(file, "rb"), "application/zip"))],
            )
        else:
            response = requests.post(
                f"{baseUrl}/algorithm-version/",
                headers={
                    "Authorization": "Bearer " + token,
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
                },
                data={
                    "algorithm": algo_id,
                    "version_tag": algo_version_tag,
                    "description": version_description,
                    "algorithm_type": algo_type,
                    "validation_criteria_version": validation_criteria,
                    "data_attestation_version": data_attestation,
                    "upload_type": "Upload Zip",
                    "upload_file_name": os.path.basename(file),
                    "has_phi_agreement": "true",
                    "wcek_version": wcek_version,
                    "is_fortanix_sgx_enabled": "false",
                    "is_microsoft_aci_enabled": str(aci),
                    "is_cvm_enabled": str(cvm),
                },
                files=[("0", (file, open(file, "rb"), "application/zip"))],
            )

        return response
    except Exception as e:
        print("Error uploading Algorithm to Escrow")
        print(e)
        raise (e)


def finish_algo_upload(env, file, response, id, compute, token):
    try:
        baseUrl = generate_frontoffice_url(environment=env)
        cvm = False
        aci = False
        if compute == "Microsoft ACI":
            aci = True
        if compute == "CVM":
            cvm = True
        data = response.json()

        version_id = data["algorithm_version_id"]
        url = data["upload_url"]
        client = BlobClient.from_blob_url(url)

        with open(file, "rb") as upload:
            client.upload_blob(upload, overwrite=True)

        patch = requests.patch(
            f"{baseUrl}/algorithm-version/{version_id}/",
            headers={"Authorization": "Bearer " + token, "User-Agent": "curl/7.71.1"},
            data={
                "status": "In Progress",
                "algorithm": id,
                "is_fortanix_sgx_enabled": "false",
                "is_microsoft_aci_enabled": str(aci),
                "is_cvm_enabled": str(cvm),
            },
            files=[("0", (file, open(file, "rb"), "application/zip"))],
        )

        return patch
    except Exception as e:
        print("Error triggering algorithm build pipeline.")
        print(e)
        raise (e)


def get_algorithm_version_tag_default(env, token, algorithm_id):
    try:
        version_tag = ""
        baseUrl = generate_frontoffice_url(environment=env)
        resp = requests.get(
            f"{baseUrl}/algorithm-version/?algorithm_id={algorithm_id}",
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer " + token,
                "User-Agent": "curl/7.71.1",
            },
        )
        algorithm_versions = resp.json()
        version_number = len(algorithm_versions)
        version_tag = f"v{str(version_number + 1)}"
        return version_tag
    except Exception as e:
        print("Error uploading Algorithm to Escrow")
        print(e)
        raise (e)


def get_algo_notification(env, project, token):
    baseNotificationsUrl = generate_notifications_url(environment=env)
    client = sseclient.SSEClient(
        f"{baseNotificationsUrl}/project-notifications/{project}/?token={token}"
    )
    for event in client:
        if event.event != "stream-open" and event.event != "keep-alive":
            if event.data != "":
                message = json.loads(event.data)["message"]
                print(f"\033[1m\033[92mESCROWAI: \033[0m\033[0m{message}")
                if message == "Docker Push Succeeded":
                    return True
                if (
                    message == "File Validation Failed"
                    or message == "EnclaveOS Build Failed"
                ):
                    return False


def find_artifacts(env, project, algo_type, token):
    try:
        baseUrl = generate_frontoffice_url(environment=env)
        artifact_get = requests.get(
            f"{baseUrl}/artifact/?project_id={project}",
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer " + token,
                "User-Agent": "curl/7.71.1",
            },
        )

        ajs = artifact_get.json()

        data_attestation_artifact_id = None
        validation_criteria_artifact_id = None

        for i in ajs:
            if (
                i.get("artifact_type")
                and i.get("artifact_type").get("name") == "validation_criteria"
            ):
                validation_criteria_artifact_id = i["id"]
            if (
                i.get("artifact_type")
                and i.get("artifact_type").get("name") == "data_attestation"
            ):
                data_attestation_artifact_id = i["id"]

        if not data_attestation_artifact_id:
            raise Exception("Could not find a Data Attestation artifact on the project")

        if not validation_criteria_artifact_id and algo_type == "validation":
            raise Exception(
                "Could not find a Validation Criteria artifact on the project"
            )

        artifact_v_get = requests.get(
            f"{baseUrl}/artifact-version/?artifact_id={data_attestation_artifact_id}",
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer " + token,
                "User-Agent": "curl/7.71.1",
            },
        )
        attest_id = artifact_v_get.json()[0]["id"]

        valid_id = None
        if validation_criteria_artifact_id:
            artifact_v_get = requests.get(
                f"{baseUrl}/artifact-version/?artifact_id={validation_criteria_artifact_id}",
                headers={
                    "Content-type": "application/json",
                    "Authorization": "Bearer " + token,
                    "User-Agent": "curl/7.71.1",
                },
            )
            valid_id = artifact_v_get.json()[0]["id"]

    except Exception as e:
        print("Error retrieving artifact versions")
        print(e)
        raise (e)

    return attest_id, valid_id
