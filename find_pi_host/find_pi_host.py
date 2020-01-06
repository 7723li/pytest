import paramiko
import threading

tested_ip = {}

def con_ssh(begin, end):
    global tested_ip

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    for i in range(begin, end):
        hostname = "192.168.9." + str(i)
        port = 22
        username = "pi"
        password = "raspberry"
        try:
            client.connect(hostname, port, username, password)
            tested_ip[hostname] = "succeed"
        except:
            tested_ip[hostname] = "Filed"

class myThread(threading.Thread):
    def __init__(self, begin, end):
        threading.Thread.__init__(self)
        self.begin = begin
        self.end = end

    def run(self):
       con_ssh(self.begin, self.end)

def main():
    global tested_ip

    for i in range(0, 255, 10):
        thr = myThread(i, i + 10)
        thr.start()

    thr = myThread(250, 255)
    thr.start()

    tar_ip = ""
    print_idex = 0
    last_idex = print_idex
    while True:
        ip_list = list(tested_ip.items())
        size = len(ip_list)

        if size >= 255:
            break
        elif size != last_idex:
            last_idex = size
        else:
            continue

        print(print_idex)
        '''
        prog = last_idex * 100 / 255
        print("already finish " + str(prog) + "%")
        '''

        for i in range(print_idex, last_idex):
            print(ip_list[i][0])
            if(ip_list[i][1] == "succeed"):
                tar_ip = ip_list[i][0]

        print_idex = last_idex
           
    print("finished")

    if "" != tar_ip:
        print("should be --> " + tar_ip)
    else:
        print("Not found")

if __name__ == "__main__":
    main()