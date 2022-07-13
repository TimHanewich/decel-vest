import time

def log(txt:str, ticks:bool=True):
    print(txt)
    f = open("log.txt", "a")

    # Should the tick piece (tp) be written?
    tp = ""
    if ticks == True:
        tp = str(time.ticks_ms()) + "_"

    # Write and close
    f.write(tp + txt + "\n")
    f.close()

def retrieve_log():
    try:
        f = open("log.txt", "r")
        return f.read()
    except:
        return ""