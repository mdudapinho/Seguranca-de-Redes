clients_file = "../src/clients.txt"
users_file = "./src/clients.txt"
services_file = "../src/services.txt"
services_file_users = "./src/services.txt"

class User:
    def __init__(self, user, hashed_password):
        self.user = user
        self.hashed_password = hashed_password

class Client:
    def __init__(self, id_c, kc):
        self.id_c = id_c
        self.kc = kc

def saveUserInFile(user):
    f = open(users_file,'a')
    f.write(user.user + ', ')
    f.write(user.hashed_password)
    f.write('\n')
    f.close()

def readUserFromFile():
    users = []
    fh = open(users_file).readlines()
    for line in fh:
        row = line.split(',')
        user_, hashed_password = [i.strip() for i in row]
        new_user = User(user_, hashed_password)
        users.append(new_user)

    return users

def ReadClientsFile():
    clients =[]
    fh = open(clients_file).readlines()
    for line in fh:
        row = line.split(',')
        id_c_, kc_ = [i.strip() for i in row]
        new_client = Client(id_c_, kc_)
        clients.append(new_client)

    return clients

def ReadServicesFile():
    services = []
    fh = open(services_file).readlines()
    for line in fh:
        id_s_  = line[:-1]
        services.append(id_s_)
    return services


def ReadServicesFileFromUser():
    services = []
    fh = open(services_file_users).readlines()
    for line in fh:
        id_s_  = line[:-1]
        services.append(id_s_)
    return services
