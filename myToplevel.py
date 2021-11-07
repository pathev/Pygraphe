from tkinter import Toplevel

class MyToplevel(Toplevel):

    def __init__(self,master,width=200,height=60,bg="white"):
        Toplevel.__init__(self,master=master,width=width,height=height,bg=bg)
        x=str(self.master.winfo_rootx()+self.master.winfo_width()//2-width//2)
        y=str(self.master.winfo_rooty()+self.master.winfo_height()//2-height//2)
        self.geometry("+"+x+"+"+y)
        self.wait_visibility()
        grab=False
        while not grab:
            try:
                self.grab_set()
                grab=True
            except:
                grab=False

    def deiconify(self):
        x=str(self.master.winfo_rootx()+self.master.winfo_width()//2-self.winfo_width()//2)
        y=str(self.master.winfo_rooty()+self.master.winfo_height()//2-self.winfo_height()//2)
        self.geometry("+"+x+"+"+y)
        Toplevel.deiconify(self)
        grab=False
        while not grab:
            try:
                self.grab_set()
                grab=True
            except:
                grab=False

    def withdraw(self):
        Toplevel.withdraw(self)
        self.grab_release()
