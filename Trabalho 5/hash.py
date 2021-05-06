import hashlib
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
