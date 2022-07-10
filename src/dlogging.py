import time

def log(txt:str):
    print(txt)
    f = open("log.txt", "a")
    f.write(str(time.ticks_ms()) + "-" + txt + "\n")
    f.close()

def retrieve_log():
    try:
        f = open("log.txt", "r")
        return f.read()
    except:
        return ""