"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
################          Servidor TGS            ################
##################################################################
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import TGS_messages_operations as tgs_mo
import sys
sys.path.insert(1, '../src/')
import file_operations as fo

DEBUG = True
hostName = "localhost"
serverPort = 8000
services =[]
services_file = "../src/services.txt"


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

        services = fo.ReadServicesFile()
        #id_c, service, time_requested, n1, kc = ass_mo.readM1(self.path)

        r = tgs_mo.ReadM3(self.path, services)

        if(r["status"]):
            #id_c, n2, k_c_tgs, serviceKey, time_requested
            id_c = r["data"]["id_c"]
            n2 = r["data"]["n2"]
            k_c_tgs = r["data"]["k_c_tgs"]
            k_s = r["data"]["k_s"]
            time_requested = r["data"]["time_requested"]

            msg4 = tgs_mo.CreateM4(id_c, n2, k_c_tgs, k_s, time_requested)
            res = { 'status': True, 'message':msg4}

            print("RESPONSE:")
            print("\tstatus: ", res['status'])
            print("\tmessage: ")
            print("\t\tm4_1: ")
            print("\t\t\t ciphertext: ", res['message']['m4_1']['ciphertext'])
            print("\t\t\t tag: ", res['message']['m4_1']['tag'])
            print("\t\t\t nonce: ", res['message']['m4_1']['nonce'])
            print("\t\tm4_2: ")
            print("\t\t\t ciphertext: ", res['message']['m4_2']['ciphertext'])
            print("\t\t\t tag: ", res['message']['m4_2']['tag'])
            print("\t\t\t nonce: ", res['message']['m4_2']['nonce'])

            self.request.send(json.dumps(res).encode('utf-8'))

        else:
            res = { 'status': False, 'message':r["data"]}
            print("Response:", res)
            self.request.send(json.dumps(res).encode('utf-8'))
        print("_________________")

def main():
    services = fo.ReadServicesFile()

    if(len(services) == 0):
        print("There's no service resgistered yet")

    with HTTPServer((hostName, serverPort), MyServer) as webServer:
        print("TGS Server started http://%s:%s" % (hostName, serverPort))
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")

main()
