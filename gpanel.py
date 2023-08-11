import tkinter as tk
from tkinter import ttk

import tkinter as tk
import subprocess

users_frame = None  # Declare global variables for users_frame and groups_frame
groups_frame = None



def create_group():
    try:
        root.withdraw()  # Hide the GUI window
        gs_process = subprocess.Popen(['python', r"C:\Users\anish\OneDrive\Documents\sem 3\Algo2\cw2\gs.py"])
        num_users = int(num_user_entry.get())  # Get the number of users from the entry field

        for _ in range(num_users):
            groupchat_process = subprocess.Popen(['python', r"C:\Users\anish\OneDrive\Documents\sem 3\Algo2\cw2\groupchat.py"])
            groupchat_process.wait()  # Wait for each process to complete
            
        gs_process.wait()  # Wait for gs.py to complete

    except ValueError:
        print("Invalid input for number of users.")
    except FileNotFoundError as e:
        print(f"Program not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create the main tkinter window
root = tk.Tk()
root.title("Admin Panel")
root.geometry("500x300")  # Set the window size

# Create a style for ttk widgets
style = ttk.Style()
style.configure("TLabel", background="#1A2226",
                foreground="#0DB8DE", font=("Roboto", 12))
style.configure("TButton", background="#0DB8DE",
                foreground="#1A2226", font=("Roboto", 12))
# Set entry background and foreground color
style.configure("TEntry", fieldbackground="#1A2226", foreground="#1A2226")
# Set background color for create box
style.configure("TFrame", background="#222D32")

# Create the create box using ttk widgets
create_box = ttk.Frame(root, padding=20)
create_box.grid(row=0, column=0, sticky="nsew")

# Create the create key
create_key = ttk.Label(create_box, text="GROUP PANEL 🌍",
                      font=("Roboto", 30, "bold"))
create_key.grid(row=0, column=0, columnspan=2, pady=15)

# Create the groupname and num_user input fields
groupname_label = ttk.Label(create_box, text="GROUP NAME")
groupname_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

groupname_entry = ttk.Entry(create_box)
groupname_entry.grid(row=1, column=1, padx=5, pady=5)

num_user_label = ttk.Label(create_box, text="NO OF USER")
num_user_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)

num_user_entry = ttk.Entry(create_box)
num_user_entry.grid(row=2, column=1, padx=5, pady=5)

def save_group():
    group_name = groupname_entry.get()
    num_users = num_user_entry.get()

    if group_name and num_users:
         with open("groupsname.txt", "a") as file:
            file.write(f"{group_name} ({num_users})\n")

def create_and_save():
    save_group()
    create_group()

# Create the admin panel frame, initially hidden
admin_panel_frame = ttk.Frame(root, padding=20)

# Create the admin panel labels and entry widgets
users_label = ttk.Label(users_frame, text="Users")
# Set the width of the entry field
users_entry = ttk.Entry(users_frame, width=50)

groups_label = ttk.Label(groups_frame, text="Groups")
# Set the width of the entry field
groups_entry = ttk.Entry(groups_frame, width=50)

create_button = ttk.Button(create_box, text="CREATE GROUP", command=create_and_save)
create_button.grid(row=3, column=0, columnspan=2, pady=15)


# Set the weight of the rows and columns to make the widgets expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
create_box.grid_rowconfigure(0, weight=1)
create_box.grid_rowconfigure(3, weight=1)
create_box.grid_columnconfigure(0, weight=1)
create_box.grid_columnconfigure(1, weight=1)

# Run the main tkinter event loop
if __name__ == "__main__":

    root.mainloop()