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
import hash as hs
import extractData as ed

PORT = 8080
HOST = ''       # '' for localhost
LOG = True
log_file = "log.txt"
MAX_CLIENTS = 10
MAX_DATA_RECV = 4096    # max number of bytes we receive at once

def checkRequest(request):
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

def printM(m):
    print(m)
    log_info(m)

class Server:
    def __init__(self):
        try:
            self.server_socket = socket(AF_INET, SOCK_STREAM)           # Create a TCP socket
            self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Re-use the socket
            self.server_socket.bind((HOST, PORT))                       # bind the socket to a public/local host, and a port
            self.server_socket.listen(MAX_CLIENTS)                      # allowing up to MAX_CLIENTS client connections
        
        except error as e:
            message = 'Unable to create/re-use the socket. Error: ' + e
            printM(message)
            sys.exit(1)

        message = "Host Name: Localhost and Host address: 127.0.0.1 and Host port: " + str(PORT)
        printM(message)
        print("Server is ready to listen for clients")

    def listen_to_client(self):
        while True:
            # accepting client connection
            client_connection_socket, client_address = self.server_socket.accept()
            
            message = "Client IP address: "+str(client_address[0])+" and Client port number: " + str(client_address[1])
            printM(message)
            
            client_details_log = ed.getClientDetailsLog(client_address, client_connection_socket)
            printM(client_details_log)
            
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
            if(checkRequest(client_request)):
                port_number, url_connect = ed.getURLData(client_request)
                web_server_response = self.ClientTCP(client_connection_socket, port_number, client_address, url_connect, client_request)
                client_connection_socket.send(web_server_response)
                
                m = ed.getWebResponse(web_server_response)
                message = "Client with port: " + str(client_address[1]) + " received from web server: \n"+ m
                printM(message)
                
            else:
                client_connection_socket.send("UNAUTHORIZED ACCESS!")
                message = "Client with port: " + str(client_address[1]) + " connection closed"
                log_info(message)
                print(message)
        else:
            # a blank request call was made by a client
            client_connection_socket.send("")
            #client_connection_socket.close()
            message = "Client with port: " + str(client_address[1]) + " connection closed"
            log_info(message)
            print(message)
         
        end_time = time.time()
        message = "Client with port: " + str(client_address[1]) + " Time Elapsed(RTT): " + str(end_time - start_time) + " seconds \n"
        message += "Client with port: " + str(client_address[1]) + " connection closed \n"
        log_info(message)
        client_connection_socket.close()

    def ClientTCP(self, client_connection_socket, port_number, client_address, url_connect, client_request):
        
        web_response = ""
        try:
            # creating the socket from the proxy server and defining timeout 
            proxy_connection_socket = socket(AF_INET, SOCK_STREAM)
            proxy_connection_socket.settimeout(2)   
        except error as e:
            message = 'Unable to create the socket. Error: %s' % e
            printM(message)
        try:    
            proxy_connection_socket.connect((url_connect, port_number))
            proxy_connection_socket.send(client_request)
            m = ed.getRequestData(client_request)
            message = "Client with port: " + str(client_address[1]) + " generated request to web server as: \n"+ m
            printM(message)

            webServer_log = ed.getWebServerDetailsLog(url_connect, port_number, client_connection_socket)
            printM(webServer_log)

            web_server_response_append = ""
            timeout_flag = False
            while True:
                try:
                    web_server_response = proxy_connection_socket.recv(MAX_DATA_RECV)
                except timeout:
                    # a time out occurred on waiting for server response so break out of loop
                    if len(web_server_response_append) <= 0:
                        timeout_flag = True
                    break
                if len(web_server_response) > 0:
                    web_server_response_append += web_server_response
                else:
                    # all the data has been received so break out of the loop
                    break
            
            if timeout_flag:
                web_response = "408 Request timeout\r\n"
            else:
                web_response = web_server_response_append
            
            proxy_connection_socket.close()
            
        except error as e:
            # sending page not found response to client
            error_message = "404 Not Found\r\n"
            message = "Client with port: " + str(client_address[1]) + " Following error occurred : "+str(e) + "\n" \
                    "Client with port: " + str(client_address[1]) + " response sent: " + error_message
            printM(message)
            web_response = error_message

        return web_response
    
if __name__ == "__main__":
    if(hs.CREATENEWHASH):
        hs.createHashFile()
    if(hs.checkApplicationIntegrity()):
        server = Server()           # creating the instance of the server class
        server.listen_to_client()   # calling the listen to Client call
    else:
        print("APPLICATION INTEGRITY COMPROMISED!")
