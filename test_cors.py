import urllib.request

req = urllib.request.Request("https://api.macvendors.com/00:00:0C", headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Origin": "http://192.168.1.220:1313",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors"
})
try:
    resp = urllib.request.urlopen(req)
    print("Code:", resp.getcode())
    print("Headers:\n", resp.headers)
    print("Body:", resp.read().decode())
except Exception as e:
    print(e)
