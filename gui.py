from Tkinter import *


def spam():
    pass

def notspam():
    pass

def score():
    pass

root = Tk()
root.wm_title("Refugees United (Rewired State 2013)")
root.minsize(640,480)

#main_frame = Tk.Frame(master=root)
#main_frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1, )

label = Label(master=root, text="Spam(er) detection system")
label.pack()

msg = Label(master=root, text="Spam(er) detection system")
msg.pack(side=TOP, fill=X, expand=1)

buttonFrame = Frame(master=root)

b = Button(buttonFrame, text="Spam", command=spam)
b.pack()
b2 = Button(buttonFrame, text="Not Spam", command=spam)
b2.pack()
b3 = Button(buttonFrame, text="Score", command=spam)
b3.pack()
b4 = Button(buttonFrame, text="Analyse", command=spam)
b4.pack()

buttonFrame.pack()
mainloop()