"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
################            PROXY SERVER          ################
##################################################################
"""

import sys, time, re
import threading
from socket import *
import hashlib

PORT = 8080
HOST = ''       # '' for localhost
LOG = True
log_file = "log.txt"
MAX_CLIENTS = 10
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
hash_file = "hash_file.txt"
this_file = "server.py"
CREATENEWHASH = False
USEHASH = False

def md5Hash(text):
    result = hashlib.md5(text.encode("utf-8")).hexdigest()
    return result[:16]

def checkApplicationIntegrity():
    if(USEHASH):
        fh = open(hash_file).read()
        th = open(this_file).read()
        hash_ = md5Hash(th)
        print("fh: ", fh)
        print("th: ", hash_)
        if(fh == hash_):
            return True
        return False
    return True

def createHashFile():
    fh = open(this_file).read()
    hash_ = md5Hash(fh)
    f = open(hash_file,'w+')
    f.write(hash_)
    f.close()

def checkMonitorando(request):
    ## TODO: hash of file
    monitorando = str(request).find("monitorando")
    if(monitorando == -1):
        return True
    return False

def log_info(message):
    if(LOG):
        logger_file = open(log_file, "a")
        logger_file.write(message)
        logger_file.write('\n')
        logger_file.close()

'''
def printM(m):
    print(m)
    if(LOG):
        log_info(m)
'''

def getClientDetailsLog(client_address, client_connection_socket):
    # getting relevant client details on the server side
    client_details_log = "******************** Client Details:- ********************\n"
    client_details_log += "Client host name: "+str(client_address[0]) + "\n"
    client_details_log += "Client port number: "+str(client_address[1]) + "\n"
    client_socket_details = getaddrinfo(str(client_address[0]), client_address[1])
    client_details_log += "Socket family: "+str(client_socket_details[0][0]) + "\n"
    client_details_log += "Socket type: "+str(client_socket_details[0][1]) + "\n"
    client_details_log += "Socket protocol: "+str(client_socket_details[0][2]) + "\n"
    client_details_log += "Timeout: "+str(client_connection_socket.gettimeout()) + "\n"
    client_details_log += "********************************************************"
    return client_details_log


def getWebServerDetailsLog(url_connect, port_number, client_connection_socket):
    # getting the web server response which is expected to be a file
    server_socket_details = getaddrinfo(url_connect, port_number)
    server_details_message = "*************** Web Server Details:- ***************\n"
    server_details_message += "Server host name: " + url_connect + "\n"
    server_details_message += "Server port number: " + str(port_number) + "\n"
    server_details_message += "Socket family: " + str(server_socket_details[0][0]) + "\n"
    server_details_message += "Socket type: " + str(server_socket_details[0][1]) + "\n"
    server_details_message += "Socket protocol: " + str(server_socket_details[0][2]) + "\n"
    server_details_message += "Timeout: " + str(client_connection_socket.gettimeout()) + "\n"
    server_details_message += "***************************************************"
    return server_details_message

def getURLData(client_request):
    http_part = client_request.split(' ')[1]
    # stripping the http part to get only the URL and removing the trailing / from the request
    double_slash_pos = str(http_part).find("//")
    url_connect = ""
    # if no http part to the url
    if double_slash_pos == -1:
        url_part = http_part[1:]
        # getting the www.abc.com part
        url_connect = url_part.split('/')[0]
    else:
        # if the url ends with / removing it e.g: www.example.com/
        if http_part.split('//')[1][-1] == "/":
            url_part = http_part.split('//')[1][:-1]
            # getting the www.abc.com part
            url_connect = url_part.split('/')[0]
        else:
            url_part = http_part.split('//')[1]
            # getting the www.abc.com part
            url_connect = url_part.split('/')[0]

    # checking if port number is provided
    client_request_port_start = str(url_part).find(":")
    # default port number
    port_number = 80
    # replacing all the non alphanumeric characters with under score
    if client_request_port_start == -1:
        pass
    else:
        port_number = int(url_part.split(':')[1])

    return port_number, url_connect, 

class Server:
    def __init__(self):
        try:
            self.server_socket = socket(AF_INET, SOCK_STREAM)           # Create a TCP socket
            self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Re-use the socket
            self.server_socket.bind((HOST, PORT))                       # bind the socket to a public/local host, and a port
            self.server_socket.listen(MAX_CLIENTS)                      # allowing up to MAX_CLIENTS client connections
        
        except error as e:
            message = 'Unable to create/re-use the socket. Error: ' + e
            print(message)
            log_info(message)
            sys.exit(1)

        message = "Host Name: Localhost and Host address: 127.0.0.1 and Host port: " + str(PORT)
        log_info(message)
        print(message)
        print("Server is ready to listen for clients")

    def listen_to_client(self):
        while True:
            # accepting client connection
            client_connection_socket, client_address = self.server_socket.accept()
            client_details_log = getClientDetailsLog(client_address, client_connection_socket)
            
            print(client_details_log)
            log_info(client_details_log)

            message = "Client IP address: "+str(client_address[0])+" and Client port number: " + str(client_address[1])
            print(message)
            log_info(message)

            # creating a new thread for every client
            d = threading.Thread(name=str(client_address), target=self.proxy_thread, args=(client_connection_socket, client_address))
            d.setDaemon(True)
            d.start()

        self.server_socket.close()

    def proxy_thread(self, client_connection_socket, client_address):
        """ method to create a new thread for every client connected """
 
        start_time = time.time()    # starting the timer to calculate the elapsed time
        client_request = client_connection_socket.recv(MAX_DATA_RECV)   # getting the client request
        
        if (client_request):
            if(checkMonitorando(client_request)):
                #message = "Client with port: " + str(client_address[1]) + " generated request: " + str(client_request).splitlines()[0]
                #log_info(message)
                #print(message)

                port_number, url_connect = getURLData(client_request)
                web_server_response = self.ClientTCP(client_connection_socket, port_number, client_address, start_time, url_connect, client_request)
            
            
                client_connection_socket.send(web_server_response)
                end_time = time.time()
                message = "Client with port: " + str(client_address[1]) + " Time Elapsed(RTT): " + str(end_time - start_time) + " seconds \n"
                log_info(message)
                print(message)
                print ("Response: " + web_server_response)
            
            else:
                client_connection_socket.send("UNAUTHORIZED ACCESS!\r\n\r\n")
                client_connection_socket.close()
                message = "Client with port: " + str(client_address[1]) + " connection closed"
                log_info(message)
                print(message)
        else:
            # a blank request call was made by a client
            client_connection_socket.send("")
            client_connection_socket.close()
            message = "Client with port: " + str(client_address[1]) + " connection closed"
            log_info(message)
            print(message)

    def ClientTCP(self, client_connection_socket, port_number, client_address, start_time, url_connect, client_request):
        try:
            # creating the socket from the proxy server
            proxy_connection_socket = socket(AF_INET, SOCK_STREAM)
            #proxy_connection_socket.settimeout(2)   
        except error as e:
            message = 'Unable to create the socket. Error: %s' % e
            print(message)
            log_info(message)    
        try:    
            
            proxy_connection_socket.connect((url_connect, port_number))
            
            proxy_connection_socket.send(client_request)
            message = "Client with port: " + str(client_address[1]) + " generated request to web server as: "+ str(client_request) + " \n"
            log_info(message)
            print(message)

            webServer_log = getWebServerDetailsLog(url_connect, port_number, client_connection_socket)
            print(webServer_log)
            log_info(webServer_log)

            web_server_response_append = ""
            receivingData = True
            while (receivingData):
                web_server_response = proxy_connection_socket.recv(MAX_DATA_RECV)
                if len(web_server_response) > 0:
                    web_server_response_append += web_server_response
                else:
                    receivingData = False

            #client_connection_socket.send(web_server_response_append)
            #end_time = time.time()
            #message = "Client with port: " + str(client_address[1]) + " Time Elapsed(RTT): " + str(end_time - start_time) + " seconds \n"
            #log_info(message)
            #print(message)
            #print ("Response: " + web_server_response_append)

            proxy_connection_socket.close()
            return web_server_response_append

        except error as e:
            # sending page not found response to client

            error_message = ""
            '''if str(e) == "timed out":
                error_message = "HTTP/1.1 404 Not Found\r\n"
                client_connection_socket.send("HTTP/1.1 408 Request timeout\r\n\r\n")
            else:'''
            error_message = "HTTP/1.1 404 Not Found\r\n\r\n"
            client_connection_socket.send('HTTP/1.1 404 not found\r\n\r\n')
            end_time = time.time()
            message = "Client with port: " + str(client_address[1]) + " Following error occurred : "+str(e) + "\n"
            log_info(message)
            message = "Client with port: " + str(client_address[1]) + " response sent: " + error_message + " \n"
            log_info(message)
            message = "Client with port: " + str(client_address[1]) + " Time Elapsed(RTT): " + str(
                end_time - start_time) + " seconds \n"
            log_info(message)
          
       # closing the client connection socket
        client_connection_socket.close()
        message = "Client with port: " + str(client_address[1]) + " connection closed \n"
        log_info(message)
       
    
if __name__ == "__main__":
    if(CREATENEWHASH):
        createHashFile()
    if(checkApplicationIntegrity()):
        print("Passou pro server!!")
        #server = Server()           # creating the instance of the server class
        #server.listen_to_client()   # calling the listen to Client call
    else:
        print("APPLICATION INTEGRITY COMPROMISED!")
