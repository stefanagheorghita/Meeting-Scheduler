import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from tkcalendar import DateEntry

background_image = None


def disable_edit(event):
    return "break"


def search(start_date_entry, end_date_entry, start_hour_combo,
           start_minute_combo, end_hour_combo,
           end_minute_combo):
    pass


def background(root):
    """
    Sets the background image of the given root window.
    :param root:
    :return:
    """
    global background_image
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    photo = Image.open("../images/search_meet.gif")
    mod_img = photo.resize((width, height))
    background_image = ImageTk.PhotoImage(mod_img)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor="center")


def search_meeting_screen(root):
    """
    Shows the search meeting screen.
    :param root:
    :return:
    """
    for widget in root.winfo_children():
        widget.pack_forget()

    def back_btn_func():
        from gui.main_menu import redraw
        redraw(root)

    background(root)

    back_frame = tk.Frame(root)
    back_frame.place(relx=0, rely=0, anchor="nw", width=60, height=30)
    back_button = tk.Button(back_frame, text="\u2190 Back", command=back_btn_func, bg="#FF3333",
                            activebackground="#CC0000", fg="white",
                            font=("Arial", 10))
    back_button.pack(fill="both", expand=True, padx=1, pady=1)

    meeting_frame = tk.Frame(root, bg="white", borderwidth=1, relief="solid")
    meeting_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.5)

    start_date_label = ttk.Label(meeting_frame, text=" Start Date:", background="white", font=("Arial", 12),
                                 borderwidth=1, relief="solid")
    start_date_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    start_date_entry = DateEntry(meeting_frame, font=("Arial", 12), background='darkblue', foreground='white',
                                 borderwidth=2, date_pattern='dd/mm/yyyy')
    start_date_entry.grid(row=0, column=1, padx=10, pady=5)
    start_date_entry.bind("<Key>", disable_edit)

    date_label = ttk.Label(meeting_frame, text="End Date:", background="white", font=("Arial", 12), borderwidth=1,
                           relief="solid")
    date_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    date_entry = DateEntry(meeting_frame, font=("Arial", 12), background='darkblue', foreground='white', borderwidth=2,
                           date_pattern='dd/mm/yyyy')
    date_entry.grid(row=1, column=1, padx=10, pady=5)
    date_entry.bind("<Key>", disable_edit)

    hours = [str(i).zfill(2) for i in range(24)]
    minutes = [str(i).zfill(2) for i in range(60)]

    start_time_label = ttk.Label(meeting_frame, text="Start Time:", background="white", font=("Arial", 12),
                                 borderwidth=1, relief="solid")
    start_time_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    start_hour_combo = ttk.Combobox(meeting_frame, values=hours, font=("Arial", 12), width=5, state='readonly')
    start_hour_combo.grid(row=2, column=1, padx=5, pady=5)
    start_hour_combo.set("00")

    start_minute_label = ttk.Label(meeting_frame, text=":", background="white", font=("Arial", 12))
    start_minute_label.grid(row=2, column=2, padx=5, pady=5)

    start_minute_combo = ttk.Combobox(meeting_frame, values=minutes, font=("Arial", 12), width=5, state='readonly')
    start_minute_combo.grid(row=2, column=3, padx=5, pady=5)
    start_minute_combo.set("00")

    end_time_label = ttk.Label(meeting_frame, text="End Time:", background="white", font=("Arial", 12), borderwidth=1,
                               relief="solid")
    end_time_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    end_hour_combo = ttk.Combobox(meeting_frame, values=hours, font=("Arial", 12), width=5, state='readonly')
    end_hour_combo.grid(row=3, column=1, padx=5, pady=5)
    end_hour_combo.set("00")

    end_minute_label = ttk.Label(meeting_frame, text=":", background="white", font=("Arial", 12))
    end_minute_label.grid(row=3, column=2, padx=5, pady=5)

    end_minute_combo = ttk.Combobox(meeting_frame, values=minutes, font=("Arial", 12), width=5, state='readonly')
    end_minute_combo.grid(row=3, column=3, padx=5, pady=5)
    end_minute_combo.set("00")

    search_button = ttk.Button(meeting_frame, text="Add participants",
                               command=lambda: search(start_date_entry, date_entry, start_hour_combo,
                                                      start_minute_combo, end_hour_combo,
                                                      end_minute_combo),
                               style='Button.TButton')
    search_button.grid(row=5, columnspan=3, pady=20)

    style = ttk.Style()
    style.theme_use("alt")
    style.configure("Button.TButton", foreground="white", background="#66CC66", font=("Arial", 12))
    style.map("TButton", background=[("active", "purple")])
