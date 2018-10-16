import logging
import sys
critical = 50
err = 40
warn = 30
inf = 20
dbg = 10

class Log:
    def __init__(self,class_name=""):
        self.class_name = class_name
        logging.basicConfig(filename = "logs.log",format = "%(levelname)s: %(asctime)s: %(message)s")
        
    def log(self,val,message):
        logging.log(val,message)
        if val == 50:
            txt = "CRITICAL"
        elif val == 40:
            txt = "ERROR"
        elif val == 30:
            txt = "WARN"
        elif val == 20:
            txt = "INFO"
        elif val == 10:
            txt == "DEBUG"
        else:
            txt = ""
        sys.stderr.write(txt+" : "+ self.class_name+" : "message+"\n")
        if val == 50:
            exit()
            
