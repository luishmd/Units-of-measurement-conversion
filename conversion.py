__author__ = 'Luis Domingues'

import conversion_GUI as conv_GUI
import conversion_lib as conv_lib
import tkinter as tk # Python3

dic_main = conv_lib.init()
root = tk.Tk()
my_gui = conv_GUI.Conversion_script_GUI(root,dic_main)
root.mainloop()
