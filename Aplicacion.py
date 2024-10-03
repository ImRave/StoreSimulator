import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class principal:
    def __init__(self, root):
        ventanaPrincipal = root
        ventanaPrincipal.title("Usuario")
        ventanaPrincipal.geometry("500x500")
        ventanaPrincipal.resizable(0,0)

root = Tk()
venPrincipal = principal(root)

root.mainloop()
