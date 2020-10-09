from pythonping import ping
import paramiko
import sys
import time
import os
import socket
import shutil
import signal
import subprocess
import getpass
import hashlib
from add_first import add_first
from add_second import add_second

print('\n\n')
print('         0******************************************************************************S')
print('         *Hello To Nexus Switches Initialization Application (NXOS) Using POAP          *')
print('         *This IS An Open For Use Application Under GNU License                         *')
print('         *Please Make Sure Of The Provided Input, Using It Is Under Your Responsibility*')
print('         0******************************************************************************S\n')
print('It Is Better To Read About POAP (Power On Auto Provisioning) To Know How This Application Works.')
print('To Start, Please Read The Following Carefully:\n')
print('1) It IS A Must To Run This Application As Administrator.')
print('2) Max. Of 2 Switches In The VPC Domain Will Be Configured.')
print('3) Connect All Management Interfaces To One Switch Along With Your Laptop.')
print('4) All Switches Should Be On Factory Defaults & Donot Press Any Key On The Console For POAP To Work.')
print('5) This Application Is Configuring LACP Only.')
print('6) This Application Is Supported On Windows OS Only & Tested On Windows 10.')
print('7) Configure Your Laptop Ethernet Interface With IP 192.168.101.253/25 & Disable All Firewalls.')
print('8) Put The Upgrade File (If You Need To Upgrade!) In The Same Application Folder & Have The MD5 Ready With You.\n')
time.sleep(11)
print('Now Checking For The Laptop Static IP Address...\n')
myip= socket.gethostbyname(socket.gethostname())
time.sleep(5)
if myip == '192.168.101.253':
    print('Your Laptop IP Address:', myip, 'Accepted\n')
else:
    print('Wrong Laptop IP Address, Please Change To 192.168.101.253\n')
    time.sleep(1)
    exit()
print('Now Checking For The Upgrade File...\n')
time.sleep(3)
g= 0
for file in os.listdir(os.getcwd()):
    if file.endswith(".bin"):
        print('Upgrade File: ', file, '\n')
        g= file
        if 'Yes' not in input('Is That The Correct File? Answer [Yes] Or [No]:\n'):
            exit()
if g==0:
    print('No Upgrade File Found\n')
print('\n')
if g != 0:
    k= hashlib.md5(open(g,'rb').read()).hexdigest()
    l= input('Please Enter The Upgrade File MD5 Acquired From Cisco Download Website:\n')
    if l == k:
        print ('Upgrade File Authenticy Confirmed, Continuing With the Application...\n')
        time.sleep(3)
    if l != k:
        print ('MD5 Validation Failed, Application Will Exit Now\n')
        time.sleep(3)
        exit()
inios1= os.getcwd() + '/server/initdev1.cfg'
inios2= os.getcwd() + '/server/initdev2.cfg'
shutil.copy(inios1, os.getcwd())
shutil.copy(inios2, os.getcwd())
if g !=0:
    add_first ('initdev1.cfg', 'boot nxos bootflash:/' + g)
    add_first ('initdev2.cfg', 'boot nxos bootflash:/' + g)
input('When You Are Ready, Press Enter. Else, Close The Application - 0S0S\n')
s= input('Do you Need To Create A VPC Domain? Answer [Yes] or [No]:\n')
if s != ('Yes' or 'No'):
    print ('Wrong Answer')
    exit()
if s == 'No':
    print('Only Switch Upgrade (If Included) Will Be Done Along With Configuring Management IP Address & Credentials\n')
a=0
b=0
c=0
if s == 'Yes':
    a= int(input('What Is The VPC Domain ID?\n'))
    b= int(input('Is The VPC Domain Will Be Connected To Normal Spanning-tree Switches? Choose 1)Yes     2)No:\n'))
    c= int(input('Is The VPC Domain Will Have SVI Configured? Choose 1)Yes     2)No:\n'))
d1=input('Enter First Switch Management IP Address:\n')
d2=input('Enter Second Switch Management IP Address:\n')
if d1 == d2:
    print ('Same Management IP Address Cannot Be Configured On Both Nexus Switches\n')
    exit()
e= input('Enter Management Subnet Mask:\n')
f= input('Enter Management Default Gateway:\n')
username= input('Please Enter Username Required To Be Configured:\n')
password= input('Please Enter Password Required To Be Configured (Complex Password Is A Must):\n')
client= input('Please Enter The Client Name:\n')
tfos= os.getcwd() + '/server/tftpd32.ini'
shutil.copy(tfos, os.getcwd())
pos= os.getcwd() + '/server/poaposos.py'
shutil.copy(pos, os.getcwd())
time.sleep(1)
if g != 0:
    m = "cli (" + "'copy tftp://cisco:cisco@192.168.101.253/" + g + " bootflash: vrf management" + "')"
    n = "cli (" + "'configure terminal ;  boot nxos bootflash:" + g + "')"
    add_first('poaposos.py', n)
    add_first ('poaposos.py', m)
