from genericpath import isfile
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
import os
from PIL import Image

def load_spell_list(path):
    file = open(path, encoding="utf-8")
    word_list = []
    for line in file.readlines():
        line = line.replace('\n', '')
        word_list.append(line)
    file.close()
    return word_list

class Gui_helper_main:
    def __init__(self):
        self.root = Tk()
        self.frame = None
        self.frame_index = 0
        self.root.geometry('450x350')
        self.root.title('Tag Extractor')
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        # maker info
        self.maker_name = Label(self.root, text="Maker : JingShing")
        self.maker_name.grid(column=0, row=3, sticky=N+W)
        
        self.frames = [page_module(self)]
        self.switch_frame(0)
        
    def switch_frame(self, index):
        if self.frame is not None:
            self.frame.grid_forget()
        self.frame_index = index
        self.frame = self.frames[self.frame_index]
        self.frame.grid(column=0, row=0, sticky=N+W)

    def run(self):
        self.root.mainloop()

    def quit(self):
        if messagebox.askyesno('Confirm','Are you sure you want to quit?'):
            self.root.quit()

class page_module(Frame):
    def __init__(self, master):
        Frame.__init__(self, master = master.root)
        self.main = master
        self.master = master.root
        self.data_dict = {

        }
        self.all_text = Text(self, width=30, height=10)
        self.all_text.grid(column=2, row=0, sticky=N+W, columnspan=2, rowspan=5)
        self.all_label = Label(self, text="all info")
        self.all_label.grid(column=2, row=3)

        self.prompt_text = Text(self, width=30, height=5)
        self.prompt_text.grid(column=0, row=0, sticky=N+W, columnspan=2)
        self.prompt_label = Label(self, text="prompt")
        self.prompt_label.grid(column=0, row=1)
        self.negative_text = Text(self, width=30, height=5)
        self.negative_text.grid(column=0, row=2, sticky=N+W, columnspan=2)
        self.negative_label = Label(self, text="negative prompt")
        self.negative_label.grid(column=0, row=3)
        self.parameter_text = Text(self, width=30, height=5)
        self.parameter_text.grid(column=0, row=4, sticky=N+W, columnspan=2)
        self.parameter_label = Label(self, text="parameter")
        self.parameter_label.grid(column=0, row=5)
        self.import_button = Button(self, text='import', command=self.import_set)
        self.import_button.grid(column=0, row=6, sticky=N+W)
        self.save_button = Button(self, text='save', command=self.save_set)
        self.save_button.grid(column=1, row=6, sticky=N+W)
        
    def add_text(self, text):
        if type(text) == dict:
            self.dict_to_text(text)
        else:
            self.data_dict['spell'] = text
        self.get_info()
        self.all_text.delete(1.0, 'end')
        self.all_text.insert(END, self.data_dict['spell'])
        self.prompt_text.delete(1.0, 'end')
        self.prompt_text.insert(END, self.data_dict['prompt'])
        self.negative_text.delete(1.0, 'end')
        self.negative_text.insert(END, self.data_dict['negative'])
        self.parameter_text.delete(1.0, 'end')
        self.parameter_text.insert(END, self.data_dict['parameter'])

    def get_info(self):
        info = self.data_dict['spell'].replace("parameters\n","").replace("Negative prompt: ", "").split("\n")
        self.data_dict['prompt']=info[0]
        self.data_dict['negative']=info[1]
        self.data_dict['parameter']=info[2]

    def dict_to_text(self, dict1):
        self.data_dict['spell'] = ''
        for key in dict1:
            self.data_dict['spell']+=key + '\n'
            self.data_dict['spell']+=dict1[key] + '\n'

    def import_set(self):
        set_path = filedialog.askopenfilename(filetypes = (("png file","*.png"),("all files","*.*")))
        if set_path:
            im = Image.open(set_path)
            im.load()
            self.data_dict['file_name'] = set_path.split('/')[-1].split('.')[0]
            self.add_text(im.info)

    def save_set(self):
        f = open(self.data_dict['file_name'] + ".txt", "w")
        f.write(str(self.data_dict['spell']))
        f.close()

main = Gui_helper_main()
main.run()