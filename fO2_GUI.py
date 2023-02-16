


from matplotlib.backends.backend_tkagg import *
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter as tk  
from tkinter import ttk


    
def COMPandDISP():
    Tc = Tcinput.get()
    P = Pinput.get()
    a = str(round(fo2.NNO(Tc,P),2))
    b = str(round(fo2.FMQ(Tc,P),2))
    c = str(round(fo2.IW(Tc,P),2))
    d = str(round(fo2.MH(Tc,P),2))
    e = str(round(fo2.CoCoO(Tc,P),2))
    f = str(round(fo2.CCO(Tc,P),2))
    tk.Label(root,text=a).grid(row=1,column=4,padx=(30,0))
    tk.Label(root,text=b).grid(row=2,column=4,padx=(30,0))
    tk.Label(root,text=c).grid(row=3,column=4,padx=(30,0))
    tk.Label(root,text=d).grid(row=4,column=4,padx=(30,0))
    tk.Label(root,text=e).grid(row=5,column=4,padx=(30,0))
    tk.Label(root,text=f).grid(row=6,column=4,padx=(30,0))
   
root = tk.Tk()
root.title('Oxygen Fugacity')
root.geometry("500x400")


Tcinput = tk.IntVar(master=root,value=1200)  
Pinput = tk.IntVar(master=root,value=1)   
Temp_input = tk.Entry(root, width=15, borderwidth=5,textvariable=Tcinput)
Temp_input.grid(row=1,column=1)
P_input = tk.Entry(root, width=15, borderwidth=5,textvariable=Pinput)
P_input.grid(row=2,column=1)

Templabel = tk.Label(root,text='Temperature (C)').grid(row=1,column=0)
Plabel = tk.Label(root,text='Pressure (bar)').grid(row=2,column=0)

tk.Label(root, text='NNO').grid(row=1,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='FMQ').grid(row=2,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='IW').grid(row=3,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='MH').grid(row=4,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='CoCoO').grid(row=5,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='CCO').grid(row=6,column=3,padx=(30,0),pady=(10,10))

comp = tk.Button(root, text='Compute', command=lambda: COMPandDISP()).grid(row=3,column=1)


root.mainloop()