add_first ('poaposos.py', 'from cli import *')
add_first ('poaposos.py', '#!/bin/env python')
time.sleep(1)
h= hashlib.md5(open('poaposos.py','rb').read()).hexdigest()
print('Current POAP File MD5SUM Is:', h, 'Please Keep It For Your Reference.')
time.sleep(1)
add_first ('poaposos.py', '#!/bin/env python')
add_second ('poaposos.py', '#md5sum=' + '''"''' + h + '''"''')
print ('Now Bootstrapping Switches, Please Wait...\n')
tfpid = subprocess.Popen("tftpd64.exe")
time.sleep(1917)
os.kill(tfpid.pid, signal.SIGTERM)
os.remove(os.getcwd() + '/initdev1.cfg')
os.remove(os.getcwd() + '/initdev2.cfg')
os.remove(os.getcwd() + '/poaposos.py')
os.remove(os.getcwd() + '/tftpd32.ini')
allip= ['192.168.101.181','192.168.101.182']
time.sleep(3)
swlst= []
i= 0
print('Now Pinging To Switches To Confirm Reachability, Please Wait...\n')
time.sleep(3)
for i in range(len(allip)):
    response= ping(allip[i], count=7)
    response1= response.success()
    if response1 == True:
        print('Switch:', allip[i], 'Up')
        swlst.append(allip[i])
    elif response1 == False:
        print ('Switches Are Unreachable')
        exit()
print('Reachability Test Finished...')
print('\n')
client= paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
i=0
print('Getting Software Version From Switches, Please Wait...\n')
time.sleep(3)
for i in range(len(swlst)):
    client.connect(swlst[i], port= 22, username= 'cisco', password= 'Cisco123')
    shell= client.invoke_shell()
    shell.send('show version\n')
    time.sleep(2)
    output = shell.recv(65535).strip()
    output2 = str(output).split()
    shell.send('exit\n')
    output3 = output2[output2.index('NXOS:') + 2]
    output4 = output3.replace('\\r\\n', '')
    print('Switch', i+1, 'Current Software Version: ', output4)
print('\n\n')
vpclnk= []
uplnk= []
vpclnk1= input('Please Enter VPC Link Ports (Port Number Only) One Per Line - Enter X To Finish:\n')
while vpclnk1 != "X":
    vpclnk.append(vpclnk1)
    vpclnk1= input()
uplnk1= input('Please Enter Uplink Ports (Port Number Only) One Per Line- Enter X To Finish:\n')
while uplnk1 != "X":
    uplnk.append(uplnk1)
    uplnk1= input()
if len(vpclnk) == 0:
    print('No VPC Links Added - Application Will Close')
    time.sleep(1)
    exit()
else:
    print("VPC Ports Are:", vpclnk)
if len(uplnk) == 0:
    print('No Uplinks Added - No Uplinks Will Be Configured')
    time.sleep(1)
else:
    print("Uplink Ports Are:", uplnk)
time.sleep(3)
if 'Yes' not in input("Is The Information Correct? - Answer [Yes] Or [No]:\n"):
    print("Please Restart The Program.\n")
    time.sleep(1)
    exit()
time.sleep(1)
print('\n\n')
print('***Now Configuring Nexus Switches - VPC Part, Please Wait...***\n')
i= 0
for i in range(2):
    client.connect(swlst[i], port= 22, username= 'cisco', password= 'Cisco123')
    shell = client.invoke_shell()
    shell.send('configure terminal\n')
    shell.send('feature vpc\n')
    time.sleep(1)
    shell.send('feature lacp\n')
    time.sleep(1)
    shell.send('vpc domain ' + str(a) + '\n')
    time.sleep(1)
    if i == 0:
        shell.send('peer-keepalive destination ' +  d2 + ' source ' + d1 + ' vrf management \n')
        time.sleep(1)
        shell.send('role priority 100\n')
        time.sleep(1)
    if i == 1:
        shell.send('peer-keepalive destination ' + d1 + ' source ' + d2 + ' vrf management \n')
        time.sleep(1)
        shell.send('role priority 90\n')
        time.sleep(1)
    shell.send('\n')
    if b == 1:
        shell.send('peer-switch\n')
        time.sleep(1)
    if c == 1:
        shell.send('peer-gateway\n')
        time.sleep(1)
    shell.send('interface port-channel 100\n')
    time.sleep(1)
    shell.send('vpc peer-link\n')
    time.sleep(1)
    shell.send('switchport mode trunk\n')
    time.sleep(1)
    shell.send('no shutdown\n')
    time.sleep(1)
    shell.send('interface ethernet ' + vpclnk[0] + ', ethernet' + vpclnk[1] + '\n')
    time.sleep(1)
    shell.send('switchport mode trunk\n')
    time.sleep(1)
    shell.send('channel-group 100 mode active\n')
    time.sleep(1)
    shell.send('no shutdown\n')
    time.sleep(1)
