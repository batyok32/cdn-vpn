import os
import subprocess
import secrets
import string

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

    change_header()


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

def delete_clients():
    code = input("Code of clients: ")
    print("Clients range -->")
    amount_start = eval(input("Clients start range: "))
    amount_end = eval(input("Clients end range: "))
    for x in range(int(amount_start), int(amount_end+1)):
        subprocess.run(
            [f"userdel {code}{x}"],
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
    random=False
    print("""
Password type of clients: 
[1] Random
[2] Custom""")
    password_type = input("[1]: ")
    if password_type == "2":
        password = input("Password of clients: ")
    else:
        random=True
    start_amount = eval(input("Start amount: "))
    amount = eval(input("End amount: "))
    time_to_live = eval(input("Time to live: "))
    list_users_txt = ""
    result_users_text = ""
    for x in range(int(start_amount), int(amount+1)):
        if random:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(16)) 
        list_users_txt += f"""
subprocess.run(
    ["menu"],
    input="1\\n1\\n{code}{x}\\n{password}\\n{time_to_live}\\n".encode(),
    shell=True,
)
    """
        result_users_text += f"""
{bcolors.OKGREEN}username: {code}{x}
password: {password}{bcolors.ENDC}
"""
    with open("/root/hey.py", "w") as f:
        f.write("import subprocess\n")
        f.write(list_users_txt)

    subprocess.run(
        ["python3 /root/hey.py"],
        shell=True,
    )
    if random:
        with open("/root/keys.txt", "w") as f:
            f.write(result_users_text)
        print(result_users_text)

def clear_cache():
    subprocess.run(
        ["rm -rf /var/log/syslog* && rm -rf /var/log/journal/*"],
        shell=True,
    )
    subprocess.run(
        ["systemctl restart syslog.service"],
        shell=True,
    )



def change_header():
    with open(f"/etc/banner", "w") as f:
        f.write("""
<b>
<br>
<br>
<font color="#none">Webci script</font><br>
<br>
<font color="#ee82ee">• Bir adamdan kop catylsa goni blok we yzyna pul berilmeyandir!</font><br>
</b>       
""")

def change_users_list_password():
    user_list = []
    result_array = ""
    print("Ulanyjy adyny yaz, gutaran bolsanam 'ex' diy.")
    while True:
        username = input("Username: ")
        if username == "ex":
            break
        else:
            user_list.append(username)

    for user in user_list:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(16)) 
        subprocess.run(
            [f"passwd {user}"],
            input=f"{password}\n{password}\n".encode(),
            shell=True,
        )
        result_array += f"username: {user}\npassword: {password}\n\n"
 
 
    print(result_array)



print(f"""{bcolors.WARNING}\n\n

1) Install
2) Change header
3) Clear space

--------------
4) Check too many connections
5) Generate clients
6) Delete all clients
7) Change random passwords 
{bcolors.ENDC}
""")

while True:
    res = input(">>> ")
    if res == "1":
        install()
        break
    
    elif res == "4":
        check_many()
        break

    elif res == "5":
        generate_clients()
        break

    elif res == "3":
        clear_cache()
        break

    elif res == "6":
        delete_clients()
        break

    elif res == "2":
        change_header()
        break

    elif res == "7":
        change_users_list_password()
        break

    else:
        print(f"{bcolors.FAIL}\nNormalny yazaiow\n{bcolors.ENDC}")
