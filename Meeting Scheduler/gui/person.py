import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from validation.person_validation import add_person_validation, add_person_confirmation

background_image = None


def background(root):
    """
    Sets the background image of the given root window (the add person window) \n
    Parameters
    ----------
    root: tk.Tk
        The root window of the application.
    Returns
    -------
    None
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
    Shows the labels and entry fields for the user to input the person's data \n
    Parameters
    ----------
    input_frame: tk.Frame
        The frame where the labels and entry fields will be placed.
    Returns
    -------
    entry_id: tk.Entry
        The entry field for the id.
    entry_first_name: tk.Entry
        The entry field for the first name.
    entry_last_name: tk.Entry
        The entry field for the last name.
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


def different_formatting_case(id, first_name, last_name, formatted_first_name, formatted_last_name):
    """
    Shows the user the different formatting options for the name and asks him to choose the correct one \n
    Parameters
    ----------
    id: str
        The id of the person.
    first_name: str
        The first name of the person.
    last_name: str
        The last name of the person.
    formatted_first_name: str
        The first name of the person in the correct format.
    formatted_last_name: str
        The last name of the person in the correct format.
    Returns
    -------
    None
    """

    def add_now(id, first_name, last_name):
        """
        Sends the data to be added to the database and shows the if the operation was successful or not \n
        Parameters
        ----------
        id: str
            The id of the person.
        first_name: str
            The first name of the person.
        last_name: str
            The last name of the person.
        Returns
        -------
        None
        """
        result, msg = add_person_confirmation(id, first_name, last_name)
        if result:
            messagebox.showinfo("Success", "Person successfully added to the database!")
        else:
            messagebox.showerror("Error", msg)
        window.destroy()

    window = tk.Toplevel()
    window.title("Name Confirmation")
    window.geometry("350x200")
    window.configure(bg="#e1f5fe")

    label = tk.Label(window, text="The name didn't have the expected format.", font=("Arial", 12), bg="#e1f5fe",
                     fg="#333")
    label.pack(pady=10)

    explanation = tk.Label(window, text="Please choose the correct variant:",
                           font=("Arial", 10), bg="#e1f5fe", fg="#333")
    explanation.pack(padx=5, pady=5, ipadx=5, ipady=5)
    parts = first_name.split()
    name = ""
    for i in range(len(parts)):
        if parts[i].isalpha() and (i + 1 < len(parts) and parts[i + 1].isalpha()):
            name += parts[i] + " "
        else:
            name += parts[i]
    first_name = name

    parts = last_name.split()
    name = ""
    for i in range(len(parts)):
        if parts[i].isalpha() and (i + 1 < len(parts) and parts[i + 1].isalpha()):
            name += parts[i] + " "
        else:
            name += parts[i]
    last_name = name
    if formatted_first_name[1:] == first_name[1:]:
        first_name = formatted_first_name
    if formatted_last_name[1:] == last_name[1:]:
        last_name = formatted_last_name
    choices = [(formatted_first_name, last_name[0].upper() + last_name[1:]),
               (first_name[0].upper() + first_name[1:], formatted_last_name),
               (formatted_first_name, formatted_last_name),
               (first_name[0].upper() + first_name[1:], last_name[0].upper() + last_name[1:])]
    choices = list(set(choices))

    for choice in choices:
        btn = tk.Button(window, text=choice[0] + " " + choice[1], font=("Arial", 10), bg="#b3e5fc", fg="#333",
                        activebackground="#81d4fa",
                        activeforeground="#222",
                        command=lambda c=choice: add_now(id, c[0], c[1]))
        btn.pack(pady=5, padx=20, ipadx=10)


def save_person(entry_id, entry_first_name, entry_last_name):
    """
    Sends the data to the validation function and to be added to the database and shows the if the operation
    was successful or not \n
    Parameters
    ----------
    entry_id: tk.Entry
        The entry field for the id.
    entry_first_name: tk.Entry
        The entry field for the first name.
    entry_last_name: tk.Entry
        The entry field for the last name.
    Returns
    -------
    None
    """
    id = entry_id.get()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    valid, message = add_person_validation(id, first_name, last_name)
    if valid:
        if message is None:
            messagebox.showinfo("Success", "Person successfully added to the database!")
        else:
            if "!!" not in message:
                messagebox.showinfo("Success", message)
            else:
                split_name = message.split("!!")
                different_formatting_case(id, first_name, last_name, split_name[0], split_name[1])
        entry_id.delete(0, tk.END)
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
    else:
        messagebox.showerror("Error", message)


def add_person(root):
    """
    Constructs the add person window \n
    Parameters
    ----------
    root: tk.Tk
        The root window of the application.
    Returns
    -------
    None
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
