#!/usr/bin/python3

from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog 
import os 


class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

def find_file():
    name = filedialog.askopenfilename() 
    return name



def answer():
    showerror("Answer", "Sorry, no answer available")

def callback():
    if askyesno('Verify', 'Really quit?'):
        showwarning('Yes', 'Not yet implemented')
    else:
        showinfo('No', 'Quit has been cancelled')


def allstates(): 
    print(list(lng.state()), list(tgl.state()))
    
def call_assembler11():
    string = 'python ./assemble11.py --outdir=' + outdir.get()+ ' --f_inference="' + f_inference.get() +'" --fragnum=' + fragnum.get() +' --overlap=0.4'
    print(string)
    os.system(string)
    os.system('echo "report"')
    
    report = 'python report.py --outdir=' + outdir.get()+ ' --assembled=$foo/$tar/recons.txt --trace=$foo/$bar/test.trace0 --labels=$foo/$bar/test.label --mode=none--bias=none'



def get_header_field():
    
    outdir.set(outdirB.get())
    
    f_inference.set(f_inferenceB.get())
    
    fragnum.set(fragnumB.get())


if __name__ == '__main__':
    root = Tk()

    
    #header
    Label(root, text="outdir").grid( row=0 )
    Label(root, text="f_inference").grid( row=1 )
    Label(root, text="fragnum").grid( row=2 )

    outdirB = Entry(root)
    f_inferenceB = Entry(root)
    fragnumB = Entry(root)

    outdirB.grid( row=0, column= 2, columnspan=5)
    f_inferenceB.grid( row=1, column =2,  columnspan = 5)
    fragnumB.grid( row=2, column = 2, columnspan = 5)
    
    outdir = StringVar()
    f_inference = StringVar()
    fragnum = StringVar()

    
    Button(root, text='Get arguments', command=get_header_field).grid( row=3, columnspan=4)

    lng = Checkbar(root, ['Assemble9', 'Assemble10', 'Assemble11'])
    tgl = Checkbar(root, ['English','German'])
    lng.grid(row = 4 , columnspan=3)
    tgl.grid(row=5, columnspan=3)
    lng.config(relief=GROOVE, bd=2)

    
    
    
    Button(root, text='Assemble!', command=call_assembler11).grid( row=9, columnspan=4)

    Button(root, text='Quit', command=root.destroy).grid( row=10, column=1)
    
    Button(root, text='Peek', command=allstates).grid( row=10, column=3)


    Button(text='Answer', command=answer).grid(row=10,columnspan=5)


    #pack(side=RIGHT)
    mainloop( )