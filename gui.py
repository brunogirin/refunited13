from Tkinter import *
import spam
import load_data

data = load_data.Data()
processor = spam.SpamProcessor()
current_message = data.getNext()
details = None

def spam():
    processor.flag_as_bad(current_message)
    next()

def notspam():
    processor.flag_as_good(current_message)
    next()

def score():
    score = processor.score(current_message)
    n = score[0]
    lbl = score[1]
    details = score[2]
    print details
    score_label.config(text=str(n) + " " + str(lbl))
    score_label.update_idletasks()

def next():
    current_message = str(data.getNext())
    msg.config(text=current_message)
    msg.update_idletasks()
    score()

def analyse():
#    msg.config(text=str(details))
#    msg.update_idletasks()
    pass

root = Tk()
root.wm_title("Refugees United (Rewired State 2013)")
root.minsize(640,480)

#main_frame = Tk.Frame(master=root)
#main_frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1, )

label = Label(master=root, text="Spam(mer) detection system")
label.pack()

msg = Label(master=root, text=current_message)
msg.pack(side=TOP, fill=X, expand=1)

score_label = Label(master=root, text="")
score_label.pack()

buttonFrame = Frame(master=root)

b = Button(buttonFrame, text="Spam", command=spam)
b.grid(row=0, column=0)
b.pack(side=LEFT)
b2 = Button(buttonFrame, text="Not Spam", command=notspam)
b2.grid(row=0, column=1)
b2.pack(side=LEFT)
b3 = Button(buttonFrame, text="Next", command=next)
b3.grid(row=0, column=2)
b3.pack(side=LEFT)
b4 = Button(buttonFrame, text="Analyse", command=analyse)
b4.grid(row=0, column=3)
b4.pack(side=LEFT)

buttonFrame.pack()
mainloop()