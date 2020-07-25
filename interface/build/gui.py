from tkinter import Button, Entry, Frame, Image, IntVar, Label, Menu, TclError, Tk, Toplevel, ttk

from .record_manager import RecordManager
from .constants import buttons_dict


class DogBarkingInterface(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("{}x{}".format(self.winfo_screenwidth(),
                                            self.winfo_screenheight()))
        self.title("JBM - Jojo Bark Messenger")
        self.option_add("*Font", "Times 10")
        try:
            try:
                self.tk.call("tk_getOpenFile", "-foobarbaz")
            except TclError:
                pass
            self.tk.call("set", "::tk::dialog::file::showHiddenVar", "0")
        except:
            pass
        img = Image("photo", file = "jojo.gif")
        self.tk.call("wm", "iconphoto", self._w, img)
        self.data = None
        self.frames = {}
        self.record_manager = RecordManager()
        self.init_start_page()
        self.show_frame(MainPage)
    

    def client_exit(self, event = None):
        exit()


    def init_start_page(self):
        frame = MainPage(self)
        self.frames[MainPage] = frame
        self.frames[MainPage].draw_buttons()

    
    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class MainPage(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid(row = 0, column = 1)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.record_manager = parent.record_manager

    
    def draw_buttons(self):
        self.frame = Frame(self)
        self.frame.grid(row = 10, column = 10, rowspan = 10, columnspan = 10)    
        entries = {}
        for button, button_dict  in buttons_dict.items():            
            Label(self.frame, text = button_dict["label"]).pack()
            entries[button] = Entry(self.frame)
            entries[button].insert(1, button_dict["default"])
            entries[button].pack()
        record_button = Button(self, text = "REC", 
                command = lambda: self.record_manager.continuous_recording(entries))
        record_button.grid(row = 10, column = 0, columnspan = 5)        
        # self.update()