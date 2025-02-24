import requests

BASE_URL = "https://kanata-05.github.io/SCP-API/scp/"

def get_all_info(scp_num):
    scp_id = f"{scp_num:03d}" 
    url = f"{BASE_URL}{scp_id}.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"ERR: {response.status_code}")
    return response.json()

def get_info(scp_num, field):
    data = get_all_info(scp_num)
    return data.get(field)
