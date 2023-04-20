
import socket  



## func for the connection of the host and the port you open on 

def host_connection():
    host = '127.0.0.1'
    port = 1338
    
    return host, port

#Creat a listening on the port
def listening(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(1)
    print(f'Server is listen on port: {port} and wait for connection ')
    
    return s

 
#the creation of the connection with  the remote ip
def server_connection(s):
    sock_conn, remote_addr = s.accept()
    remote_ip, remote_port = remote_addr
    print(f'You are connected to remote host: {remote_ip}, on  remote port: {remote_port} ')
    open_msg = sock_conn.recv(2048)
    print(open_msg.decode('utf-8'))
    permissions_awar = sock_conn.recv(2048)
    print(permissions_awar.decode('utf-8'))
    
    while sock_conn:

        status = data_recive(sock_conn)
        if status == 'exit':
           return 'exit'
        
      
def data_recive(sock_conn):
    in_d = sock_conn.recv(2048)

    if not in_d:
        return 'exit'
    elif 'exit' in in_d.decode('utf-8'):
        return 'exit'
    
    try:
        cmd_line = input(in_d.decode('utf-8'))
        send_data(sock_conn,cmd_line)
        back_data = sock_conn.recv(2048)
        print(back_data.decode('utf-8'))
    except Exception as e:
        print(e)
    return ""
    
    
def send_data(sock_conn,cmd_line):
    sock_conn.send(cmd_line.encode())
    
          
   
def break_connection(s):
    s.close()
              




        
    
def main():
    
    host, port = host_connection()
    server_conn = listening(host,port)
    server_status = server_connection(server_conn)
    if 'exit' in server_status:
        break_connection(server_conn)
        print('\nConnection have ended\n  ')
    

        
try:
    main()

except KeyboardInterrupt:
    print('\nThank you and Good bye ')