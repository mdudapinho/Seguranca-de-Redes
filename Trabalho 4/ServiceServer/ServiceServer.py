"""
##################################################################
################    UTFPR - SEGURANCA DE REDES    ################
################    MARIA EDUARDA REBELO PINHO    ################
################        Servidor Servicos         ################
##################################################################
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import ServiceServer_messages_operations as ss_mo

DEBUG = True
hostName = "localhost"
serverPort = 9000
services =[]
services_file = "../src/services.txt"


def ReadServicesFile():
    fh = open(services_file).readlines()
    for line in fh:
        id_s_  = line[:-1]
        services.append(id_s_)

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
        #id_c, service, time_requested, n1, kc = ass_mo.readM1(self.path)

        r = ss_mo.ReadM5(self.path, services)

        if(r["status"]):
            # data = {'n3': n3, 'k_c_s': k_c_s}
            n3 = r['data']['n3']
            k_c_s = r['data']['k_c_s']
            t_a = r['data']['t_a']
            msg5 = ss_mo.CreateM6(n3, k_c_s, t_a)
            res = { 'status': True, 'message': msg5}

            print("RESPONSE:")
            print("\tstatus: ", res['status'])
            print("\tmessage: ")
            print("\t\tm5: ")
            print("\t\t\t ciphertext: ", res['message']['ciphertext'])
            print("\t\t\t tag: ", res['message']['tag'])
            print("\t\t\t nonce: ", res['message']['nonce'])
            self.request.send(json.dumps(res).encode('utf-8'))

        else:
            res = { 'status': False, 'message':r["data"]}
            print("Response:", res)
            self.request.send(json.dumps(res).encode('utf-8'))
        print("_________________")

def main():
    ReadServicesFile()

    if(len(services) == 0):
        print("There's no service resgistered yet")

    with HTTPServer((hostName, serverPort), MyServer) as webServer:
        print("Services Server started http://%s:%s" % (hostName, serverPort))
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")

main()
