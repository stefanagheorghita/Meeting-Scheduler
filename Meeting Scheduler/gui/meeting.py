import tkinter as tk
from datetime import datetime, time
from tkinter import ttk, messagebox

from PIL import Image, ImageTk
from tkcalendar import DateEntry

from database.manager import DatabaseManager
from validation.meeting_validation import validate_meeting_data

background_image = None
participant_window_open = False


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


def get_data(start_date_entry, end_date_entry, start_hour_combo, start_minute_combo, end_hour_combo, end_minute_combo):
    """
    Gets the data from the fields of the add meeting screen
    :param start_date_entry: Entry field for the start date
    :param end_date_entry: Entry field for the end date
    :param start_hour_combo: Combobox for the start hour
    :param start_minute_combo: Combobox for the start minute
    :param end_hour_combo: Combobox for the end hour
    :param end_minute_combo: Combobox for the end minute
    :return:
    """
    global participant_window_open
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    start_hour = start_hour_combo.get()
    start_minute = start_minute_combo.get()
    end_hour = end_hour_combo.get()
    end_minute = end_minute_combo.get()
    result, msg = validate_meeting_data(start_date, end_date, start_hour, start_minute, end_hour, end_minute)
    print(result, msg)
    if result and not participant_window_open:
        start_hour_combo.set("00")
        start_minute_combo.set("00")
        end_hour_combo.set("00")
        end_minute_combo.set("00")
        participant_window_open = True
        open_choose_participants(start_date, end_date, start_hour, start_minute, end_hour, end_minute)
    elif result and participant_window_open:
        pass
    else:
        messagebox.showerror("Error", msg)


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

    save_button = ttk.Button(meeting_frame, text="Add participants",
                             command=lambda: get_data(start_date_entry, date_entry, start_hour_combo,
                                                      start_minute_combo, end_hour_combo,
                                                      end_minute_combo),
                             style='Button.TButton')
    save_button.grid(row=5, columnspan=3, pady=20)

    style = ttk.Style()
    style.theme_use("alt")
    style.configure("Button.TButton", foreground="white", background="#66CC66", font=("Arial", 12))
    style.map("TButton", background=[("active", "purple")])


def disable_edit(event):
    return "break"


def open_choose_participants(start_date, end_date, start_hour, start_minute, end_hour, end_minute):
    """
    Opens the window where the user can select the participants of the meeting.
    :return:
    """

    db_manager = DatabaseManager()
    participants = db_manager.find_all_persons()
    if participants is None:
        messagebox.showerror("Error", "There was an error while retrieving the participants from the database!")

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
        global participant_window_open
        if len(selected_participants) == 0:
            messagebox.showerror("Error", "You must select at least one participant!")
            return
        participants_window.destroy()
        participant_window_open = False
        send_data(start_date, end_date, start_hour, start_minute, end_hour, end_minute, selected_participants)

    save_button = tk.Button(participants_window, text="Save", command=save_selected)
    save_button.pack(side=tk.BOTTOM, anchor="nw", fill=tk.X)

    participants_canvas = tk.Canvas(participants_window)
    participants_frame = tk.Frame(participants_canvas)

    scrollbar = tk.Scrollbar(participants_window, orient="vertical", command=participants_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    participants_canvas.pack(side="left", fill="y", expand=True)
    participants_canvas.create_window((0, 0), window=participants_frame, anchor="nw")

    participants_frame.bind("<Configure>",
                            lambda e: participants_canvas.configure(scrollregion=participants_canvas.bbox("all")))

    participants_canvas.configure(yscrollcommand=scrollbar.set)

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

        text = f"{participant[0]} - {participant[1]} {participant[2]}"
        checkbox = tk.Checkbutton(participants_frame, text=text, variable=var,
                                  command=on_checkbox_click, font=("Arial", 12))
        checkbox.pack(anchor=tk.W)


def send_data(start_date, end_date, start_hour, start_minute, end_hour, end_minute, selected_participants):
    """
    Sends the data to the database
    :param start_date:
    :param end_date:
    :param start_hour:
    :param start_minute:
    :param end_hour:
    :param end_minute:
    :param selected_participants:
    :return:
    """
    db_manager = DatabaseManager()
    start_hour = int(start_hour)
    start_minute = int(start_minute)
    end_hour = int(end_hour)
    end_minute = int(end_minute)
    start_time = datetime.combine(start_date, time(start_hour, start_minute))
    end_time = datetime.combine(end_date, time(end_hour, end_minute))

    result = db_manager.add_meeting(start_time, end_time, selected_participants)
    if result:
        messagebox.showinfo("Success", "Meeting successfully added to the database!")
    else:
        messagebox.showerror("Error", "There was an error while adding the meeting to the database!")
