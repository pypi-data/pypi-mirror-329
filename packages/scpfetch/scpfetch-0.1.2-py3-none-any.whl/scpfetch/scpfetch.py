import requests
from typing import Any, Dict, Union

BASE_URL = "https://kanata-05.github.io/SCP-API/scp/"

def get_all_info(scp_num: int) -> Dict[str, Any]:
    scp_id: str = f"{scp_num:03d}"
    url: str = f"{BASE_URL}{scp_id}.json"
    response: requests.Response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"ERR: {response.status_code}")
    return response.json()

def get_info(scp_num: int, field: str, adnum: Union[int, None] = None) -> Any:
    data: Dict[str, Any] = get_all_info(scp_num)
    fieldVal: Any = data.get(field)
    if not isinstance(fieldVal, list):
        return fieldVal
    elif adnum is not None and 0 <= adnum < len(fieldVal):
        return fieldVal[adnum]
    raise IndexError("Invalid index")

print(get_info(343, "description", 1))
