import tkinter as tk
from PIL import Image, ImageTk

from gui.menu.button_handling import add_person, add_meeting, import_data, export_data

background_image = None
mod_img = None


def background(root):
    global background_image
    global mod_img
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    photo = Image.open("../images/menu.gif")
    mod_img = photo.resize((width, height))
    background_image = ImageTk.PhotoImage(mod_img)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor="center")


def buttons(root):
    frame = tk.Frame(root, bg="white", bd=5)
    frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.6, anchor="center")

    add_person_btn = tk.Button(frame, text="Add Person", command=add_person, bg="lightgreen", fg="black",
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


def menu_window():
    root = tk.Tk()
    root.title("Meeting Scheduler")
    root.geometry("500x400")
    background(root)
    buttons(root)
    root.mainloop()
