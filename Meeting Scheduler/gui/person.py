import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from validation.person_validation import add_person_validation

background_image = None


def background(root):
    """
    Sets the background image of the given root window (the add person window).
    :param root:
    :return:
    """
    global background_image
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    photo = Image.open("../images/person.gif")
    mod_img = photo.resize((width, height))
    background_image = ImageTk.PhotoImage(mod_img)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor="center")


def show_input_labels(input_frame):
    """
    Shows the labels and entry fields for the user to input the person's data.
    :param input_frame:
    :return:
    """
    label_id = tk.Label(input_frame, text="Id:", font=("Arial", 12))
    label_id.pack()
    entry_id = tk.Entry(input_frame, font=("Arial", 12))
    entry_id.pack()

    label_first_name = tk.Label(input_frame, text="First Name:", font=("Arial", 12))
    label_first_name.pack()
    entry_first_name = tk.Entry(input_frame, font=("Arial", 12))
    entry_first_name.pack()

    label_last_name = tk.Label(input_frame, text="Last Name:", font=("Arial", 12))
    label_last_name.pack()
    entry_last_name = tk.Entry(input_frame, font=("Arial", 12))
    entry_last_name.pack()
    return entry_id, entry_first_name, entry_last_name


def save_person(entry_id, entry_first_name, entry_last_name):
    """
    Sends the data to the validation function and to be added to the database and shows the if the operation was successful or not.
    :return:
    """
    id = entry_id.get()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    valid, message = add_person_validation(id, first_name, last_name)
    if valid:
        if message is  None:
            messagebox.showinfo("Success", "Person successfully added to the database!")
        else:
            messagebox.showinfo("Success", message)
        entry_id.delete(0, tk.END)
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
    else:
        messagebox.showerror("Error", message)


def add_person(root):
    """
    Constructs the add person window.
    :param root:
    :return:
    """
    for widget in root.winfo_children():
        widget.pack_forget()

    def back_btn_func():
        from gui.main_menu import redraw
        input_frame.destroy()
        redraw(root)

    background(root)
    input_frame = tk.Frame(root, bg="#F4D9E9", bd=5)
    input_frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.6, anchor="center")
    entry_id, entry_first_name, entry_last_name = show_input_labels(input_frame)

    save_button = tk.Button(input_frame, text="Save",
                            command=lambda: save_person(entry_id, entry_first_name, entry_last_name), bg="#FF9999",
                            fg="white",
                            font=("Arial", 12, "bold"))
    save_button.pack(side=tk.BOTTOM, pady=10)

    back_frame = tk.Frame(root)
    back_frame.place(relx=0, rely=0, anchor="nw", width=60, height=30)
    back_button = tk.Button(back_frame, text="\u2190 Back", command=back_btn_func, bg="#FF3333",
                            activebackground="#CC0000", fg="white",
                            font=("Arial", 10))
    back_button.pack(fill="both", expand=True, padx=1, pady=1)
