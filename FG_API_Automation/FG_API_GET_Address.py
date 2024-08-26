import requests as req
from pprint import pprint

url = "http://192.168.10.99/api/v2/cmdb/firewall/address?access_token=d580jc97QHxwn4b9bxqzxHkxtx0wwh"

payload = {}
headers = {'Authorization': "Bearer"}

if __name__ == "__main__":
    # response = req.request("GET", url, headers=headers, data=payload, verify=False)
    response = req.request("GET", url, headers=headers, data=payload)

    pprint(response.text)
