import customtkinter
from tkinter import *
import sqlite3
from datetime import datetime
import CTkMessagebox
import time

def create_score_table():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score_seconds INTEGER,
                    datetime TEXT)''')
    conn.commit()
    conn.close()

def insert_score(score_seconds):
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO scores (score_seconds, datetime) VALUES (?, ?)''', (score_seconds, current_datetime))
    conn.commit()
    conn.close()

def output():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scores ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    if len(rows) == 0:
        CTkMessagebox.CTkMessagebox(title="Information", message="Data does not exist: Note - first solve some questions.")
        return
    avg = sum(row[1] for row in rows) / len(rows)
    CTkMessagebox.CTkMessagebox(title='Report', message= f'''Time taken is {rows[0][1]} seconds and Average time taken by last {len(rows)} questions is: {avg} seconds. ''', icon='check')
    conn.close()
def deletedb():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scores")
    conn.commit()
    conn.close()
    CTkMessagebox.CTkMessagebox(title="Information", message= "All Data Cleared...", icon='check')

class Stopwatch:
    def __init__(self, label):
        self.label = label
        self.start_time = 0
        self.paused_time = 0
        self.paused = False
        self.running = False
        self.elapsed_time = 0
        self.update_time()

    def start(self):
            if not self.running:
                self.start_time = time.time() - self.elapsed_time
                self.running = True
                self.update_time()
    def pause(self):
            if self.running:
                self.elapsed_time = time.time() - self.start_time
                self.running = False

    def reset(self):
            self.start_time = 0
            self.paused_time = 0
            self.paused = False
            self.running = False
            self.elapsed_time = 0
            self.label.configure(text="00:00:00")

    def update_time(self):
            if self.running:
                self.elapsed_time = time.time() - self.start_time
                minutes, seconds = divmod(self.elapsed_time, 60)
                hours, minutes = divmod(minutes, 60)
                time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                self.label.configure(text=time_str)
            self.label.after(1000, self.update_time)

    def get_elapsed_time(self):
        return int(self.elapsed_time)

# GUI Functions
def start_timer():
    stopwatch.start()

def pause_timer():
    stopwatch.pause()

def reset_timer():
    stopwatch.reset()

def save_time():
    elapsed_time = stopwatch.get_elapsed_time()
    insert_score(elapsed_time)
    output()
    stopwatch.reset()

def delete_data():
    deletedb()


def main():
    global stopwatch
    customtkinter.set_appearance_mode('dark') #SPECIFIES WEATHER USE THE DARK THEME OR THE LIGHT THEME OR SYSTEM THEME. 
    root = customtkinter.CTk()
    root.title("Question solve timer.")

    #Main clock label
    time_label = customtkinter.CTkLabel(root, text="00:00:00", fg_color="transparent",font=('CTkFont', 55))
    time_label.pack(fill = 'both')

    start_button = customtkinter.CTkButton(master=root,text="Start", command=start_timer)
    start_button.pack(side='left',expand=1)

    pause_button = customtkinter.CTkButton(master=root, text = 'Pause', command=pause_timer)
    pause_button.pack(side='left',expand=1)

    reset_button = customtkinter.CTkButton(master=root, text = 'Reset', command=reset_timer)
    reset_button.pack(side='left',expand=1)

    save_button = customtkinter.CTkButton(master=root, text = 'Save', command=save_time)
    save_button.pack(side='left',expand=1)

    delete_button = customtkinter.CTkButton(master=root, text = 'DeleteDB', command= delete_data)
    delete_button.pack(side='left',expand=1)
    stopwatch = Stopwatch(time_label)
    root.mainloop()

if __name__ == "__main__":
    create_score_table()
    main()