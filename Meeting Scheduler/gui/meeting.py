import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

background_image = None


def background(root):
    """
    Sets the background image of the given root window.
    :param root:
    :return:
    """
    global background_image
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    photo = Image.open("../images/meeting.gif")
    mod_img = photo.resize((width, height))
    background_image = ImageTk.PhotoImage(mod_img)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor="center")


def disable_edit(event):
    return "break"


def add_meeting_screen(root):
    """
    Shows the add meeting screen.
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

    date_label = ttk.Label(meeting_frame, text="Date:", background="white", font=("Arial", 12), borderwidth=1,
                           relief="solid")
    date_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    date_entry = DateEntry(meeting_frame, font=("Arial", 12), background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=0, column=1, padx=10, pady=5)
    date_entry.bind("<Key>", disable_edit)

    hours = [str(i).zfill(2) for i in range(24)]
    minutes = [str(i).zfill(2) for i in range(60)]

    start_time_label = ttk.Label(meeting_frame, text="Start Time:", background="white", font=("Arial", 12),
                                 borderwidth=1, relief="solid")
    start_time_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    start_hour_combo = ttk.Combobox(meeting_frame, values=hours, font=("Arial", 12), width=5, state='readonly')
    start_hour_combo.grid(row=1, column=1, padx=5, pady=5)
    start_hour_combo.set("00")

    start_minute_label = ttk.Label(meeting_frame, text=":", background="white", font=("Arial", 12))
    start_minute_label.grid(row=1, column=2, padx=5, pady=5)

    start_minute_combo = ttk.Combobox(meeting_frame, values=minutes, font=("Arial", 12), width=5, state='readonly')
    start_minute_combo.grid(row=1, column=3, padx=5, pady=5)
    start_minute_combo.set("00")

    end_time_label = ttk.Label(meeting_frame, text="End Time:", background="white", font=("Arial", 12), borderwidth=1,
                               relief="solid")
    end_time_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    end_hour_combo = ttk.Combobox(meeting_frame, values=hours, font=("Arial", 12), width=5, state='readonly')
    end_hour_combo.grid(row=2, column=1, padx=5, pady=5)
    end_hour_combo.set("00")

    end_minute_label = ttk.Label(meeting_frame, text=":", background="white", font=("Arial", 12))
    end_minute_label.grid(row=2, column=2, padx=5, pady=5)

    end_minute_combo = ttk.Combobox(meeting_frame, values=minutes, font=("Arial", 12), width=5, state='readonly')
    end_minute_combo.grid(row=2, column=3, padx=5, pady=5)
    end_minute_combo.set("00")

    save_button = ttk.Button(meeting_frame, text="Save Meeting", command=open_choose_participants,
                             style='EntireGreen.TButton')
    save_button.grid(row=4, columnspan=3, pady=20)

    style = ttk.Style()
    style.theme_use("alt")
    style.configure("EntireGreen.TButton", foreground="white", background="#66CC66", font=("Arial", 12))
    style.map("TButton", background=[("active", "purple")])


participants = [
    "Participant 1",
    "Participant 2",
    "Participant 3",
]


def open_choose_participants():
    """
    Opens the window where the user can select the participants of the meeting.
    :return:
    """
    participants_window = tk.Toplevel()
    participants_window.title("Select Participants")

    window_width = 400
    window_height = 400
    screen_width = participants_window.winfo_screenwidth()
    screen_height = participants_window.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    participants_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    selected_participants = []

    def save_selected():
        print(selected_participants)
        participants_window.destroy()

    participants_frame = tk.Frame(participants_window)
    participants_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    checkbox_vars = []

    for participant in participants:
        var = tk.BooleanVar()
        var.set(False)
        checkbox_vars.append(var)

        def on_checkbox_click(participant=participant, var=var):
            if var.get() and participant not in selected_participants:
                selected_participants.append(participant)
            elif not var.get() and participant in selected_participants:
                selected_participants.remove(participant)

        checkbox = tk.Checkbutton(participants_frame, text=participant, variable=var,
                                  command=on_checkbox_click, font=("Arial", 12))
        checkbox.pack(anchor=tk.W)

    save_button = tk.Button(participants_window, text="Save", command=save_selected)
    save_button.pack()
