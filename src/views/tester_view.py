import tkinter as tk
from tkinter import ttk
from src.views.abstract_view import AbstractView
from src.logger import DogovLogger

log = DogovLogger.get_logger()

class TesterView(AbstractView):
    
    def _init_logic(self):
        pass

    def _build_gui(self):
        self.main_frame.grid(column=0, row=0)

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


        self.toolRibbon    = ttk.Frame(self.main_frame, style='mRRed.TFrame',borderwidth=4)
        self.subtoolRibbon = ttk.Frame(self.main_frame, style='mRBlue.TFrame',borderwidth=4)
        self.titleFrame    = ttk.Frame(self.main_frame, style='mPurple.TFrame',borderwidth=4)
        self.contentFrame  = ttk.Frame(self.main_frame, style='mPink.TFrame',borderwidth=4)
        self.optionRibbon  = ttk.Frame(self.main_frame, style='mSCyan.TFrame',borderwidth=4)
        self.statusFrame   = ttk.Frame(self.main_frame, style='mVYellow.TFrame',borderwidth=4)
        self.infoFrame     = ttk.Frame(self.main_frame, style='mGreen.TFrame',borderwidth=4)

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
    
    class DummyController:
        pass
    dc = DummyController()

    root = tk.Tk()
    root.geometry("800x600")
    root.title("Fill Out Contract Form")
    app = TesterView(root, dc) 
    app.show()
    root.mainloop()