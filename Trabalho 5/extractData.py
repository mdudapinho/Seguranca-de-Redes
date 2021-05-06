def getClientDetailsLog(client_address, client_connection_socket):
    # getting relevant client details on the server side
    client_details_log = "******************** Client Details:- ********************\n"
    client_details_log += "Client host name: "+str(client_address[0]) + "\n"
    client_details_log += "Client port number: "+str(client_address[1]) + "\n"
    # client_socket_details = getaddrinfo(str(client_address[0]), client_address[1])
    # client_details_log += "Socket family: "+str(client_socket_details[0][0]) + "\n"
    # client_details_log += "Socket type: "+str(client_socket_details[0][1]) + "\n"
    # client_details_log += "Socket protocol: "+str(client_socket_details[0][2]) + "\n"
    # client_details_log += "Timeout: "+str(client_connection_socket.gettimeout()) + "\n"
    client_details_log += "********************************************************"
    return client_details_log

def getWebServerDetailsLog(url_connect, port_number, client_connection_socket):
    # getting the web server response which is expected to be a file
    #server_socket_details = getaddrinfo(url_connect, port_number)
    server_details_message = "*************** Web Server Details:- ***************\n"
    server_details_message += "Server host name: " + url_connect + "\n"
    server_details_message += "Server port number: " + str(port_number) + "\n"
    # server_details_message += "Socket family: " + str(server_socket_details[0][0]) + "\n"
    # server_details_message += "Socket type: " + str(server_socket_details[0][1]) + "\n"
    # server_details_message += "Socket protocol: " + str(server_socket_details[0][2]) + "\n"
    # server_details_message += "Timeout: " + str(client_connection_socket.gettimeout()) + "\n"
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

def getRequestData(client_request):
    r = str(client_request).split("\r\n")
    m = "\t" + r[0] + \
        "\n\t" + r[1] + \
        "\n\t" + r[2] + \
        "\n\t" + r[3] + \
        "\n\t" + r[4] + \
        "\n\t" + r[5] + \
        "\n\t" + r[6] + \
        "\n\t" + r[7] + \
        "\n\t" + r[8] + \
        "\n\t" + r[9] + \
        "\n\t" + r[10] 
    return m

def getWebResponse(web_server_response):
    r = str(web_server_response).split("\r\n")
    m = "\t" + r[0]
    if(len(r) > 2):
        m += "\n\t" + r[1] + \
            "\n\t" + r[2] + \
            "\n\t" + r[3] + \
            "\n\t" + r[4] + \
            "\n\t" + r[5] + \
            "\n\t" + r[6] + \
            "\n\t" + r[7] + \
            "\n\t" + r[8] + \
            "\n\t" + r[9]  
    return m