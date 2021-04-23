"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
################        Client Operations         ################
##################################################################
"""
import requests
import json


DEBUG = True
as_url = "http://localhost:8080/"
tgs_url = "http://localhost:8000/"
service_url = "http://localhost:9000/"

def ToQuery(parameters):
    query_string = '?'
    for key in parameters.keys():
        query_string += str(key).replace(' ', '%20')
        query_string += '='
        query_string += str(parameters[key]).replace(' ', '+')
        query_string += '&'

    return query_string

def ClientToASRequest(message):
    message1 = ToQuery(message)
    request_url = as_url + message1

    response = False
    try:
        r = requests.get(request_url)
        response = json.loads(r.content.decode('utf-8'))
    except:
        response = { 'status': False, 'message': "AS Server: Error while performing GET"}

    return response

def ClientToTGSRequest(message):
    message3 = ToQuery(message)
    request_url = tgs_url + message3
    response = False

    try:
        r = requests.get(request_url)
        response = json.loads(r.content.decode('utf-8'))
    except:
        response = { 'status': False, 'message': "TGS Server: Error while performing GET"}

    return response

def ClientToServiceRequest(message):
    message5 = ToQuery(message)
    request_url = service_url + message5
    response = False

    try:
        r = requests.get(request_url)
        response = json.loads(r.content.decode('utf-8'))
    except:
        response = { 'status': False, 'message': "Service Server: Error while performing GET"}

    return response
