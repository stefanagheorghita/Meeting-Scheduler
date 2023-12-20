import tkinter as tk
from datetime import datetime, time
from tkinter import ttk, messagebox

from PIL import Image, ImageTk
from tkcalendar import DateEntry

from database.manager import DatabaseManager
from importing_exporting.export import export
from validation.meeting_validation import validate_meeting_search

background_image = None


def disable_edit(event):
    return "break"


def show_search_results(rows, participants):
    """
    Shows the search results in a new window
    Parameters
    ----------
    rows: list
        A list of tuples containing the meeting information
    participants: list
        A list of lists containing the participants of each meeting
    Returns
    -------
    None
    """
    result_window = tk.Toplevel()
    result_window.title("Meeting Search Results")

    result_text = tk.Text(result_window, height=20, width=50)
    result_text.tag_configure("bold", font=("Arial", 10, "bold"))
    result_text.tag_configure("red", foreground="red")
    result_text.tag_configure("green", foreground="green")
    result_text.tag_configure("blue", foreground="blue")
    result_text.tag_configure("orange", foreground="orange")
    result_text.pack()

    meetings = []
    for i in range(len(rows)):
        result_text.insert(tk.END, "Meeting ID: ", "red")
        result_text.insert(tk.END, f"{rows[i][0]}\n")
        result_text.insert(tk.END, "Meeting name: ", "orange")
        result_text.insert(tk.END, f"{rows[i][3]}\n")
        result_text.insert(tk.END, "Start time: ", "blue")
        result_text.insert(tk.END, f"{rows[i][1]}\n")
        result_text.insert(tk.END, "End time: ", "blue")
        result_text.insert(tk.END, f"{rows[i][2]}\n")
        result_text.insert(tk.END, "Participants:\n", "green")
        for participant in participants[i]:
            result_text.insert(tk.END, f"{participant[1]} {participant[2]}\n")
        meetings.append((rows[i][0], rows[i][1], rows[i][2], rows[i][3], participants[i]))
    result_text.config(state=tk.DISABLED)
    result_text.pack(fill="both", expand=True)

    export_button = tk.Button(result_window, text="Export", command=lambda: export(False, meetings), bg="#FF9999",
                              fg="white",
                              font=("Arial", 12, "bold"))
    export_button.pack()


def search(start_date_entry, end_date_entry, start_hour_combo,
           start_minute_combo, end_hour_combo,
           end_minute_combo):
    """
    Searches for meetings in the given interval
    Parameters
    ----------
    start_date_entry: DateEntry
        The start date of the interval
    end_date_entry: DateEntry
        The end date of the interval
    start_hour_combo: tk.Combobox
        The start hour of the interval
    start_minute_combo: tk.Combobox
        The start minute of the interval
    end_hour_combo: tk.Combobox
        The end hour of the interval
    end_minute_combo: tk.Combobox
        The end minute of the interval
    Returns
    -------
    None
    """
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    start_hour = start_hour_combo.get()
    start_minute = start_minute_combo.get()
    end_hour = end_hour_combo.get()
    end_minute = end_minute_combo.get()
    res, msg = validate_meeting_search(start_date, end_date, start_hour, start_minute, end_hour, end_minute)
    db_manager = DatabaseManager()
    start_time = datetime.combine(start_date, time(int(start_hour), int(start_minute)))
    end_time = datetime.combine(end_date, time(int(end_hour), int(end_minute)))
    all_participants = []
    if res:
        meetings = db_manager.search_meetings(start_time, end_time)
        if meetings is None:
            messagebox.showerror("Error", "An error occurred while searching for meetings!")
        else:
            if len(meetings) == 0:
                messagebox.showinfo("Info", "No meetings were found!")
                return
            for meeting in meetings:
                participants = db_manager.get_participants(meeting[0])
                if participants is None:
                    messagebox.showerror("Error", "An error occurred while searching for participants!")
                    return
                all_participants.append(participants)
            show_search_results(meetings, all_participants)
    else:
        messagebox.showinfo("Info", "No meetings were found! The interval is invalid!")


def background(root):
    """
    Sets the background image of the given root window \n
   Parameters
    ----------
    root: Tk
        The root window
    Returns
    -------
    None
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
    Shows the search meeting screen \n
    Parameters
    ----------
    root: Tk
        The root window
    Returns
    -------
    None
    """
    for widget in root.winfo_children():
        widget.pack_forget()

    def back_btn_func():
        """
        Returns to the main menu \n
        Returns
        -------

        """
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

    search_button = ttk.Button(meeting_frame, text="Search",
                               command=lambda: search(start_date_entry, date_entry, start_hour_combo,
                                                      start_minute_combo, end_hour_combo,
                                                      end_minute_combo),
                               style='Button.TButton')
    search_button.grid(row=5, columnspan=3, pady=20)

    style = ttk.Style()
    style.theme_use("alt")
    style.configure("Button.TButton", foreground="white", background="#66CC66", font=("Arial", 12))
    style.map("TButton", background=[("active", "purple")])
