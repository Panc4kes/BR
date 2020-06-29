from tkinter import *
import tkinter.messagebox as tm
import shelve

CURRENT_USER = "Guest"

all_users = []


class User:
    def __init__(self, username, password, BCoins):
        self.username = username
        self.password = password
        self.BCoins = BCoins


def write_password():
    global all_users
    file = shelve.open(r"creds\data")
    file["users"] = all_users


def read_password():
    global all_users
    file = shelve.open(r"creds\data")
    try:
        all_users = file["users"]
    except KeyError:
        pass


def callback():
    raise SystemExit


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.btn_login = Button(
            self, text="Login", width=27, command=self._login_btn_clicked)
        self.btn_login.grid(row=3, columnspan=2)
        root.bind('<Return>', self._login_btn_clicked)

        self.btn_register = Button(
            self, text="Register", width=27,
            command=self._register_btn_clicked)
        self.btn_register.grid(row=4, columnspan=2)

        self.pack()

    def _register_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        for users in all_users:
            if username == users.username:
                tm.showerror("ERROR", "User already registered")
                break
        else:
            if tm.askyesno("Proceed?",
                           "Would you like to register {0}?".format(username)):
                all_users.append(User(username, password, 50))
                write_password()
                tm.showinfo("Success!", "User registered.")

    def _login_btn_clicked(self, *args):
        global CURRENT_USER
        username = self.entry_username.get()
        password = self.entry_password.get()

        read_password()
        for users in all_users:
            if username == users.username:
                if password == users.password:
                    tm.showinfo("Login Success", "Welcome " + users.username)
                    CURRENT_USER = all_users.index(users)
                    root.destroy()
                    break
                else:
                    tm.showerror("Login error", "Incorrect Password")
                    break
        else:
            tm.showerror("Login error", "User not found")


def run():
    global root
    try:
        read_password()

    except KeyError:
        write_password()
        read_password()
    root = Tk()
    LoginFrame(root)
    root.protocol("WM_DELETE_WINDOW", callback)
    root.mainloop()
