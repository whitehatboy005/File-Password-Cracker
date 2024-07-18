import os
import zipfile
import itertools
import string
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import pyzipper
import pikepdf
import rarfile
import py7zr
import patoolib
from lzma import LZMAError

def extract_zip(zip_path, password):
    try:
        with pyzipper.AESZipFile(zip_path) as zip_ref:
            zip_ref.extractall(pwd=password.encode('utf-8'))
            return True
    except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile):
        return False
    except Exception as e:
        return False

def extract_pdf(pdf_path, password):
    try:
        with pikepdf.open(pdf_path, password=password):
            return True
    except pikepdf._qpdf.PasswordError:
        return False
    except Exception as e:
        return False

def extract_rar(rar_path, password):
    try:
        with rarfile.RarFile(rar_path) as rar_ref:
            rar_ref.extractall(pwd=password)
            return True
    except rarfile.BadRarFile:
        return False
    except Exception as e:
        return False

def extract_7z(seven_zip_path, password):
    try:
        with py7zr.SevenZipFile(seven_zip_path, password=password) as seven_zip_ref:
            seven_zip_ref.extractall()
            return True
    except (py7zr.exceptions.CrcError, py7zr.exceptions.Bad7zFile, EOFError, LZMAError, RuntimeError):
        return False
    except Exception as e:
        return False


def extract_with_patool(file_path, password, archive_type):
    try:
        patoolib.extract_archive(file_path, outdir='.', password=password)
        return True
    except Exception as e:
        return False

def dictionary_attack(file_path, password_list_path, file_type):
    with open(password_list_path, 'r') as password_file:
        for line in password_file:
            password = line.strip()
            status_label.config(text=f"Trying password: {password}")
            root.update()
            if file_type == 'zip' and extract_zip(file_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
            elif file_type == 'pdf' and extract_pdf(file_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
            elif file_type == 'rar' and extract_rar(file_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
            elif file_type == '7z' and extract_7z(file_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
            elif file_type in ['gzip', 'bzip2', 'tar', 'wim', 'xz'] and extract_with_patool(file_path, password, file_type):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
    messagebox.showinfo("Failure", "Password not found in the dictionary.")

def brute_force_attack(file_path, max_length, file_type):
    characters = string.ascii_letters + string.digits + string.punctuation
    for length in range(1, max_length + 1):
        for password in itertools.product(characters, repeat=length):
            password = ''.join(password)
            status_label.config(text=f"Trying password: {password}")
            root.update()
            if file_type == 'zip' and extract_zip(file_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
            elif file_type == 'pdf' and extract_pdf(file_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
            elif file_type == 'rar' and extract_rar(file_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
            elif file_type == '7z' and extract_7z(file_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
            elif file_type in ['gzip', 'bzip2', 'tar', 'wim', 'xz'] and extract_with_patool(file_path, password, file_type):
                messagebox.showinfo("Success", f"Password found: {password}")
                return
    messagebox.showinfo("Failure", "Password not found using brute force.")

def select_file():
    selected_file = filedialog.askopenfilename(filetypes=[("All supported files", "*.zip *.pdf *.rar *.7z *.gz *.bz2 *.tar *.wim *.xz")])
    if selected_file:
        file_extension = os.path.splitext(selected_file)[1].lower()
        if file_extension in ['.zip', '.pdf', '.rar', '.7z', '.gz', '.bz2', '.tar', '.wim', '.xz']:
            file_path.set(selected_file)
            file_label.config(text=f"Selected file: {file_path.get()}")
            if file_extension == '.zip':
                file_type.set('zip')
            elif file_extension == '.pdf':
                file_type.set('pdf')
            elif file_extension == '.rar':
                file_type.set('rar')
            elif file_extension == '.7z':
                file_type.set('7z')
            elif file_extension == '.gz':
                file_type.set('gzip')
            elif file_extension == '.bz2':
                file_type.set('bzip2')
            elif file_extension == '.tar':
                file_type.set('tar')
            elif file_extension == '.wim':
                file_type.set('wim')
            elif file_extension == '.xz':
                file_type.set('xz')
        else:
            messagebox.showerror("Invalid File", "The selected file is not supported. Please select a supported file.")
    else:
        messagebox.showerror("Invalid File", "No file selected.")

def select_password_file():
    selected_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if selected_file:
        password_list_path.set(selected_file)
        password_label.config(text=f"Selected Password file: {password_list_path.get()}")

def start_cracking():
    if file_path.get() and password_list_path.get():
        start_time = time.time()
        threading.Thread(target=dictionary_attack, args=(file_path.get(), password_list_path.get(), file_type.get())).start()
        end_time = time.time()
        status_label.config(text=f"Total time taken: {end_time - start_time:.2f} seconds")
    else:
        messagebox.showwarning("Input Required", "Please select both a file and a password list")

root = tk.Tk()
root.title("File Password Cracker")

file_path = tk.StringVar()
password_list_path = tk.StringVar()
file_type = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

file_button = tk.Button(frame, text="Select File", command=select_file)
file_button.grid(row=0, column=0, padx=5, pady=5)

file_label = tk.Label(frame, text="No file selected")
file_label.grid(row=0, column=1, padx=5, pady=5)

password_button = tk.Button(frame, text="Select Password File", command=select_password_file)
password_button.grid(row=1, column=0, padx=5, pady=5)

password_label = tk.Label(frame, text="No password file selected")
password_label.grid(row=1, column=1, padx=5, pady=5)

start_button = tk.Button(frame, text="Start Cracking", command=start_cracking)
start_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(frame, text="Status: Waiting to start")
status_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
