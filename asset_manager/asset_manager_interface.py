import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

class AssetManagerInterface:

  def __init__(self):
    # attributes
    self.directory_path = ""
    self.ui_select_directory = None
    self.ui_list_dir_files = None

    # init window
    self.window = Tk()
    self.window.title("Asset Manager")
    self.window.iconbitmap("data/images/PP-logo.ico")
    self.window.maxsize(800, 100000)
    
    # set window size and position
    w = 500
    h = 700
    sw = self.window.winfo_screenwidth()
    sh = self.window.winfo_screenheight()
    x = (sw / 2) - (w / 2)
    y = (sh / 2) - (h / 2)
    self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    # logo image
    img_logo = Image.open("data/images/PP-logo.png")
    img_logo = img_logo.resize((100, 100))
    img_logo = ImageTk.PhotoImage(img_logo)

    lbl_logo = ttk.Label(self.window, image=img_logo, padding=10)
    lbl_logo.pack(side='top', fill='y')

    self.__startupUI()

    # open UI
    self.window.mainloop()

  def __startupUI(self):
    # main frame
    frame_main = ttk.Frame(self.window, padding=10)
    frame_main.grid_columnconfigure(0, weight=0)
    frame_main.grid_columnconfigure(1, weight=1)
    frame_main.grid_columnconfigure(2, weight=0)

    lbl_seldir = ttk.Label(frame_main, text="Select folder:")
    lbl_seldir.grid(column=0, row=0, padx=10, pady=10, sticky="w")

    ent_seldir = ttk.Entry(frame_main, textvariable=self.directory_path, width=100)
    ent_seldir.grid(column=1, row=0, padx=10, pady=10)

    btn_seldir = ttk.Button(frame_main, text="Browse...", command=self.chooseDirectory)
    btn_seldir.grid(column=2, row=0, padx=10, pady=10, sticky="e")

    # list files frame
    frame_files = ttk.Frame(self.window, padding=10)

    lbl_files = ttk.Label(frame_files, text="Files found:")
    lbl_files.pack(anchor="w", padx=10, pady=10)

    lst_files = Listbox(frame_files, bg="white", fg="black", font="Arial 9", bd=0, selectbackground="#00bb00", cursor="hand2", activestyle='none')
    lst_files.pack(fill='x', padx=10, pady=10)

    # actions frame
    frame_actions = ttk.Frame(self.window, padding=10)

    btn_unzip = ttk.Button(frame_actions, text="Unzip all files", command=self.chooseDirectory)
    btn_unzip.grid(column=0, row=0, padx=10, pady=10)

    btn_csv = ttk.Button(frame_actions, text="Export CSV", command=self.chooseDirectory)
    btn_csv.grid(column=1, row=0, padx=10, pady=10)

    btn_del = ttk.Button(frame_actions, text="Delete ZIP files", command=self.chooseDirectory)
    btn_del.grid(column=2, row=0, padx=10, pady=10)

    # footer frame
    frame_foot = ttk.Frame(self.window, padding=25)

    btn_quit = ttk.Button(frame_foot, text="Quit", command=self.window.destroy)
    btn_quit.pack()

    # packing UI
    frame_main.pack(fill='x')
    frame_files.pack(fill='x')
    frame_foot.pack(side='bottom', fill='y')
    frame_actions.pack(side='bottom')

    # set UI attributes
    self.ui_select_directory = ent_seldir
    self.ui_list_dir_files = lst_files

  def chooseDirectory(self):
    path = filedialog.askdirectory()
    
    self.directory_path = path
    self.ui_select_directory.delete(0, END)
    self.ui_select_directory.insert(0, path)

    files = [f for f in os.listdir(path) if f.endswith('.zip')]
    for i, f in enumerate(files):
      self.ui_list_dir_files.insert(i, f)


if __name__ == "__main__":
  ami = AssetManagerInterface()