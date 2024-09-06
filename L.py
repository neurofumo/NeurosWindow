import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import os
import sys

def rp(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.title("Neuro-sama")
root.geometry("298x215")
root.resizable(False,False)
root.iconbitmap(rp("neuroSetup.ico"))
center_window(root, 298, 215)

def create_messagebox():
    dialog_frame = ttk.Frame(root)
    dialog_frame.pack(expand=True)

create_messagebox()

def neurowindow():
    nwin = tk.Toplevel(root)
    nwin_width = 450
    nwin_height = 318
    nwin.geometry(f"{nwin_width}x{nwin_height}")
    nwin.overrideredirect(True)  
    nwin.lift()
    nwin.resizable(False,False)
    nwin.iconbitmap(rp("neuroSetup.ico"))
    # If you're probably wondering why neuro.png isn't transparent, it's because of this.
    nwin.attributes('-transparentcolor', '#F0F0F0') 

    # GIF support, also supports PNGs so this is unchanged
    gif = Image.open(rp("neuro.png"))
    gif_frames = [
        ImageTk.PhotoImage(frame.convert("RGBA").resize((nwin_width, nwin_height), Image.Resampling.LANCZOS)) 
        for frame in ImageSequence.Iterator(gif)
    ]

    gif_label = tk.Label(nwin, bg="white")
    gif_label.pack(expand=True, fill=tk.BOTH)

    def update_gif(ind):
        frame = gif_frames[ind]
        ind = (ind + 1) % len(gif_frames)
        gif_label.configure(image=frame)
        root.after(100, update_gif, ind)

    root.after(0, update_gif, 0)

    return nwin

nwin = neurowindow()
center_window(nwin, 450, 318)

def sync_windows(event):
    x, y = root.winfo_x(), root.winfo_y()
    nwin.geometry(f"+{x - 75}+{y - 0}")  
    nwin.overrideredirect(True)
    nwin.lift()

root.bind("<Configure>", sync_windows)

def on_closing():
    root.destroy()
    nwin.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

def minimize_windows(event=None):
    root.iconify()
    nwin.state('withdrawn')

def restore_windows(event=None):
    root.deiconify()
    nwin.state('normal')

root.bind("<Unmap>", minimize_windows)
root.bind("<Map>", restore_windows)

root.mainloop()
