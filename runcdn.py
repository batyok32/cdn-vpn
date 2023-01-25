import os
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f"{bcolors.BOLD}{bcolors.UNDERLINE}{bcolors.OKCYAN}\nHi, it is script to run cdn vpn using dropbear.\n{bcolors.ENDC}")



def install():

    subprocess.run(
        ["rm -f install* && wget -q https://raw.githubusercontent.com/excelsiorcode/websocket/master/install && chmod +x install && ./install"],
            shell=True,
    )

    with open(f"/root/cleanup.sh", "w") as f:
        f.write("""
#!/bin/bash

rm -rf /var/log/syslog*
rm -rf /var/log/journal/*    
        """)

    subprocess.run(
        ["chmod +x /root/cleanup.sh"],
        shell=True,
    )
    subprocess.run(
        ["apt install python3-pip -y"],
        shell=True,
    )
    subprocess.run(
        ["pip3 install python-crontab"],
        shell=True,
    )

    from crontab import CronTab

    my_cron = CronTab(user='root')
    job = my_cron.new(command='bash /root/cleanup.sh')
    job2 = my_cron.new(command='bash /usr/local/sbin/clearcache.sh')
    job.minute.every(30)
    job2.minute.every(30)
    my_cron.write()


def install_check():
    with open("/root/killmultiple.sh", "w") as z:
        z.write("""
#!bin/bash
source /usr/local/sbin/base-script > /dev/null 2>&1
if [[ "${MYSHELL}" != '/usr/local/sbin' ]]; then
 echo -e "[\e[31mError\e[0m] Error loading menuscript files"
 exit 1
fi
#clear
if [[ -e "/var/log/auth.log" ]]; then
 LOG="/var/log/auth.log"
elif [[ -e "/var/log/secure" ]]; then
 LOG="/var/log/secure"
fi
if [[ -z "$(cat < $LOG)" ]]; then
 systemctl restart rsyslog > /dev/null 2>&1
 systemctl restart rsyslogd > /dev/null 2>&1
 service rsyslog restart > /dev/null 2>&1
 service rsyslogd restart > /dev/null 2>&1
 echo -e "Seems your SSH authlogs are empty, please double check your rsyslog service"
fi
                
ps aux | grep -i dropbear | awk '{print $2}' > /var/data.txt
cat $LOG | grep -i dropbear | grep -i "Password auth succeeded" > /var/login-db.txt;

/usr/bin/python3 /root/findmultiple.py        
        """)

    with open("/root/findmultiple.py", "w") as x:
        x.write("""
import json
import subprocess
import collections
f = open("/var/data.txt", "r")
data = f.readlines()
connectedlist = []
for pid in data:
    pid = pid.split("\\n")[0]
    clea = open("/var/login-db-pid.txt", "w")
    clea.write("")
    clea.close()
    subprocess.call(
        [f"cat /var/login-db.txt | grep 'dropbear\[{pid}\]' > /var/login-db-pid.txt;"],
        shell=True,
        stdout=subprocess.PIPE,
    )
    num = subprocess.check_output(
        "cat /var/login-db-pid.txt | wc -l", shell=True
    )
    user = subprocess.check_output(
        "cat /var/login-db-pid.txt | awk '{print $10}'",
        shell=True,
    )
    ip = subprocess.check_output(
        "cat /var/login-db-pid.txt | awk '{print $12}'",
        shell=True,
    )
    num = json.loads(num)  
    user = user.decode("utf-8")
    user = user[1:-2]
    if num == 1:
        connectedlist.append(user)
seen = set()
dupes = []
for connecteduser in connectedlist:
    if connecteduser in seen:
        dupes.append(connecteduser)
    else:
        seen.add(connecteduser)
print("Ахуевшие клиенты: \\n")
counter = collections.Counter(dupes)
for count in counter:
    print(count, "-", counter[count]+1)
f.close()        
        """)

def run_check():
    subprocess.run(
        ["bash /root/killmultiple.sh"],
        shell=True,
    )


def check_many():
    if os.path.exists("/root/killmultiple.sh") and os.path.exists("/root/findmultiple.py"):
        run_check()
    else:
        install_check()
        run_check()


def generate_clients():
    code = input("Code of clients: ")
    password = input("Password of clients: ")
    amount = eval(input("Clients amount: "))
    list_users_txt = ""
    for x in range(1, int(amount+1)):
        list_users_txt += f"""
subprocess.run(
    ["menu"],
    input="1\\n1\\n{code}{x}\\n{password}\\n30\\n".encode(),
    shell=True,
)
    """
    with open(f"/root/hey.py", "w") as f:
        f.write("import subprocess\n")
        f.write(list_users_txt)

    subprocess.run(
        ["python3 /root/hey.py"],
        shell=True,
    )

def clear_cache():
    subprocess.run(
        ["rm -rf /var/log/syslog* && rm -rf /var/log/journal/*"],
        shell=True,
    )



print(f"""{bcolors.WARNING}\n\n
1) Install
2) Check too many connections
3) Generate clients
4) Clear space
{bcolors.ENDC}
""")

while True:
    res = input(">>> ")
    if res == "1":
        install()
        break
    
    elif res == "2":
        check_many()
        break

    elif res == "3":
        generate_clients()
        break

    elif res == "4":
        clear_cache()
        break

    else:
        print(f"{bcolors.FAIL}\nNormalny yazaiow\n{bcolors.ENDC}")
