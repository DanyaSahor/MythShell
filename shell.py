import tkinter as tk
from tkinter import *
from tkinter import ttk

from tkinter import font
from tkinter.font import Font
import customtkinter

import os
import getpass
import sys
import configparser
import json


class shell:
    config = configparser.ConfigParser()
    config.read("bin/config/shell.ini")
    root_geometry = config["MythShell.Interface"]["root.geometry"]



# Добавление в системный патч
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bin.log import log
from bin.libraries.TerminalTab import TerminalTab
from bin.libraries.Interpreter import Interpreter
from bin.libraries.ExitDiaglogBox import ExitDiaglogBox
from bin.libraries.Utils import get_absolute_path
from bin.libraries.Config import MythShellConfig
from bin import launch


log(request_file="LAUNCHER", message=f"Launch MythShell from a directory: {os.getcwd()}")
log(request_file="LAUNCHER", message=f"Launching from: {__file__}")


class Terminal(tk.Frame):
    """ Terminal widget """

    def __init__(self, parent, text=None, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self.splashText = text

        Interpreter.init_backends()
        self.TerminalConfig = MythShellConfig.get_default()

        if "Cascadia Code SemiLight" in font.families():
            self.TerminalConfig["fontfamily"] = "Cascadia Code SemiLight"
        else:
            self.TerminalConfig["fontfamily"] = "Consolas"

        MythShellConfig.set_default(self.TerminalConfig)

        # загрузка настроек
        if os.path.isfile(MythShellConfig.CONFIG_FILE):
            with open(MythShellConfig.CONFIG_FILE, "r") as f:
                try:
                    data = json.load(f)

                    for k in data.keys():
                        if k in self.TerminalConfig.keys():
                            self.TerminalConfig[k] = data[k]
                except:
                    pass

        MythShellConfig.set_config(self.TerminalConfig)

        ########################################################################
        # Create terminal tabs using notebook
        ########################################################################
        self.notebook = TerminalTab(self, self.splashText)
        self.notebook.pack(expand=True, fill=BOTH)

    def add_interpreter(self, *args, **kwargs):
        """ Add a new interpreter and optionally set as default """

        Interpreter.add_interpreter(*args, **kwargs)

    def run_command(self, cmd):
        """ Run command on current terminal tab """

        # Get the selected tab
        tab_id = self.notebook.select()

        # Get the associated terminal widget
        terminal = self.notebook.nametowidget(tab_id)
        terminal.run_command(cmd)

    def on_resize(self, event):
        """Auto scroll to bottom when resize event happens"""

        first_visible_line = self.TerminalScreen.index("@0,0")

        if self.scrollbar.get()[1] >= 1:
            self.TerminalScreen.see(END)
        elif float(first_visible_line) >  1.0:
            self.TerminalScreen.see(float(first_visible_line)-1)

        self.statusText.set(self.TerminalScreen.winfo_height())
def main():
    try:
        log(request_file="SHELL INTERFACE", message="Creating shell interface...")
        root = tk.Tk()
        root.title(f"{getpass.getuser()}@MythShell: ~{os.getcwd()}")
        root.geometry(shell.root_geometry)
        log(request_file="SHELL INTERFACE", message=f"Window size set(ROOT.GEOMETRY)={shell.root_geometry}")
        root.wm_attributes('-alpha', 0.1)

        terminal = Terminal(root)
        terminal.pack(expand=True, fill=BOTH)

        icon = PhotoImage(file=launch.LoadImg.icon)
        root.iconphoto(True, icon)

        ExitDiaglogBox(root, icon)
        root.mainloop()

    except IndexError:
        log(request_file="SHELL INTERFACE", message="Error to create shell interface. Stopped MythShell", mode="ERROR")

if __name__ == "__main__":
    main()