# Entry point: load data, then open the login window; on failure show an error dialog and exit
import os
import sys
import tkinter as tk
from tkinter import messagebox
from data_manager import load_users_posts
from GUI import LoginWindow



def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, "test_data.json")
        users, posts = load_users_posts(data_path)
    except Exception as e:
        tmp = tk.Tk()
        tmp.withdraw()
        messagebox.showerror("Load Error", f"Failed to load data:\n{e}")
        tmp.destroy()
        sys.exit(1)
    root = tk.Tk()
    root.withdraw()
    LoginWindow(root, users, posts)
    root.mainloop()


if __name__ == "__main__":
    main()
