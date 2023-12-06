import os

import tkinter as tk
from PIL import Image, ImageTk

from gui.menu.button_handling import add_meeting, import_data, export_data
from gui.person import add_person

background_image = None


def get_image_path(image_name):
    """Returns the absolute path of the background image with the given name
    :param image_name: The name of the image.
    :return: The absolute path of the image.
    """
    current_file_path = os.path.abspath(__file__)
    path_parts = current_file_path.split(os.sep)
    base_dir_index = path_parts.index("Meeting-Scheduler")
    base_dir = os.sep.join(path_parts[:base_dir_index + 1])
    path = os.path.join(base_dir, "images", image_name)
    return path


def background(root):
    """
    Sets the background image of the given root window.
    :param root:
    :return:
    """
    global background_image
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    photo = Image.open(get_image_path("menu.gif"))
    mod_img = photo.resize((width, height))
    background_image = ImageTk.PhotoImage(mod_img)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor="center")


def buttons(root):
    """
    Places the buttons on the given root window (the main menu window).
    :param root:
    :return:
    """
    frame = tk.Frame(root, bg="white", bd=5)
    frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.6, anchor="center")

    add_person_btn = tk.Button(frame, text="Add Person", command=lambda: add_person(root), bg="lightgreen", fg="black",
                               relief=tk.RAISED, font=("Arial", 12, "bold"))
    add_person_btn.pack(side=tk.TOP, padx=20, pady=10, fill=tk.X)

    add_meeting_btn = tk.Button(frame, text="Add Meeting", command=add_meeting, bg="#CFA9F3", fg="black",
                                relief=tk.RAISED, font=("Arial", 12, "bold"))
    add_meeting_btn.pack(side=tk.TOP, padx=20, pady=10, fill=tk.X)

    import_btn = tk.Button(frame, text="Import", command=import_data, bg="lightblue", fg="black",
                           relief=tk.RAISED, font=("Arial", 12, "bold"))
    import_btn.pack(side=tk.TOP, padx=20, pady=10, fill=tk.X)

    export_btn = tk.Button(frame, text="Export", command=export_data, bg="lightcoral", fg="black",
                           relief=tk.RAISED, font=("Arial", 12, "bold"))
    export_btn.pack(side=tk.TOP, padx=20, pady=10, fill=tk.X)


def redraw(root):
    """
    Redraws the main menu window (it is needed when the user presses the back button).
    :param root:
    :return:
    """
    background(root)
    buttons(root)


def menu_window():
    """
    Constructs the main menu window.
    :param:
    :return:
    """
    root = tk.Tk()
    root.title("Meeting Scheduler")
    root.geometry("500x400")
    background(root)
    buttons(root)
    root.mainloop()
