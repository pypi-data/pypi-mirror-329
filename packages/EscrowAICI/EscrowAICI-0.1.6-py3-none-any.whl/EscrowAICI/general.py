import requests
from EscrowAICI.utils import generate_frontoffice_url


def find_keys(env, project, ao, token):
    baseUrl = generate_frontoffice_url(environment=env)
    if ao:
        wkey_get = requests.get(
            f"{baseUrl}/wrapped-content-encryption-key/?project_id={project}&is_ao_wcek={ao}",
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer " + token,
                "User-Agent": "curl/7.71.1",
            },
        )
    else:
        wkey_get = requests.get(
            f"{baseUrl}/wrapped-content-encryption-key/?project_id={project}",
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer " + token,
                "User-Agent": "curl/7.71.1",
            },
        )

    wjs = wkey_get.json()

    for i in wjs:
        if i["project"]["id"] == project and i["is_ao_wcek"] == ao:
            wkey_id = i["id"]
            break

    wkey_version_get = requests.get(
        f"{baseUrl}/wrapped-content-encryption-key-version/",
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer " + token,
            "User-Agent": "curl/7.71.1",
        },
    )

    wvjs = wkey_version_get.json()

    for i in wvjs:
        if i["key"] == wkey_id:
            kek = i["kek_version"]["id"]
            wkey_v = i["id"]
            break

    return wkey_id, kek, wkey_v
