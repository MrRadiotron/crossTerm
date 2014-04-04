#! /usr/bin/python

import sys, socket, time

logFile = "..\Dropbox\GroupController Logs\serverLog.log"

def serverLogWrite(text):
    log = open("..\Dropbox\GroupController Logs\serverLog.log", "a")
    log.write(text)
    sys.stdout.write(text)
    log.close()

def logWrite(text):
    log = open(logFile, "a")
    log.write(text)
    sys.stdout.write(text)
    log.close()

def refreshLogName():
    global logFile
    logFile = "..\Dropbox\GroupController Logs\GroupController " + time.strftime("%Y-%m-%d", time.localtime()) + ".log"
    serverLogWrite("Current log file is: " + logFile + '\n')

logWrite("\nTCP Server Start: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n\n")

refreshLogName()

host = ''
port = 502
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

while 1:
    serverLogWrite("\nready to accept: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
    
    client, address = s.accept()
    client.settimeout(10)

    refreshLogName()
    serverLogWrite("accept: "+ str(address) + "\n")
    logWrite("accepted: "+ str(address) + ", " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n\n")
    

    while 1:
        try:  
            data = client.recv(1)
        except:
            break
        
        if data == chr(5):
            serverLogWrite("data: ENQ\n")
            try:
                client.send(chr(6))#send ACK
            except:
                break
        elif data == chr(4):
            serverLogWrite("data: EOT\n")
            logWrite("\n") #send ACK
            try:
                client.send(chr(6))#send ACK
            except:
                break
            #break
        else:
             logWrite(data)

        #try:
        #    client.send(data)
        #except:
        #    break

    client.close()
