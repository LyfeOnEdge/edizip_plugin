#!/usr/bin/env python3
# Author: LyfeOnEdge

import os, subprocess, sys
import tkinter as tk

import style
from gui.widgets import basePlugin, basePage, button
from gui.widgets import scrollingWidgets
from gui.widgets import themedPathEntry
from asyncthreader import threader

LABELWIDTH = 125
ABOUT = "~Edizip~\nOriginal Script by Lyfe\n\nA tool for interacting with WerWolv's .edz style archives."
OPTIONS = ["Archive", "Extract", "Verify File Magic", "Read File Header"]
OPTIONMAP = {
    "Archive" : None,
    "Extract": "-d",
    "Verify File Magic": "-v",
    "Read File Header": "-x"
}

class Page(basePage.BasePage):
    def __init__(self, app, container, plugin):
        basePage.BasePage.__init__(self, app, container, "Switch ~ Edizip")
        self.plugin = plugin
        
        self.about_label = tk.Label(self, text = ABOUT, background = style.secondary_color, font = style.smalltext, foreground = style.primary_text_color)
        self.about_label.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 90, y = - 180)

        self.target_entry_label = tk.Label(self, text = "Target -", foreground = "white", background = style.secondary_color)
        self.target_entry_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 100)
        self.target_entry_box = themedPathEntry.ThemedPathEntry(self, foreground = "white", background = style.primary_color, justify = "center", font = style.mediumtext)
        self.target_entry_box.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 100)

        self.target_output_entry_label = tk.Label(self, text = "Output (Optional) -", foreground = "white", background = style.secondary_color)
        self.target_output_entry_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 70)
        self.target_output_entry_box = themedPathEntry.ThemedPathEntry(self, foreground = "white", background = style.primary_color, justify = "center", font = style.mediumtext)
        self.target_output_entry_box.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 70)

        self.tid_entry_label = tk.Label(self, text = "TitleID (Optional) -", foreground = "white", background = style.secondary_color)
        self.tid_entry_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 40)
        self.tid_entry_box = tk.Entry(self, foreground = "white", background = style.primary_color, justify = "center", font = style.mediumtext)
        self.tid_entry_box.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 40)

        self.selected_option_label = tk.Label(self, text = "Mode -", foreground = "white", background = style.secondary_color)
        self.selected_option_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 10 )
        self.selected_option = tk.StringVar()
        self.selected_option.set(OPTIONS[0])
        self.selected_option_dropdown = tk.OptionMenu(self,self.selected_option,*OPTIONS)
        self.selected_option_dropdown.configure(foreground = "white")
        self.selected_option_dropdown.configure(background = style.primary_color)
        self.selected_option_dropdown.configure(highlightthickness = 0)
        self.selected_option_dropdown.configure(borderwidth = 0)
        self.selected_option_dropdown.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 10)

        self.run_button = button.Button(self, text_string = "run script", background = style.primary_color, callback = self.run)
        self.run_button.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 20, y = 20)

        self.console_label = tk.Label(self, text = "CONSOLE:", foreground = "white", background = style.secondary_color)
        self.console_label.place(relwidth = 1, x = - 0.5 * LABELWIDTH, width = LABELWIDTH, rely = 0.5, height = 20, y = 40 + style.offset)

        self.console = scrollingWidgets.ScrolledText(self, background = "black", foreground = "white")
        self.console.place(relwidth = 1, width = - (2 * style.offset), relheight = 0.5, height = - (2 * style.offset + 60), rely = 0.5, y = 60 + style.offset, x = + style.offset)

    def Print(self, string):
        self.console.insert("end", string + "\n")
        self.console.yview_pickplace("end")
        self.plugin.out(string)

    def run(self):
        argstring = ""

        target = self.target_entry_box.get()
        if not target:
            self.Print("No target.\n\n")
            return        
        argstring += target

        mode = OPTIONMAP[self.selected_option.get()]
        if mode:
            argstring += (" " + mode)
        
        tid = self.tid_entry_box.get()
        if tid:
            argstring += f" -t {tid}"

        output = self.target_output_entry_box.get()
        if output:
            argstring += f" -o {output}"

        threader.do_async(main(argstring,self.Print))
        
class Plugin(basePlugin.BasePlugin):
    def __init__(self, app, container):
        self.app = app
        self.container = container
        basePlugin.BasePlugin.__init__(self, app, "Edizip", container)

    def get_pages(self):
        return[Page(self.app, self.container, self)]

    def exit(self):
        pass

def main(argstring, sout):
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "edizip.py"))
    args = [sys.executable, script_path]
    args.extend(argstring.split(" "))
    p = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    with p.stdout:
        for line in iter(p.stdout.readline, b""):
            sout(line.decode("ascii"))
    
def setup(app, container):
    return Plugin(app, container)