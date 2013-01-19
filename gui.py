from Tkinter import *
import spam
import load_data

data = load_data.Data()
processor = spam.SpamProcessor()
current_message = ""

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
    score_label.text = str(n) + " " + str(lbl)

def next():
    current_message = data.getNext()
    score()

def analyse():
    pass

root = Tk()
root.wm_title("Refugees United (Rewired State 2013)")
root.minsize(640,480)

#main_frame = Tk.Frame(master=root)
#main_frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1, )

label = Label(master=root, text="Spam(er) detection system")
label.pack()

msg = Label(master=root, text=current_message)
msg.pack(side=TOP, fill=X, expand=1)

score_label = Label(master=root, text="")
score_label.pack()

buttonFrame = Frame(master=root)

b = Button(buttonFrame, text="Spam", command=spam)
b.grid(row=0, column=0)
b.pack()
b2 = Button(buttonFrame, text="Not Spam", command=notspam)
b2.grid(row=0, column=1)
b2.pack()
b3 = Button(buttonFrame, text="Next", command=next)
b3.grid(row=0, column=2)
b3.pack()
b4 = Button(buttonFrame, text="Analyse", command=analyse)
b4.grid(row=0, column=3)
b4.pack()

buttonFrame.pack()
mainloop()