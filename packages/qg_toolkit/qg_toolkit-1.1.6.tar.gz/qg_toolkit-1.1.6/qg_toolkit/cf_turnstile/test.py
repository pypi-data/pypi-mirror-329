import requests


def get_cf_token_v2():
    body = {
        "site_key": "0x4AAAAAAAaHm6FnzyhhmePw",
        "target_url": "https://pioneer.particle.network/zh-CN/point",
        "headless": True
    }
    r = requests.post("http://127.0.0.1:5555/solve", json=body)
    token = r.json()["token"]
    print("Solved :: " + token)
    return token

def get_cf_token_on_sonic():
    """在sonic上解CF_TOKEN"""
    body = {
        "site_key": "0x4AAAAAAAM8ceq5KhP1uJBt",
        "target_url": "https://yaps.kaito.ai/onboarding/0?redirect=%2F",
        "headless": True
    }
    r = requests.post("http://127.0.0.1:5555/solve", json=body)
    token = r.json()["token"]
    print("Solved :: " + token)
# get_cf_token_v2()
get_cf_token_on_sonic()