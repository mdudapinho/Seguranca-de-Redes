"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
################           Servidor AS            ################
##################################################################
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import simplejson as json
import ASS_messages_operations as ass_mo
import sys
sys.path.insert(1, '../src/')
import file_operations as fo

DEBUG = True
hostName = "localhost"
serverPort = 8080
clients =[]
clients_file = "../src/clients.txt"

class Client:
    def __init__(self, id_c, kc):
        self.id_c = id_c
        self.kc = kc


def HTTP_HEADER(self):
    print("_____________________")
    print("___Header___")
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    print("__________")

def HTTPPage(self, res):
    self.wfile.write(bytes("<html><head><title>AS Server</title></head>", "utf-8"))
    self.wfile.write(bytes("<p>-Request: %s</p>" % self.path, "utf-8"))
    self.wfile.write(bytes("<body>", "utf-8"))
    #self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
    #self.wfile.write(bytes("</body></html>", "utf-8"))
    self.wfile.write(bytes("<p>Response: %s</p></html>" % res, "utf-8"))

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        HTTP_HEADER(self)

        clients = fo.ReadClientsFile()

        #id_c, service, time_requested, n1, kc = ass_mo.readM1(self.path)

        r = ass_mo.ReadM1(self.path, clients)

        if(r["status"]):
            id_c = r["data"]["id_c"]
            service = r["data"]["service"]
            time_requested = r["data"]["time_requested"]
            n1 = r["data"]["n1"]
            kc = r["data"]["clientKey"]
            #id_c, service, time_requested, n1, kc = r["data"]

            msg2 = ass_mo.CreateM2(id_c, service, time_requested, n1, kc)
            res = { 'status': True, 'message':msg2}
            print("RESPONSE:")
            print("\tstatus: ", res['status'])
            print("\tmessage: ")
            print("\t\tm2_1: ")
            print("\t\t\t ciphertext: ", res['message']['m2_1']['ciphertext'])
            print("\t\t\t tag: ", res['message']['m2_1']['tag'])
            print("\t\t\t nonce: ", res['message']['m2_1']['nonce'])
            print("\t\tm2_2: ")
            print("\t\t\t ciphertext: ", res['message']['m2_2']['ciphertext'])
            print("\t\t\t tag: ", res['message']['m2_2']['tag'])
            print("\t\t\t nonce: ", res['message']['m2_2']['nonce'])

            #HTTPPage(self, res)
            self.request.send(json.dumps(res).encode('utf-8'))

        else:
            res = { 'status': False, 'message': r["data"]}
            print("Response:", res)
            self.request.send(json.dumps(res).encode('utf-8'))
        print("_________________")

def main():
    clients = fo.ReadClientsFile()

    if(len(clients) == 0):
        print("There's no clients resgistered yet")

    with HTTPServer((hostName, serverPort), MyServer) as webServer:
        print("AS Server started http://%s:%s" % (hostName, serverPort))
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")

main()
