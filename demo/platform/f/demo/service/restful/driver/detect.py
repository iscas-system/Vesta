import os,re
import time
import datetime

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def main(name):
    while(True):
        cmd = "kubectl get pods"
        result = execCmd(cmd)
        result = result.split(os.linesep)
        for item in result:
            if item.find(name+'-driver'):
                if item.find('Completed'):
                    #print(time.time())
                    return time.time()
        sleep(1)

if __name__ == '__main__':
    main("spark-pi")
