__author__ = 'Luis Domingues'

import conversion_lib as conv_lib
try:
    import Tkinter as tk # Python2
except ImportError:
    import tkinter as tk # Python3


class Conversion_script_GUI(object):

    def __init__(self, master, dic):
        self.master = master
        self.dic = dic

        # Constants
        self.NUM_DEC = 6
        self.SCIENTIFIC_THRESHOLD = 1000
        self.DEFAULT_FONT = 'Helvetica 12'
        self.LABEL_FONT = 'Helvetica 12 bold'

        # Title
        self.master.title("Conversion tool")

        # Fonts, sizes and colourssizes
        #default_font = 'Helvetica 12'
        #label_font = 'Helvetica 12 bold'
        self.master.option_add("*Font", self.DEFAULT_FONT)
        self.master.option_add("*Text.Background", "white")
        self.master.option_add("*Entry.Background", "white")
        self.master.option_add("*Label.Font", self.LABEL_FONT)
        self.master.option_add("*Label.Background", "light grey")
        self.master.option_add("*Frame.Background", "light grey")
        self.master.config(background="light grey")

        # Initialise tracer variables
        self.conv_type = tk.StringVar()
        self.conv_from = tk.StringVar()
        self.conv_to = tk.StringVar()

        # Conversion types
        options = list(self.get_conversion_types(dic))
        label_to = tk.Label(self.master, text="Type: ")
        label_to.grid(row=1,column=0)
        self.conv_type.set(options[0]) # default value
        menu_conv = tk.OptionMenu(self.master, self.conv_type, *options)
        menu_conv.grid(row=1,column=1)
        self.conv_type.trace("w",self.show_frame)

        self.frames = self.create_frames(dic)
        self.show_frame()

        # Input entry
        label_from = tk.Label(self.master, text="Amount  ")
        label_from.grid(row=2,column=0, sticky="W")
        self.entry_from = tk.Entry(self.master, width=15)
        self.entry_from.grid(row=2,column=1)
        label_white_space = tk.Label(self.master, text="   ")
        label_white_space.grid(row=2,column=2, sticky="NSEW")

        # Output text
        label_to = tk.Label(self.master, text="Result  ")
        label_to.grid(row=3,column=0, sticky="W")
        self.text_to = tk.Text(self.master, height=1, width=15)
        self.text_to.grid(row=3,column=1)
        label_white_space = tk.Label(self.master, text="   ")
        label_white_space.grid(row=2,column=2, sticky="NSEW")

        # Convert button
        convert_button = tk.Button(self.master, text ="Press to convert", font=self.LABEL_FONT, command = self.convert )
        convert_button.grid(row=0,column=0, columnspan= 4,sticky="NSEW")
        self.master.bind('<Return>', self.convert)

    def get_conversion_types(self,dic):
        types = dic.keys()
        return types

    def get_conversion_units(self,type):
        if not type in ["temperature","speed","pace"]:
            units = self.dic[type].keys()
        else:
            units = self.dic[type][0].keys()
        return units

    def get_default(self,type):
        defaults_dic = conv_lib.get_default_units()
        try:
            default_unit = defaults_dic[type]
        except:
            default_unit = "no unit"
        return default_unit

    def float_to_str(self,num):
        '''
        Converts a float to a string with the desired precision and format
        '''
        if num > self.SCIENTIFIC_THRESHOLD or num < float(1.0/self.SCIENTIFIC_THRESHOLD):
            filter = "{:." + str(self.NUM_DEC) + "e}"
        else:
            filter = "{:." + str(self.NUM_DEC) + "f}"
        num_str = filter.format(num)
        return num_str

    def convert(self, *args):
        try:
            num = float(self.entry_from.get())
            type = self.conv_type.get()
            unit_from = self.conv_from.get()
            unit_to = self.conv_to.get()
            dic = self.dic
            out = conv_lib.conv(num,type,unit_from,unit_to,dic)
            out_str = self.float_to_str(out)
            self.text_to.delete('1.0',tk.END)
            self.text_to.insert(tk.END,out_str)
        except ValueError:
            self.text_to.delete('1.0',tk.END)
            out = "NaN"
            self.text_to.insert(tk.END,out)

    def show_frame(self, *args):
        option = self.conv_type.get()
        self.conv_from.set(self.get_default(option)) # default value
        self.conv_to.set(self.get_default(option)) # default value
        frame = self.frames[self.conv_type.get()]
        frame.tkraise()

    def create_frames(self,dic):
        frames = {}
        options = list(self.get_conversion_types(dic))
        for option in options:
            my_frame = tk.Frame(self.master)
            my_frame.grid(row=2, column=3, rowspan=2, sticky='news')
            units = list(self.get_conversion_units(option))

            self.conv_from.set(self.get_default(option)) # default value
            menu_from = tk.OptionMenu(my_frame, self.conv_from, *units)
            menu_from.grid(row=0,column=0,sticky="W")
            self.conv_to.set(self.get_default(option)) # default value
            menu_to = tk.OptionMenu(my_frame, self.conv_to, *units)
            menu_to.grid(row=1,column=0,sticky="W")

            frames[option] = my_frame
        return frames


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Conversion_script_GUI(root)
    root.mainloop()
