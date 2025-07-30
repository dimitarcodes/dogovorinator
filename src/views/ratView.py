import tkinter as tk
from tkinter import ttk

class MainFrame:
    def __init__(self,parent):
        self.frame = ttk.Frame(parent,padding='3 3 12 12')
        self.frame.grid(column=0, row=0)

        self.mRRed = ttk.Style()
        self.mRBlue = ttk.Style()
        self.mPurple = ttk.Style()
        self.mPink = ttk.Style()
        self.mSCyan = ttk.Style()
        self.mVYellow = ttk.Style()
        self.mGreen  = ttk.Style()

        self.mRRed.configure("mRRed.TFrame",background="#E61E50")
        self.mRBlue.configure("mRBlue.TFrame",background="#0F69AF")
        self.mPurple.configure("mPurple.TFrame",background="#503291")
        self.mPink.configure("mPink.TFrame",background="#EB3C96")
        self.mSCyan.configure("mSCyan.TFrame",background="#2BDECD")
        self.mVYellow.configure("mVYellow.TFrame",background="#FFC832")
        self.mGreen.configure("mGreen.TFrame",background="#149B5F")


        self.toolRibbon    = ttk.Frame(self.frame, style='mRRed.TFrame',borderwidth=4)
        self.subtoolRibbon = ttk.Frame(self.frame, style='mRBlue.TFrame',borderwidth=4)
        self.titleFrame    = ttk.Frame(self.frame, style='mPurple.TFrame',borderwidth=4)
        self.contentFrame  = ttk.Frame(self.frame, style='mPink.TFrame',borderwidth=4)
        self.optionRibbon  = ttk.Frame(self.frame, style='mSCyan.TFrame',borderwidth=4)
        self.statusFrame   = ttk.Frame(self.frame, style='mVYellow.TFrame',borderwidth=4)
        self.infoFrame     = ttk.Frame(self.frame, style='mGreen.TFrame',borderwidth=4)

        self.toolRibbon.grid(column=0,row=0)
        self.subtoolRibbon.grid(column=0,row=1)
        self.titleFrame.grid(column=1,row=1)
        self.contentFrame.grid(column=1,row=2)
        self.optionRibbon.grid(column=1,row=3)
        self.statusFrame.grid(column=1,row=4)
        self.infoFrame.grid(column=4,row=1)

        self.test = ttk.Label(self.optionRibbon, text='cyan test')
        self.test.pack()

        self.test2 = ttk.Label(self.contentFrame, text='pink test')
        self.test2.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("test")

    main = MainFrame(root)
    root.mainloop()