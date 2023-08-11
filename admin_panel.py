import tkinter as tk
from tkinter import ttk
import unittest
from tkinter import messagebox
users_frame = None  # Declare global variables for users_frame and groups_frame
groups_frame = None


def login():
    # Replace this function with your login logic
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "admin":
        show_admin_panel()
    else:
        # Show the error message
        login_error_label.config(text="Invalid credentials")
        login_error_label.grid(
            row=3, column=0, columnspan=2, pady=5, sticky="nsew")
        # Raise AssertionError for unittest
        raise AssertionError("Invalid login credentials")


def show_admin_panel():
    def read_names_from_file(filename):
        try:
            with open(filename, 'r') as file:
                names = [name.strip() for name in file.readlines()]
            return names
        except FileNotFoundError:
            return []

    def create_field_box(window, row, column, names): 
        frame = tk.Frame(window, width=400, height=500, bd=1, relief=tk.SOLID, bg="#1A2226")
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="n")
        frame.pack_propagate(False)

        listbox = tk.Listbox(frame, font=('Arial', 14), bg="#1A2226", fg="#ECF0F5",
                             selectbackground="#222D32", selectforeground="#ECF0F5")
        listbox.pack(fill=tk.BOTH, expand=True)
        for name in names:
            listbox.insert(tk.END, name)
            
    def open_chats_file():
        try:
            with open("chats.txt", "r") as chats_file:
                chats = chats_file.read()
            messagebox.showinfo("Chats", chats)
        except FileNotFoundError:
            messagebox.showerror("Error", "Chats file not found!")

    if __name__ == "__main__":
        window = tk.Tk()
        window.title("Users and groups")
        window.geometry("850x600")
        window.config(bg="#1A2226")
        users_label = tk.Label(window, text="Users", font=(
            'Arial', 18, 'bold'), bg="#222D32", fg="#ECF0F5")
        users_label.grid(row=0, column=0, pady=(20, 5), padx=20, sticky="ew")
        users = read_names_from_file("usernames.txt")
        create_field_box(window, row=1, column=0, names=users)
        groups_label = tk.Label(window, text="Groups", font=(
            'Arial', 18, 'bold'), bg="#222D32", fg="#ECF0F5")
        groups_label.grid(row=0, column=1, pady=(20, 5), padx=20, sticky="ew")
        groups = read_names_from_file("groupsname.txt")
        create_field_box(window, row=1, column=1, names=groups)
        chats_button = tk.Button(window, text="Chats", font=(
            'Arial', 12, 'bold'), bg="#3498DB", fg="#ECF0F1", command=open_chats_file)
        chats_button.place(x=20, y=550, anchor="sw")
        window.mainloop()
def show_login_error():
    login_error_label.grid(row=4, column=0, columnspan=2, pady=10)


# Create the main tkinter window
root = tk.Tk()
root.title("Admin Panel")
root.geometry("800x600")  # Set the window size

style = ttk.Style()
style.configure("TLabel", background="#1A2226",
                foreground="#0DB8DE", font=("Roboto", 12))
style.configure("TButton", background="#0DB8DE",
                foreground="#1A2226", font=("Roboto", 12))
style.configure("TEntry", fieldbackground="#1A2226", foreground="#1A2226")
# Set background color for login box
style.configure("TFrame", background="#222D32")
login_box = ttk.Frame(root, padding=20)
login_box.grid(row=0, column=0, sticky="nsew")
login_key = ttk.Label(login_box, text="ADMIN PANEL 🔒",
                      font=("Roboto", 30, "bold"))
login_key.grid(row=0, column=0, columnspan=2, pady=15)
# Create the username and password input fields
username_label = ttk.Label(login_box, text="USERNAME")
username_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
username_entry = ttk.Entry(login_box)
username_entry.grid(row=1, column=1, padx=5, pady=5)
password_label = ttk.Label(login_box, text="PASSWORD")
password_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
password_entry = ttk.Entry(login_box, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)

# Create the login button
login_button = ttk.Button(login_box, text="LOGIN", command=show_admin_panel)
login_button.grid(row=3, column=0, columnspan=2, pady=15)

# Create a label to display login error message
login_error_label = ttk.Label(
    login_box, text="Invalid username or password.", foreground="red")
# Create the admin panel frame, initially hidden
admin_panel_frame = ttk.Frame(root, padding=20)

# Create the admin panel labels and entry widgets
users_label = ttk.Label(users_frame, text="Users")
# Set the width of the entry field
users_entry = ttk.Entry(users_frame, width=50)
groups_label = ttk.Label(groups_frame, text="Groups")
# Set the width of the entry field
groups_entry = ttk.Entry(groups_frame, width=50)

# Set the weight of the rows and columns to make the widgets expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
login_box.grid_rowconfigure(0, weight=1)
login_box.grid_rowconfigure(3, weight=1)
login_box.grid_columnconfigure(0, weight=1)
login_box.grid_columnconfigure(1, weight=1)


class TestAdminPanel(unittest.TestCase):
    def test_login_with_correct_credentials(self):
        show_admin_panel()  # Ensure the admin panel is created before running the test
        username_entry.insert(0, "admin")
        password_entry.insert(0, "admin")
        login_button.invoke()
        self.assertEqual(users_label.grid_info()["row"], 0)
        self.assertEqual(groups_label.grid_info()["row"], 1)

    def test_login_with_incorrect_credentials(self):
        show_admin_panel()  # Ensure the admin panel is created before running the test
        username_entry.insert(0, "wronguser")
        password_entry.insert(0, "wrongpass")
        # Check for AssertionError in unittests
        with self.assertRaises(AssertionError):
            login_button.invoke()
# Run the main tkinter event loop
if __name__ == "__main__":
       root.mainloop()