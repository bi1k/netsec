from pexpect import pxssh


class SshServer:
    def __init__(self, h, u, p):
        self.s = pxssh.pxssh()
        self.hostn = h
        self.usern = u
        self.passw = p
        self.statu = "offline"

    def log_in(self):
        try:
            self.s.login(self.hostn, self.usern, self.passw)
            self.statu = "online"
            print("Login successful for {}.".format(self.hostn))
            return True
        except pxssh.ExceptionPxssh as err:
            print("Login failed for {}. {}".format(self.hostn, err))
            return False

    def command(self, c, para, flsh):
        if para == "y":
            self.s.sendline(c)
            print("Command sent to {}.".format(self.hostn))
        else:
            if flsh == "y":
                print("This may take a moment if a previous command is still running.")
                self.s.prompt()
            self.s.sendline("echo '|||'; {}; echo '|||'".format(c))
            self.s.prompt()
            stdout = str(self.s.before).split("\\r\\n|||\\r\\n")
            print("{}".format(self.hostn))
            print(stdout[1].replace("\\n", "\n").replace("\\r", "\r"))

    def log_out(self):
        self.s.logout()

    def __str__(self):
        return '"{}", "{}", "{}"'.format(self.hostn, self.usern, self.passw)


ssh_servers = []
parallel = "y"
flush = "n"

try:
    with open("ssh_servers.txt", "r") as f:
        for line in f:
            li = line.split(", ")
            ssh_servers.append(SshServer(li[0], li[1], li[2].rstrip("\n")))
except Exception as e:
    print("{}. Creating new file.".format(e))
    f = open("ssh_servers.txt", "w")
    f.close()

ss_len = len(ssh_servers)

for i in range(0, ss_len):
    stay_on_index = "y"
    while stay_on_index == "y":
        if i >= ss_len:
            break
        status_check = ssh_servers[i].log_in()
        if status_check:
            stay_on_index = "n"
        else:
            del ssh_servers[i]
            ss_len = len(ssh_servers)

instruct = ""
while instruct != "q":
    instruct = input("\nEnter a command: ").lower()
    if not instruct:
        pass
    elif instruct.lower().startswith("option "):
        if instruct[7:] == "help":
            print("- help: displays options\n"
                  "- parallel: toggles botnet parallelism. "
                  "If on, entered commands are run on all SSH bots at the same time but does not return their STDOUT. "
                  "If off, entered commands are run on each SSH bot one at a time and returns their STDOUT")
        elif instruct[7:] == "parallel":
            if parallel == "y":
                parallel = "n"
                print("SSH botnet parallelism toggled off.")
            else:
                parallel = "y"
                print("SSH botnet parallelism toggled on.")
        else:
            print("Invalid option")
    elif instruct != "q":
        for i in range(0, ss_len):
            ssh_servers[i].command(instruct, parallel, flush)
        if parallel == "y":
            flush = "y"
        else:
            flush = "n"
    else:
        for i in range(0, ss_len):
            ssh_servers[i].log_out()
