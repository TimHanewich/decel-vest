def log(txt:str):
    print(txt)
    f = open("log.txt", "a")
    f.write(txt + "\n")
    f.close()

def retrieve_logs():
    try:
        f = open("log.txt", "r")
        return f.read()
    except:
        return ""