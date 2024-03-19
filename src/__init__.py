import json
def getConfig(key):
    # add your configuration path
    con_file=r"c:\\Users\muthu\playground\e-commerce\config.json"
    file=open(con_file,'r')
    config=json.loads(file.read())
    file.close()
    if key in config:
        return config[key]
    else:
        raise Exception("ey {} is not found".format(key))