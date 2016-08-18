from Tkinter import *

root = Tk()
top_frame = Frame(root)
top_frame.pack()
bottom_frame = Frame(root)
bottom_frame.pack(side=BOTTOM)

button1 = Button(top_frame, text="Bitchin1", fg = "black")
button2 = Button(top_frame, text="Bitchin2", fg = "blue")
button3 = Button(top_frame, text="Bitchin3", fg = "green")
button4 = Button(bottom_frame, text="Bitchin4", fg = "purple")

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)


root.mainloop()