print('***VPC Configuration Finished...***\n')
i= 0
j= 0
print('***Now Configuring Nexus Switches - Uplinks Part, Please Wait...***\n')
for i in range(len(swlst)):
    for j in range (len(uplnk)):
        client.connect(swlst[i], port= 22, username= 'cisco', password= 'Cisco123')
        shell = client.invoke_shell()
        shell.send('configure terminal\n')
        time.sleep(1)
        shell.send('interface ethernet ' + uplnk[j] + '\n')
        time.sleep(1)
        shell.send('switchport mode trunk\n')
        time.sleep(1)
        shell.send('channel-group 200 mode active\n')
        time.sleep(1)
        shell.send('no shutdown\n')
        time.sleep(1)
        shell.send('interface port-channel 200\n')
        time.sleep(1)
        shell.send('switchport mode trunk\n')
        time.sleep(1)
        shell.send('vpc 200\n')
        time.sleep(3)
        shell.send('no shutdown\n')
        time.sleep(1)
print('***Uplinks Configuration Finished...***\n')
time.sleep(5)
print('***Starting Additional Configuration, Please Wait...***\n')
i= 0
for i in range(2):
    client.connect(swlst[i], port= 22, username= 'cisco', password= 'Cisco123')
    shell = client.invoke_shell()
    shell.send('configure terminal\n')
    time.sleep(1)
    shell.send('username ' + username + 'password ' + password + ' role network-admin\n')
    time.sleep(1)
    shell.send('ip route 0.0.0.0 0.0.0.0 ' + f + ' vrf management\n')
    time.sleep(1)
    shell.send('show running-config interface mgmt 0\n')
    time.sleep(1)
    output = shell.recv(65535).strip()
    output2 = str(output).split()
    output3 = output2[output2.index('address') + 1]
    output4 = output3.replace("\\r\\n\\r\\n\\rosos(config)#'",'')
    time.sleep(11)
    if output4 == '192.168.101.181/25':
        shell.send('hostname N9K-1\n')
        time.sleep(1)
        shell.send('interface mgmt 0\n')
        time.sleep(1)
        shell.send('ip address ' + d1 + ' 255.255.255.0\n')
        time.sleep(1)
        shell.send('copy running-config startup-config\n')
        time.sleep(1)
    if output4 == '192.168.101.182/25':
         shell.send('hostname N9K-2\n')
         shell.send('interface mgmt 0\n')
         time.sleep(1)
         shell.send('ip address ' + d2 + ' 255.255.255.0\n')
         time.sleep(1)
         shell.send('copy running-config startup-config\n')
         time.sleep(1)
    time.sleep(1)
print('***Additional Configuration Finished...***\n')
getos= os.getcwd() + '/server/getname.cmd'
shutil.copy(getos, os.getcwd())
time.sleep(3)
q = subprocess.Popen('getname 192.168.101.253', shell=True, stdout=subprocess.PIPE)
r1, error=  q.communicate()
r2= r1.decode('utf-8')
r3= r2.replace('\r\n','')
d3= str(d1).split('.')
d31= d3[0]
d32= d3[1]
d33= d3[2]
d34= int(d3[3])
d4= d34 + 5
d5= str(d31) + '.' + str(d32) + '.' + str(d33) + '.' + str(d4)
t1 = str('netsh interface ipv4 add address ' + '"' + r3 + '" ' + d5 +  ' 255.255.255.0')
t2 = str('netsh interface ipv4 delete address ' + '"' + r3 + '" ' + d5 +  ' 255.255.255.0')
subprocess.Popen( t1, shell=True, stdout=subprocess.PIPE)
time.sleep(3)
print('Now Pinging To Switches With The Required Management IP Address To Confirm Reachability, Please Wait...\n')
time.sleep(3)
dd= ['0','0']
dd[0]= d1
dd[1]= d2
i= 0
for i in range(len(dd)):
    response= ping(dd[i], count=7)
    response1= response.success()
    if response1 == True:
        print('Switch:', dd[i], 'Up')
    elif response1 == False:
        print ('Switches Are Unreachable')
        exit()
print('Reachability Test Finished...')
print('\n')
print('***Displaying VPC Configuration - show vpc -, Please Wait...***\n')
i= 0
for i in range(2):
    print ('Show VPC On Switch', i + 1, '\n')
    client.connect(dd[i], port= 22, username= 'cisco', password= 'Cisco123')
    shell = client.invoke_shell()
    stdin, stdout, stderr = client.exec_command('show vpc\n')
    time.sleep(1)
    u= 0
    for u in stdout:
        print(u)
    print ('\n')
print('***Configuration & Verification Are Completed...***\n')
subprocess.Popen( t2, shell=True, stdout=subprocess.PIPE)
time.sleep(3)
os.remove(os.getcwd() + '/getname.cmd')
print('*****Please Refer To Cisco Guides For How To Confirm VPC Configuration & Troubleshooting*****')
print('Bye :) Ahmed Ossama')
time.sleep(5)
exit()
