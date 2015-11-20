from socket import socket, AF_INET, SOCK_STREAM 
port = 50008 
host = 'localhost' 
def server():
    sock = socket(AF_INET, SOCK_STREAM) # IP
    sock.bind(('', port)) 
    sock.listen(5) 
    while True:
        conn, addr = sock.accept() #apply connection
        data = conn.recv(1024) #bytes from client
        reply = 'server got: [%s]' % data  #new socket
        conn.send(reply.encode()) #to client
        
def client(name):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port)) 
    sock.send(name.encode()) 
    reply = sock.recv(1024)
    sock.close()
    print('client got: [%s]' % reply)
if __name__ == '__main__':
    from threading import Thread
    sthread = Thread(target=server)
    sthread.daemon = True 
    sthread.start() # wait 
    for i in range(5):
        Thread(target=client, args=('client%s' % i,)).start()
########################################################################
"""тоже сокет, но теперь для общения независимых программ, а не только потоков
выполнения; сервер в этом примере обслуживает клиентов, выполняющихся в виде
отдельных процессов и потоков; сокеты, как и именованные каналы, являются
глобальными для компьютера: для их использования не требуется совместно
используемая память"""       
import sys, os
from threading import Thread
mode = int(sys.argv[1])
if mode == 1: # запустить сервер в этом процессе
    server()
elif mode == 2: # запустить клиента в этом процессе
    client('client:process=%s' % os.getpid())
else: # запустить 5 потоков-клиентов
    for i in range(5):
        Thread(target=client, args=('client:thread=%s' % i,)).start()